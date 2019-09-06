# -*- coding:utf-8 -*-
# Copyright 2019 TEEX
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import os

from queue import Queue
import time
import json
import threading
import coloredlogs, logging
from typing import List, Optional, Dict
from backend.kms.kms import KMSConnector, oracle_owner_address

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../lib")))

from pyzil.zilliqa import chain
from pyzil.crypto import zilkey


class Responder(threading.Thread):
    test = True  # for test

    def __init__(self):
        threading.Thread.__init__(self)
        self.res_q = Queue()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(int(os.getenv('Tora-log-level')))
        coloredlogs.install(logger=self.logger)

    def add_response(self, response):
        self.res_q.put(response)

    def run(self):
        print("run the responder")


class ZilliqaResponder(Responder):
    def run(self):
        chain.set_active_chain(chain.TestNet)
        while True:
            self.respond()

    def respond(self):
        if not self.res_q.empty():
            response = self.res_q.get()
            self.logger.info("zilliqa respond: " + response.result)
            if self.test:
                return
            request_id = response.request_id
            proof = '0xD14E8CE1289BDEAFDFA6A50FB5D77A3863BD9AE2DBA36F29FD6175A6A8652E8561CA066F2BC0AFF4C39E077FDBCFCA0F2929CE6440203C41DB1C038FEB8C66CA'  # todo generate the proof
            tora_contract_address = 'zil106hde8sfhslm44632vplgmgkllapt4nktjnyxq'

            data = self.__generate_send_data(method="responseString",
                                             params=[self.__value_dict('id', 'Uint32', str(request_id)),
                                                     self.__value_dict('proof', 'ByStr64', proof),
                                                     self.__value_dict('result', 'String', response.result),
                                                     self.__value_dict('oracle_owner_address', 'ByStr20',
                                                                       oracle_owner_address)
                                                     ])
            resp = self.__send_data_to_contract(tora_contract_address, response.gas_price, response.gas_limit, data)
            print(resp)
        else:
            time.sleep(1)

    @staticmethod
    def __value_dict(vname: str, vtype: str, value: str) -> dict:
        return {"vname": vname, "type": vtype, "value": value}

    @staticmethod
    def bytes_to_int(bytes_hex: bytes, byteorder="big") -> int:
        """Convert bytes to int."""
        return int.from_bytes(bytes_hex, byteorder=byteorder)

    @staticmethod
    def __hex_str_to_bytes(str_hex: str) -> bytes:
        """Convert hex string to bytes."""
        str_hex = str_hex.lower()
        if str_hex.startswith("0x"):
            str_hex = str_hex[2:]
        if len(str_hex) & 1:
            str_hex = "0" + str_hex
        return bytes.fromhex(str_hex)

    @staticmethod
    def __generate_send_data(method: str, params: Optional[List[Dict]]):
        call_data = json.dumps({
            "_tag": method,
            "params": params
        })
        return call_data

    """rewrite the account transfer function"""

    @staticmethod
    def __send_data_to_contract(to_addr: str,
                                gas_price: Optional[int] = None, gas_limit=1,
                                data="", priority=False, timeout=300, sleep=20):
        # to_addr zli... to checksum address
        to_addr = zilkey.normalise_address(to_addr)
        if not to_addr:
            raise ValueError("invalid to address")
        kms_conn = KMSConnector()
        master_tee_nonce = kms_conn.get_master_tee_nonce() + 1
        master_tee_pubkey_bytes = kms_conn.get_master_tee_pubkey()
        master_tee_pubkey = hex(int.from_bytes(master_tee_pubkey_bytes, byteorder="big"))

        data_to_sign = chain.active_chain.get_data_to_sign(master_tee_pubkey_bytes, to_addr,
                                                           0, master_tee_nonce,
                                                           gas_price, gas_limit,
                                                           "", data)
        signature = kms_conn.sign_message(data_to_sign)
        params = {
            "version": chain.active_chain.version,
            "nonce": master_tee_nonce,
            "toAddr": to_addr,
            "amount": str(0),
            "pubKey": '0'+master_tee_pubkey[2:],
            "gasPrice": str(gas_price),
            "gasLimit": str(gas_limit),
            "code": None,
            "data": data or None,
            "signature": signature,
            "priority": priority,
        }

        txn_info = chain.active_chain.api.CreateTransaction(params)

        txn_details = chain.active_chain.wait_txn_confirm(txn_info["TranID"], timeout=timeout, sleep=sleep)
        return txn_details
