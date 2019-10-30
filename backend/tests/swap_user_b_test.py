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

import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../lib")))

from pprint import pprint

from pyzil.crypto import zilkey
from pyzil.zilliqa import chain
from pyzil.account import Account
from pyzil.contract import Contract
from pyzil.zilliqa.api import ZilliqaAPI

chain.set_active_chain(chain.TestNet)

# user account
account = Account(private_key="dc15707f4bf08367c89eae066daaa0a2335799fcd75dfb2c4ba514c55bc6e317")
balance = account.get_balance()
print("{}: {}".format(account, balance))

contract_addr = "zil1qhg3lqcmnecd3vtsq03anman887kgnnlkl5qd8"
contract = Contract.load_from_address(contract_addr)
contract.account = account


def commit_swap_hash_test(swap_request_id, user_addr, tx_hash, gas_price, gas_limit):
    resp = contract.call(method="commit_swap_hash", params=[
        Contract.value_dict("swap_request_id", "Uint32", swap_request_id),
        Contract.value_dict("user_addr", "ByStr20", user_addr),
        Contract.value_dict("tx_hash", "String", tx_hash),
        Contract.value_dict("gas_price", "Uint128", gas_price),
        Contract.value_dict("gas_limit", "Uint128", gas_limit)
    ], amount=25)
    pprint(resp)


def appeal_test(swap_request_id):
    resp = contract.call(method="appeal", params=[
        Contract.value_dict("swap_request_id", "Uint32", swap_request_id)
    ])
    pprint(resp)


def __has_txn(api, block_num):
    block_info = api.GetTxBlock(block_num)
    if block_info["header"]["NumTxns"] == 0:
        return False
    else:
        return True


def __get_swap_request_event(account_addr, api, block_num):
    txns = api.GetTransactionsForTxBlock(block_num)
    for txn in txns:
        if len(txn) != 0:
            receipt = api.GetTransaction(txn[0])["receipt"]
            if "event_logs" in receipt:
                event_logs = receipt["event_logs"]
                for event_log in event_logs:
                    if event_log["address"] == (zilkey.normalise_address(contract_addr)).lower():
                        if event_log["_eventname"] == "swap":
                            params = event_log["params"]
                            for param in params:
                                if param["vname"] == "targetaddr" and param["value"] == account_addr.lower():
                                    print(event_log)
                                    return True
    return False


def monitor_swap_request_event(account_addr):
    url = "https://dev-api.zilliqa.com/"
    api = ZilliqaAPI(url)
    cur_block_num = str(int(api.GetCurrentMiniEpoch()) - 1)
    while True & (int(cur_block_num) != 0):
        if int(cur_block_num) >= int(api.GetCurrentMiniEpoch()):
            time.sleep(1)
        else:
            if __has_txn(api, cur_block_num):
                if __get_swap_request_event(account_addr, api, cur_block_num):
                    break
                else:
                    cur_block_num = str(int(cur_block_num) + 1)
            else:
                cur_block_num = str(int(cur_block_num) + 1)


if __name__ == "__main__":
    monitor_swap_request_event("0x7dcB18944157BD73A36DbB61a1700FcFd0182680")
    # commit_swap_hash_test("0", "0x7dcB18944157BD73A36DbB61a1700FcFd0182680", "0xcdca9cf3867180a939342bebe344560e50d99b77fb21d120950cb908cac7bdee", "20000", "1000000000")
