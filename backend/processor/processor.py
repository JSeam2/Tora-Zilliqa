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
    
    

    def get_request(self):
        if not self.req_q.empty():
            request = self.req_q.get()
            return request
        else:
            return None


    def generate_response_str(self, req, res_str):
        response = Response(req.type, res_str, request.ID, request.chain_name, request.gas_price, request.gas_limit)
        self.dispatcher.dispatch_response(response)

    def process(self, params):
        return

    def run(self):
        while True:

            request = self.get_request()
            if not request:
                time.sleep(10)
            
            else:
                #TODO: Validate the request

                param_data = json.loads(request.param.replace("'", '"'))

                response = self.process(param_data)

                self.generate_response_str(request, response)



class Collector(Processor):

    def process(self, params):
        
        #TODO: Invoke Web API
        print("call the general api")
        return "collect result"


class Executor(Processor):
    def process(self):
        #TODO:
        return


class Relay(Processor):
    def process(self):
        #TODO:
        return

