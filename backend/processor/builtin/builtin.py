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

import sys, os  
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import cmc_spider
from backend.processor.processor import Processor
import logging


#The registry of built-in functions
#where each function is formatted as follow:
# func-name(params: dic) -> str


func_table = {

    "market_trade_pairs_info": cmc_spider.process
    
}


class BuiltIn(Processor):

    def process(self, params):
        
        self.logger.info("Enter Builtin Processor~")

        builtin_name = params["builtin"]

        if( func_table.__contains__(builtin_name)):

            res = func_table[builtin_name](params)

            return res
        
        else:
            #TODO: error handler
            return None
