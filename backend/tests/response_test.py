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

from pprint import pprint

from pyzil.zilliqa import chain
from pyzil.account import Account
from pyzil.contract import Contract

chain.set_active_chain(chain.TestNet)

contract_addr = "zil1ec4jhgn0lr3e55856we44wvjw9zjy9c540gx08"
contract = Contract.load_from_address(contract_addr)

account_sk = "dc15707f4bf08367c89eae066daaa0a2335799fcd75dfb2c4ba514c55bc6e317"
account = Account(private_key=account_sk)
balance = account.get_balance()
print("{}: {}".format(account, balance))

contract.account = account


def response_string(result, gas_price, gas_limit):
    resp = contract.call(method="responseString",
                         params=[Contract.value_dict('id', 'Uint32', '0'),
                                 Contract.value_dict('proof', 'ByStr64',
                                                     '0xD14E8CE1289BDEAFDFA6A50FB5D77A3863BD9AE2DBA36F29FD6175A6A8652E8561CA066F2BC0AFF4C39E077FDBCFCA0F2929CE6440203C41DB1C038FEB8C66CA'),
                                 Contract.value_dict('result', 'String', result)],
                         gas_price=gas_price, gas_limit=gas_limit)
    pprint(resp)
    pprint(contract.last_receipt)


response_string('result string', 2000000000, 20000)


def get_reward():
    resp = contract.call(method="getReward",
                         params=[Contract.value_dict('request_id', 'Uint32', '0')])
    pprint(resp)
    pprint(contract.last_receipt)
