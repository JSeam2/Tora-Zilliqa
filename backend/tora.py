# -*- coding:utf-8 -*- 
#Copyright 2019 TEEX
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.



import os
import sys

sys.path.append(os.path.abspath( os.path.join( os.path.dirname(__file__),"../")))
sys.path.append(os.path.abspath( os.path.join( os.path.dirname(__file__),"lib")))
import _thread
from backend.monitor.monitor import ZilliqaMonitor
from backend.resolver.resolver import Resolver

import click
import logging
import monitor

from configobj import ConfigObj

# --||
# registry of required config entries
# client works only when all have been set correctly. 
# --||
_required_cfg = [
    ["master-host",     "auth",     "master-host"],
]

_baseChain_cfg_zilliqa = [
    ["baseChainServer",         "rpc-server"],
    ["baseChainID",             "network-id"],
    ["baseChainversion",        "version"],
    ["baseChainContract",       "contract-address"],
]

_optional_cfg = [
    ["log-level","debug","level",   "DEBUG"],
    ["log-file", "debug","log-file","stdout"],
]

_log_level_map ={
    "DEBUG":    logging.DEBUG,
    "INFO":     logging.INFO,
    "WARNING":  logging.WARNING,
    "ERROR":    logging.ERROR,
    "CRITICAL": logging.CRITICAL
}


@click.group()
def main():
    pass
        
        
@main.command(short_help="removed...")
@click.option(  '--account',        default="",                       help="The account of the beneficiary")
@click.option(  '--master',         default="",                       help="The server address of a master TEE")
@click.option(  '--target',         default="zilliqa",                help="The target blockchain name")
def init(account, master, target):
    pass



@main.command()
@click.option(  '--config',         default="/",    type=click.Path(exists=True))
@click.option(  '--network',        default="",     type=click.Choice(['mainnet','testnet','local','']), help="The network choice")
@click.option(  '--rpcserver',      default="",     help="The rpc server address")
@click.option(  '--teeaddress',     default="",     help="The address of an registered TEE")
def launch(config,network,rpcserver,teeaddress):
    '''
    The main procedure of a worker client.

    Args:
        config:
        network:
        rpcserver:
        teeaddress:

    Returns:
        None

    Note: The '--config' option is prior than others. It means if '--config' is set, other options will be ignored even if the config file is incomplete.
    '''

    if(config != "/"):
            cfg = _parse_config(config)
    else:
        ##TODO: Handler of seperately declared arguments
        print("Please declare arguments in a config file and pass it through '--config' option >.<!!")
        exit()


    #Logging Config
    log_file = "" if cfg["log-file"] =="stdout" else cfg["log-file"]
    log_level = cfg["log-level"]

    logging.basicConfig(filename=log_file,
                        format='%(asctime)s %(levelname)s:%(message)s',
                        level=_log_level_map[log_level])


    
    ##TODO:launch Monitor
    
    zilliqa_monitor = ZilliqaMonitor(url = cfg["baseChainServer"], contract_addr = cfg["baseChainContract"])
    resolver = Resolver([zilliqa_monitor])

    logging.info("Monitor lanuched~")
    logging.info("BaseChain: Zilliqa")
    logging.info("RPC-server: " + cfg["baseChainServer"])
    logging.info("Tora Contract Address: " + cfg["baseChainContract"])

  
    zilliqa_monitor.start()
    resolver.start()

    zilliqa_monitor.join()
    resolver.join()

   


def run_resolver(monitors):
    resolver = Resolver(monitors)
    resolver.run()



@main.command(short_help="withdraw toke from master account")
@click.option( '--account',    default="",  help="The account of the beneficiary" )
def withdraw():
    '''
    This function will generate a transaction to transfer the token from TEE accoount to the worker's account.
    '''
    #validate input

    #construct a withdraw transaction

    #invoke the KMS to sign the transaction

    #send the transaction




@main.command(short_help="check worker's balance")
@click.option( '--account',    default="",  help="The account to check" )
def getBalance():

    pass



def _parse_config(path):
    '''
    The procedure to parse the config file. It will be triggered on receiving valid config path from cli.

    Args:
        path:

    Returns:
        A dict mapping keys to config entries
        which contains all item in _required_cfg and _optional_cfg
        
    '''
    res = {}
   
    if(os.path.isabs(path)):
        config_path = path
    else:
        curpath = os.path.dirname(os.path.realpath(__file__))
        config_path = os.path.join(curpath, path)

    config = ConfigObj(config_path)

    for item in _required_cfg:
        try:
            res[item[0]] = config[item[1]][item[2]]
        except KeyError:
            print("No such key in your config file:  " + item[2] + " !!")
            exit()
    
    #for zilliqa
    for item in _baseChain_cfg_zilliqa:
        try:
            res[item[0]] = config["BaseChain"]["zilliqa"][item[1]]
        except KeyError:
            print("No such key in BaseChain-zilliqa section:  " + item[1] + " !!")
            exit()   

    
    for item in _optional_cfg:
        try:
            res[item[0]] = config[item[1]][item[2]]
        except:
            res[item[0]] = item[3]
    
    return res




if __name__ == "__main__":
    main()

