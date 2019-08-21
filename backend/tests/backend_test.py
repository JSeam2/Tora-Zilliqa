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

import _thread

from backend.monitor.monitor import ZilliqaMonitor
from backend.resolver.resolver import Resolver


def run_monitor(monitor):
    monitor.run()


def run_resolver(monitors):
    resolver = Resolver(monitors)
    resolver.run()


# for test
monitor = ZilliqaMonitor("https://dev-api.zilliqa.com/", "0x7eaedc9e09bc3fbad7515303f46d16fffa15d676")

monitors = []
monitors.append(monitor)

try:
    _thread.start_new_thread(run_monitor, (monitor,))
    _thread.start_new_thread(run_resolver, (monitors,))
except:
    print("Error: 无法启动线程")

while 1:
    pass
