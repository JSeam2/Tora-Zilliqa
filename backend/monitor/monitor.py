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

from queue import Queue
import time


class Monitor:
    req_q = Queue()

    def run(self):
        print("run the monitor")

    def get_front_request(self):
        if not self.req_q.empty():
            return self.req_q.get()
        else:
            return None


class ZilliqaMonitor(Monitor):

    def run(self):
        while True:
            # get requests from chain
            time.sleep(200)


