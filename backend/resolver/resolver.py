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

from backend.dispatcher.request_dispatcher import RequestDispatcher
import time
import threading


class Resolver(threading.Thread):
    

    def __init__(self, monitors, configs):

        threading.Thread.__init__(self)
        self.monitors = monitors
        self.dispatcher = RequestDispatcher(configs)

    def run(self):
        while True:
            for monitor in self.monitors:
                request = monitor.get_front_request()
                if request is not None:
                    # resolve the request params

                    # dispatch the request
                    self.dispatcher.dispatch_request(request)
                else:
                    time.sleep(1)
