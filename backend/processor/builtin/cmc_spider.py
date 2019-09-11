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

'''
    cmc_spider.py
    
    This is a built-in collector for data on top 100 trading pairs from the top 10 exchanges
    User can invoke this collector by specifying the req_type as "market_trade_pairs_info", without any other parameters. 

    Here we choose the top 10 exchange websites from coinmarketcap, at 2019-8-15 
    IT'S JUST FOR TEST
'''

from bs4 import BeautifulSoup
from re import sub
import certifi
import urllib3
import json


top_exchange_urls = [
    "https://coinmarketcap.com/exchanges/bitmax/",
    "https://coinmarketcap.com/exchanges/bitmex/",
    "https://coinmarketcap.com/exchanges/fcoin/",
    "https://coinmarketcap.com/exchanges/okex/",
    "https://coinmarketcap.com/exchanges/digifinex/",
    "https://coinmarketcap.com/exchanges/cointiger/",
    "https://coinmarketcap.com/exchanges/zb-com/",
    "https://coinmarketcap.com/exchanges/huobi-global/",
    "https://coinmarketcap.com/exchanges/bw-com/",
    "https://coinmarketcap.com/exchanges/exx/"
]


def process(param):

    pair_list = {}
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())


    for url in  top_exchange_urls:

        r = http.request('GET', url)
        soup = BeautifulSoup(r.data, 'html.parser')
        table = soup.find_all(id="exchange-markets")[0].tbody

        for idx, tr in enumerate(table.find_all('tr')):


            if(idx == 100):
                break
            tds = tr.find_all('td')

            pair_name = tds[2].contents[0].string
            volume = tds[3].contents[1].string.strip()

            if(volume == "$?"):
                break
            
            if(pair_list.__contains__(pair_name)):
                pair_list[pair_name] += int(sub(r'[^\d.]', '', volume))
            else:
                pair_list[pair_name] = int(sub(r'[^\d.]', '', volume))


    res = {}
    count = 0
    for i in sorted(pair_list, key=pair_list.__getitem__,reverse=True):
        
        if count == 10:
            break
        count += 1
        
        res[i] = str(pair_list[i])
    return json.dumps(res)

