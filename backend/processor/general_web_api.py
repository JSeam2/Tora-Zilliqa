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


def get_web_api_json_result(url, params):
    ret = requests.get(url, params=params)
    if ret.status_code == 200:
        result = ret.text.replace(" ", "")
        result = result.replace("\n", "")
        return result


# url = "https://samples.openweathermap.org/data/2.5/weather"
# param = {"q": "London,uk", "appid": "b6907d289e10d714a6e88b30761fae22"}
# print(get_web_api_json_result(url, param))
