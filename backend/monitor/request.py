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


class Request:
    def __init__(self, ID, type, param, gas_price, gas_limit, fee, chain_name, tora_addr):
        self.ID = ID
        self.type = type  # collector 0, executor 1, relay 2
        self.param = param
        self.gas_price = gas_price
        self.gas_limit = gas_limit
        self.fee = fee
        self.chain_name = chain_name
        self.tora_addr = tora_addr
