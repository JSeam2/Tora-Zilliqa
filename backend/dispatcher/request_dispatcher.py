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

from backend.processor.processor import Collector, Executor, Relay
from backend.processor.builtin.builtin  import BuiltIn
import _thread


def run_processor(processor):
    processor.run()


class RequestDispatcher:
    # processor list
    processors = {}

    def __init__(self):
        self.processors[0] = BuiltIn()
        self.processors[1] = Collector()
        self.processors[2] = Executor()
        self.processors[3] = Relay()
        # run the processors
        for key in self.processors.keys():
            try:
                _thread.start_new_thread(run_processor, (self.processors[key],))
            except:
                print("Error: 无法启动线程")

    def dispatch_request(self, request):
        # processor.process
        processor = self.processors[request.type]
        if processor is not None:
            processor.add_request(request)
        else:
            print("can not process the request")
