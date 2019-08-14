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

from backend.responder.responder import ZilliqaResponder
import _thread


def run_responder(responder):
    responder.run()


class ResponseDispatcher:
    # responder list
    responders = {}

    def __init__(self):
        self.responders['Zilliqa'] = ZilliqaResponder()
        # run the responders
        for key in self.responders.keys():
            try:
                _thread.start_new_thread(run_responder, (self.responders[key],))
            except:
                print("Error: 无法启动线程")

    def dispatch_response(self, response):
        print(response)
        # responder.respond
        responder = self.responders[response.chain_name]
        if responder is not None:
            responder.add_response(response)
        else:
            print("can not response")
