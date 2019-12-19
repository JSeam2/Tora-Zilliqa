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

from backend.dispatcher.response_dispatcher import ResponseDispatcher
from backend.responder.response import Response
from backend.processor.general_web_api import get_web_api_json_result
from backend.processor.swap_process_register import ZilliqaSwapProcessRegister
from backend.processor.eth_verifier import Verifier
from queue import Queue
import time
import json
import coloredlogs, logging
import threading


class Processor(threading.Thread):

    def __init__(self, configs):
        threading.Thread.__init__(self)

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(int(os.getenv('Tora-log-level')))
        coloredlogs.install(logger=self.logger)

        self.configs = configs

        self.req_q = Queue()
        self.dispatcher = ResponseDispatcher()

    def add_request(self, request):
        self.req_q.put(request)

    def get_request(self):

        if not self.req_q.empty():
            request = self.req_q.get()
            return request
        else:
            return None

    def generate_response_str(self, request, res_str):
        response_method = ""
        if request.type in [0, 1, 3, 4]:
            response_method = "responseString"
        elif request.type == 2:
            response_method = "commit_verify_result"
        response = Response(request.type, response_method, res_str, request.ID, request.chain_name, request.gas_price, request.gas_limit, request.tora_addr, request.user_addr)
        self.dispatcher.dispatch_response(response)

    def process(self, params):
        return

    def run(self):
        while True:

            request = self.get_request()
            if not request:
                time.sleep(1)
            
            else:
                try:
                    param_data = json.loads(request.param.replace("'", '"'))
                    response = self.process(param_data)
                    if response is None:
                        # abort this request
                        continue
                    if not isinstance(response, str):
                        response = str(response)
                except:
                    response = "No correct request params"
                self.generate_response_str(request, response)


class Collector(Processor):

    def process(self, params):
        self.logger.info("Enter Web API Collector~")
        if ('url' not in params.keys()) or ('params' not in params.keys()):
            return "No correct request params"
        result = get_web_api_json_result(params['url'], params['params'])
        return result


class Executor(Processor):
    def process(self, params):
        print("Enter Executor~")
        # TODO:
        return


class SwapRelay(Processor):
    def process(self, params):
        self.logger.info("Enter SwapRelay~")
        swap_id = params['swap_id']
        swap_chain = params['swap_chain']
        initial_chain = params['initial_chain']
        verify_id = params['verify_id']
        swap_process_register = None
        if initial_chain == "Zilliqa":
            swap_process_register = ZilliqaSwapProcessRegister(self.configs['swapContract'])
        if swap_chain == "Ropsten":
            if swap_process_register is not None:
                if self.configs['oracleSK'] is None or self.configs['oracleSK'] == "":
                    self.logger.info("No available sk for relay process")
                    return
                if swap_process_register.register_to_process(self.configs['oracleSK'], verify_id):
                    tx_hash = params['tx_hash']
                    initial_addr = params['initial_addr']
                    target_addr = params['target_addr']
                    swap_money = params['swap_money']
                    if self.configs["ropstenProvider"] is None:
                        self.logger.info("No ropsten provider set")
                        return None
                    verifier = Verifier(self.configs["ropstenProvider"])
                    result = verifier.verify_transaction(tx_hash, swap_id, initial_addr, target_addr, swap_money)
                    return result
                else:
                    self.logger.info("Process register fail, abort the request")
                    return None
            else:
                self.logger.info("Can't process this chain swap")
                return None
        else:
            self.logger.info("Can't process this chain swap")
            return None


class CrossChainInfoRelay(Processor):

    def process(self, params):
        self.logger.info("Enter CrossChainInfoRelay~")
        if 'chain_name' in params.keys() and 'contract_addr' in params.keys() and 'data_positions' in params.keys():
            if params['chain_name'] == 'Ethereum':
                if self.configs["ethereumProvider"] is None:
                    self.logger.info("No ethereum provider set")
                    return None
                contract_addr = params['contract_addr']
                data_positions = params['data_positions']
                verifier = Verifier(self.configs["ethereumProvider"])
                if 'block_number' not in params.keys():
                    result = verifier.verify_state(contract_addr, data_positions)
                else:
                    block_number = params['block_number']
                    result = verifier.verify_state(contract_addr, data_positions, block_number)
                return result
            else:
                self.logger.info("Can't process this chain txn")
                return None
        else:
            return "No correct request params"


class CrossChainTxnVerifier(Processor):
    def process(self, params):
        self.logger.info("Enter CrossChainTxnVerifier~")
        if 'chain_name' in params.keys() and 'txn_hash' in params.keys():
            if params['chain_name'] == 'Ethereum':
                if self.configs["ethereumProvider"] is None:
                    self.logger.info("No ethereum provider set")
                    return None
                verifier = Verifier(self.configs["ethereumProvider"])
                return verifier.verify_transaction_exist(params['txn_hash'])
            else:
                self.logger.info("Can't process this chain txn")
                return None
        else:
            return "No correct request params"
