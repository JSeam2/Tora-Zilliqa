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

sys.path.append(os.path.abspath( os.path.join( os.path.dirname(__file__),"../../")))
sys.path.append(os.path.abspath( os.path.join( os.path.dirname(__file__),"../lib")))


from pprint import pprint

from pyzil.zilliqa import chain
from pyzil.account import Account
from pyzil.contract import Contract
from pyzil.crypto import schnorr

chain.set_active_chain(chain.TestNet)

contract_addr = "zil16et2dwg4cyueyrz96ex5lp83me73qzet8glhal"
contract = Contract.load_from_address(contract_addr)

account_sk = "dc15707f4bf08367c89eae066daaa0a2335799fcd75dfb2c4ba514c55bc6e317"
account = Account(private_key=account_sk)
balance = account.get_balance()
print("{}: {}".format(account, balance))

contract.account = account


def register_test(owner_addr, pk, proof):
    resp = contract.call(method="register", params=[
        Contract.value_dict("owner_address", "ByStr20", owner_addr),
        Contract.value_dict("pk", "ByStr33", pk),
        Contract.value_dict("proof", "ByStr64", proof)])
    pprint(resp)
    pprint(contract.last_receipt)


def leave_test():
    resp = contract.call(method="leave", params=[])
    pprint(resp)
    pprint(contract.last_receipt)


def comeback_test():
    resp = contract.call(method="comeback", params=[])
    pprint(resp)
    pprint(contract.last_receipt)


def bytes_to_int(bytes_hex: bytes, byteorder="big") -> int:
    """Convert bytes to int."""
    return int.from_bytes(bytes_hex, byteorder=byteorder)


# pk = "0x03CC285856FEE0DB4E856B27AC25848D824E440BBAF391C86C20DC469EDAEB7A98"
ec_point = schnorr.get_public_key(0xdc15707f4bf08367c89eae066daaa0a2335799fcd75dfb2c4ba514c55bc6e317)
pk = hex(bytes_to_int(schnorr.encode_public(ec_point.x, ec_point.y)))

pprint(str(pk).upper())

register_test("0x7dcB18944157BD73A36DbB61a1700FcFd0182680",
              "0x03CC285856FEE0DB4E856B27AC25848D824E440BBAF391C86C20DC469EDAEB7A98",
              "0xD14E8CE1289BDEAFDFA6A50FB5D77A3863BD9AE2DBA36F29FD6175A6A8652E8561CA066F2BC0AFF4C39E077FDBCFCA0F2929CE6440203C41DB1C038FEB8C66CA")

leave_test()

comeback_test()
