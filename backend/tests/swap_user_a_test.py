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


def new_swap_request_test(swap_chain, initial_money, swap_money, target_addr, swap_chain_initial_addr, swap_chain_target_addr):
    resp = contract.call(method="request_swap", params=[
        Contract.value_dict("swap_chain", "String", swap_chain),
        Contract.value_dict("initial_money", "Uint128", str(initial_money)),
        Contract.value_dict("swap_money", "Uint128", str(swap_money)),
        Contract.value_dict("target_addr", "ByStr20", target_addr),
        Contract.value_dict("swap_chain_initial_addr", "ByStr20", swap_chain_initial_addr),
        Contract.value_dict("swap_chain_target_addr", "ByStr20", swap_chain_target_addr)
    ], amount=initial_money/1000000000000, priority=True)
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
                        if event_log["_eventname"] == "Swap success":
                            params = event_log["params"]
                            for param in params:
                                if param["vname"] == "initialaddr" and param["value"] == account_addr.lower():
                                    print(event_log)
                                    return True
    return False


def monitor_swap_success_event(account_addr):
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
    new_swap_request_test("Ethereum", 1000000000000, 1, "0x7dcB18944157BD73A36DbB61a1700FcFd0182680", "0x734Ac651Dd95a339c633cdEd410228515F97fAfF", "0x7006abF3216445aaE379Ac77c9b89929147F5301")
    # monitor_swap_success_event("0x7dcB18944157BD73A36DbB61a1700FcFd0182680")
