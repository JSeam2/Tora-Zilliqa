import time
import json
from typing import List, Optional, Dict
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../lib")))

from pyzil.zilliqa import chain
from pyzil.crypto import zilkey
from backend.kms.kms import KMSConnector, oracle_owner_address


def respond():
    chain.set_active_chain(chain.TestNet)
    proof = '0xD14E8CE1289BDEAFDFA6A50FB5D77A3863BD9AE2DBA36F29FD6175A6A8652E8561CA066F2BC0AFF4C39E077FDBCFCA0F2929CE6440203C41DB1C038FEB8C66CA'  # todo sign with kms
    tora_contract_address = 'zil106hde8sfhslm44632vplgmgkllapt4nktjnyxq'

    data = __generate_send_data(method="responseString",
                                params=[__value_dict('id', 'Uint32', '0'),
                                        __value_dict('proof', 'ByStr64', proof),
                                        __value_dict('result', 'String', 'result string'),
                                        __value_dict('oracle_owner_address', 'ByStr20',
                                                     oracle_owner_address)
                                        ])
    resp = __send_data_to_contract(tora_contract_address, 1000000000, 10000, data)
    print(resp)


def __value_dict(vname: str, vtype: str, value: str) -> dict:
    return {"vname": vname, "type": vtype, "value": value}


def __hex_str_to_bytes(str_hex: str) -> bytes:
    """Convert hex string to bytes."""
    str_hex = str_hex.lower()
    if str_hex.startswith("0x"):
        str_hex = str_hex[2:]
    if len(str_hex) & 1:
        str_hex = "0" + str_hex
    return bytes.fromhex(str_hex)


def __generate_send_data(method: str, params: Optional[List[Dict]]):
    call_data = json.dumps({
        "_tag": method,
        "params": params
    })
    return call_data


"""rewrite the account transfer function"""


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
    print(master_tee_pubkey)

    data_to_sign = chain.active_chain.get_data_to_sign(master_tee_pubkey_bytes, to_addr,
                                                       master_tee_nonce, 0,
                                                       gas_price, gas_limit,
                                                       '', data)
    print(data_to_sign)
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
    print(params)
    txn_info = chain.active_chain.api.CreateTransaction(params)

    txn_details = chain.active_chain.wait_txn_confirm(txn_info["TranID"], timeout=timeout, sleep=sleep)
    return txn_details


def hex_str_to_bytes(str_hex: str) -> bytes:
    """Convert hex string to bytes."""
    str_hex = str_hex.lower()
    if str_hex.startswith("0x"):
        str_hex = str_hex[2:]
    if len(str_hex) & 1:
        str_hex = "0" + str_hex
    return bytes.fromhex(str_hex)


if __name__ == "__main__":
    respond()
