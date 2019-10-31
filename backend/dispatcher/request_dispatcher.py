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
import coloredlogs
import logging
import os

from backend.processor.processor import Collector, Executor, SwapRelay, CrossChainInfoRelay
from backend.processor.builtin.builtin import BuiltIn


class RequestDispatcher:
    # processor list
    processors = {}

    def __init__(self, configs):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(int(os.getenv('Tora-log-level')))
        coloredlogs.install(logger=self.logger)

        self.processors[0] = BuiltIn()
        self.processors[1] = Collector()
        self.processors[2] = SwapRelay()
        self.processors[2].set_ethereum_provider(configs['ethereum-provider'])
        self.processors[3] = CrossChainInfoRelay()
        self.processors[3].set_ethereum_provider(configs['ethereum-provider'])
        self.processors[4] = Executor()
        # run the processors
        for key in self.processors.keys():
            self.processors[key].start()

    def dispatch_request(self, request):
        # processor.process
        processor = self.processors[request.type]
        if processor is not None:
            processor.add_request(request)
        else:
            self.logger.info("Can not process this type request")
