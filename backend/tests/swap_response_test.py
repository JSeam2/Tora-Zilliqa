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
account = Account(private_key="919457fa2d81c0b7f1f1918683b1ff6b459c444aefec494c92f34d746ebb6b73")
balance = account.get_balance()
print("{}: {}".format(account, balance))

contract_addr = "zil13a4dul8j27tqu6s0v3xs8q25m9d7nm5n4u45mc"
contract = Contract.load_from_address(contract_addr)
contract.account = account


def register_to_process_test(verify_request_id):
    resp = contract.call(method="register_to_process", params=[
        Contract.value_dict("verify_request_id", "Uint32", verify_request_id)
    ], amount=2)
    pprint(resp)
    if not resp:
        pprint("Register fail")
    if resp['receipt']['success']:
        if "event_logs" in resp['receipt']:
            event_logs = resp['receipt']["event_logs"]
            for event_log in event_logs:
                if event_log['_eventname'] == 'register success':
                    pprint('Verify the request...')
                    return
        pprint('Register fail')


def commit_verify_result_test(verify_request_id, result, oracle_owner_address):
    resp = contract.call(method="commit_verify_result", params=[
        Contract.value_dict('verify_request_id', 'Uint32', verify_request_id),
        Contract.value_dict('result', 'String', result),
        Contract.value_dict('oracle_owner_address', 'ByStr20', oracle_owner_address)
    ])
    pprint(resp)


if __name__ == "__main__":
    # register_to_process_test("1")
    commit_verify_result_test("1", "True", "0xa391fb22ef65d65167a0c94d5e9b6eacece56c7e")
