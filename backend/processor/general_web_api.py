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

import requests


def get_web_api_json_result(url, param):
    ret = requests.get(url + param, params={"format": "json"})
    if ret.status_code == 200:
        print(ret.text)
        return ret.text


# url = "https://blockchain.info/rawblock/"
# param = "0000000000000bae09a7a393a8acded75aa67e46cb81f7acaa5ad94f9eacd103"
# get_web_api_json_result(url, param)
