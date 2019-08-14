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

import sys
sys.path.append('../../')

from backend.dispatcher.response_dispatcher import ResponseDispatcher
from backend.responder.response import Response
from queue import Queue
import time
import json


class Processor:
    dispatcher = ResponseDispatcher()
    req_q = Queue()

    def add_request(self, request):
        self.req_q.put(request)

    def process(self):
        return

    def run(self):
        while True:
            self.process()


class Collector(Processor):
    def process(self):
        if not self.req_q.empty():
            request = self.req_q.get()
            param_data = json.loads(request.param.replace("'", '"'))
            if param_data["builtin"] != "":
                builtin_name = param_data["builtin"]
                if builtin_name == "market_trade_pairs_info":
                    # todo
                    print("call the builtin function: " + builtin_name)
            else:
                # todo
                print("call the general api")
            response = Response(0, "collect result", request.ID, request.chain_name, request.gas_price, request.gas_limit)
            self.dispatcher.dispatch_response(response)
        else:
            time.sleep(10)


class Executor(Processor):
    def process(self):
        # todo
        return


class Relay(Processor):
    def process(self):
        # todo
        return
