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

from pyzil.crypto import zilkey
from pyzil.zilliqa import chain
from pyzil.account import Account
from pyzil.contract import Contract

chain.set_active_chain(chain.TestNet)

account = Account(private_key="67d8c95700458aff274734dd2267dce59e67f9d9269739ff768c5f36cc5c6f94")
balance = account.get_balance()
print("{}: {}".format(account, balance))

contract_addr = "zil1tguejn657waxjaddynns9z9s3ek908d46cc67d"
contract = Contract.load_from_address(contract_addr)
contract.account = account

oracle_address = '0x' + zilkey.to_valid_address("zil1ec4jhgn0lr3e55856we44wvjw9zjy9c540gx08")


resp = contract.call(method="request", params=[], gas_price=2000000000, gas_limit=20000)
pprint(resp)
pprint(contract.last_receipt)
