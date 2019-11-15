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

# oracle_address = '0x' + zilkey.to_valid_address("zil1vxv8lsha9cx4a2fth74zvd8e22y8eh85px4thu")
# pprint(oracle_address)


def __has_txn(api, block_num):
    block_info = api.GetTxBlock(block_num)
    if block_info["header"]["NumTxns"] == 0:
        return False
    else:
        return True


def __get_response_from_block(contract_addr, api, block_num):
    txns = api.GetTransactionsForTxBlock(block_num)
    for txn in txns:
        if len(txn) != 0:
            receipt = api.GetTransaction(txn[0])["receipt"]
            if "event_logs" in receipt:
                event_logs = receipt["event_logs"]
                for event_log in event_logs:
                    if event_log["address"] == (zilkey.normalise_address(contract_addr)).lower():
                        if event_log["_eventname"] == "callback":
                            print("Get a response...")
                            print(event_log)
                            return True
    return False


def get_response_event(contract_addr):
    url = "https://dev-api.zilliqa.com/"
    api = ZilliqaAPI(url)
    cur_block_num = str(int(api.GetCurrentMiniEpoch()) - 10)
    while True & (int(cur_block_num) != 0):
        if int(cur_block_num) >= int(api.GetCurrentMiniEpoch()):
            time.sleep(1)
        else:
            if __has_txn(api, cur_block_num):
                if __get_response_from_block(contract_addr, api, cur_block_num):
                    break
                else:
                    cur_block_num = str(int(cur_block_num) + 1)
            else:
                cur_block_num = str(int(cur_block_num) + 1)


def test_cross_chain_info():
    # request contract address
    contract_addr = "zil1muhe748ch3awrkvrtth39aswu3a539q0t7ves8"
    contract = Contract.load_from_address(contract_addr)
    contract.account = account
    print("Waiting for the request published on chain...")
    resp = contract.call(method="request", params=[], amount=25, priority=True)
    if resp['receipt']['success']:
        event_logs = resp['receipt']['event_logs']
        if event_logs[0]['_eventname'] == 'request':
            print("Request committed successfully, waiting the response...")
            get_response_event(contract_addr)
        else:
            print("Commit fail, please see the event log")
            pprint(event_logs)
    else:
        print("Commit fail")
        pprint(resp)


def test_cross_chain_txn():
    # request contract address
    contract_addr = "zil1sl4zqk7x2ure00plx864957tame22sw9ud3j2h"
    contract = Contract.load_from_address(contract_addr)
    contract.account = account
    print("Waiting for the request published on chain...")
    resp = contract.call(method="request", params=[], amount=15, priority=True)
    if resp['receipt']['success']:
        event_logs = resp['receipt']['event_logs']
        if event_logs[0]['_eventname'] == 'request':
            print("Request committed successfully, waiting the response...")
            get_response_event(contract_addr)
        else:
            print("Commit fail, please see the event log")
            pprint(event_logs)
    else:
        print("Commit fail")
        pprint(resp)


if __name__ == "__main__":
    test_cross_chain_info()
    test_cross_chain_txn()
