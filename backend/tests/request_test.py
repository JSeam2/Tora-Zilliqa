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

from pyzil.crypto import zilkey
from pyzil.zilliqa import chain
from pyzil.account import Account
from pyzil.contract import Contract

chain.set_active_chain(chain.TestNet)

# user account
account = Account(private_key="dc15707f4bf08367c89eae066daaa0a2335799fcd75dfb2c4ba514c55bc6e317")
balance = account.get_balance()
print("{}: {}".format(account, balance))

# oracle_address = '0x' + zilkey.to_valid_address("zil13f4l3cjtw40x3qvrg3y67ywdu99yc6vruh4h7t")
# pprint(oracle_address)


def test_trading_pairs():
    # request contract address
    contract_addr = "zil1a0vs39fgx08ngcmtjdv7r3l8yclrcrptrdzaqz"  # test request
    contract = Contract.load_from_address(contract_addr)
    contract.account = account
    resp = contract.call(method="request", params=[], amount=15)
    pprint(resp)
    pprint(contract.last_receipt)


def test_web_api():
    # request contract address
    contract_addr = "zil18aule5w5syw830kr9lnad3evvtg7extapkmeck"  # test request
    contract = Contract.load_from_address(contract_addr)
    contract.account = account
    resp = contract.call(method="request", params=[], amount=15)
    pprint(resp)
    pprint(contract.last_receipt)


if __name__ == "__main__":
    test_trading_pairs()
    test_web_api()
