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

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../lib")))

from pprint import pprint

from pyzil.zilliqa import chain
from pyzil.account import Account
from pyzil.contract import Contract

chain.set_active_chain(chain.TestNet)

# tora contract address
# contract_addr = "zil106hde8sfhslm44632vplgmgkllapt4nktjnyxq"
contract_addr = "zil188cxacmwwdzagnwpv4gharfsdgdxacfu4njdd5"
contract = Contract.load_from_address(contract_addr)

# master tee sk
account_sk = "919457fa2d81c0b7f1f1918683b1ff6b459c444aefec494c92f34d746ebb6b73"
account = Account(private_key=account_sk)
balance = account.get_balance()
print("{}: {}".format(account, balance))

contract.account = account


def response_string(result, gas_price, gas_limit, oracle_owner_address):
    resp = contract.call(method="responseString",
                         params=[Contract.value_dict('id', 'Uint32', '2'),
                                 Contract.value_dict('proof', 'ByStr64',
                                                     '0xD14E8CE1289BDEAFDFA6A50FB5D77A3863BD9AE2DBA36F29FD6175A6A8652E8561CA066F2BC0AFF4C39E077FDBCFCA0F2929CE6440203C41DB1C038FEB8C66CA'),
                                 Contract.value_dict('result', 'String', result),
                                 Contract.value_dict('oracle_owner_address', 'ByStr20', oracle_owner_address)],
                         gas_price=gas_price, gas_limit=gas_limit)
    pprint(resp)
    pprint(contract.last_receipt)


response_string('result string', 1000000000, 10000, '0x7dcB18944157BD73A36DbB61a1700FcFd0182680')
