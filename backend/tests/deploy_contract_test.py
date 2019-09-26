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


from pyzil.zilliqa import chain
from pyzil.account import Account
from pyzil.contract import Contract

chain.set_active_chain(chain.TestNet)


def deploy_contract(contract_file, account_sk):
    # deploy the contract
    code = open(contract_file).read()
    contract = Contract.new_from_code(code)
    print(contract)

    account = Account(private_key=account_sk)
    balance = account.get_balance()
    print("{}: {}".format(account, balance))

    # set account before deploy
    contract.account = account

    contract.deploy(timeout=300, sleep=10)
    assert contract.status == Contract.Status.Deployed


account_sk2 = "919457fa2d81c0b7f1f1918683b1ff6b459c444aefec494c92f34d746ebb6b73"
account_sk1 = ""
# deploy_contract("../../contracts/Tora.scilla", account_sk1)

deploy_contract("../../contracts/TopRequest.scilla", account_sk2)
deploy_contract("../../contracts/GeneralRequest.scilla", account_sk2)
