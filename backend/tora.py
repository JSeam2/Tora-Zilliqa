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
import time

sys.path.append(os.path.abspath( os.path.join( os.path.dirname(__file__),"../")))
sys.path.append(os.path.abspath( os.path.join( os.path.dirname(__file__),"lib")))

from backend.monitor.monitor import ZilliqaMonitor
from backend.resolver.resolver import Resolver
from backend.kms.kms import KMSConnector

import click
import coloredlogs, logging
import monitor

from configobj import ConfigObj


from pyzil.account import Account
from pyzil.contract import Contract
from pyzil.crypto import zilkey
from pyzil.zilliqa import chain
from pyzil.zilliqa.chain import BlockChain

# --||
# registry of required config entries
# client works only when all have been set correctly. 
# --||
_required_cfg = [
    ["master-host",     "auth",     "master-host"],
    ["oracle-account",     "auth",     "account"],
]

_baseChain_cfg_zilliqa = [
    ["baseChainServer",         "rpc-server"],
    ["baseChainID",             "network-id"],
    ["baseChainversion",        "version"],
    ["baseChainContract",       "contract-address"],
]

_kms_cfg = [
    ["KMS_HOST", "host"],
    ["KMS_PORT", "port"],
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


# for oracle node to launch
@main.command()
@click.option('--config',         default="config.ini",    type=click.Path(exists=True))
def launch(config):
    '''
    The main procedure of a worker client.

    Args:
        config:

    Returns:
        None

    Note: The '--config' option is prior than others. It means if '--config' is set, other options will be ignored even if the config file is incomplete.
    '''

    cfg = _parse_config(config)

    #Logging Config

    log_file = "" if cfg["log-file"] =="stdout" else cfg["log-file"]
    log_level = _log_level_map[cfg["log-level"]]

    os.environ['Tora-log-level']=str(log_level)

    # logging.basicConfig(filename="log_file",
    #                     format='%(asctime)s %(levelname)s %(filename)s: %(message)s')

    logger =logging.getLogger(__name__)
    logger.setLevel(log_level)
    coloredlogs.install(logger=logger)

    # set the active chain
    local_chain = BlockChain(cfg["baseChainServer"], int(cfg["baseChainversion"]), int(cfg["baseChainID"]))
    chain.set_active_chain(local_chain)
    KMSConnector.rpcserver = cfg["baseChainServer"]
    KMSConnector.version = cfg["baseChainversion"]
    KMSConnector.networkid = cfg["baseChainID"]
    KMSConnector.host = str(cfg["KMS_HOST"])
    KMSConnector.port = int(cfg["KMS_PORT"])
    KMSConnector.oracle_owner_address = cfg["oracle-account"]
    
    ##TODO:launch Monitor
    
    zilliqa_monitor = ZilliqaMonitor(url = cfg["baseChainServer"], contract_addr = cfg["baseChainContract"])
    resolver = Resolver([zilliqa_monitor])

    logger.info("Monitor lanuched~")
    logger.info("BaseChain: Zilliqa")
    logger.info("RPC-server: " + cfg["baseChainServer"])
    logger.info("Tora Contract Address: " + cfg["baseChainContract"])

  
    zilliqa_monitor.start()
    resolver.start()

    zilliqa_monitor.join()
    resolver.join()


def run_resolver(monitors):
    resolver = Resolver(monitors)
    resolver.run()



@main.command(short_help="withdraw toke from master account")
@click.option('--config',         default="config.ini",    type=click.Path(exists=True))
@click.option('--sk', help="The account sk")
@click.option('--address', help="The account address of the beneficiary" )
@click.option('--gas_price',  default=1000000000)
@click.option('--gas_limit',  default=10000)
def withdraw(config, sk, address, gas_price, gas_limit):

    '''
    This function will generate a transaction to transfer the token from TEE accoount to the worker's account.
    '''
    cfg = _parse_config(config)

    # set the active chain
    local_chain = BlockChain(cfg["baseChainServer"], int(cfg["baseChainversion"]), int(cfg["baseChainID"]))
    chain.set_active_chain(local_chain)
    KMSConnector.rpcserver = cfg["baseChainServer"]
    KMSConnector.version = cfg["baseChainversion"]
    KMSConnector.networkid = cfg["baseChainID"]
    KMSConnector.host = str(cfg["KMS_HOST"])
    KMSConnector.port = int(cfg["KMS_PORT"])

    contract_addr = cfg["baseChainContract"]
    contract = Contract.load_from_address(contract_addr)

    account = Account(private_key=sk)
    contract.account = account
    resp = contract.call(method="get_reward_balance",
                             params=[Contract.value_dict('oracle_owner_address', 'ByStr20', zilkey.normalise_address(address))],
                             gas_price=gas_price, gas_limit=gas_limit)
    if (resp is not None) and (not resp['receipt']['success']):
        print("Network error")
    else:
        if (resp['receipt']['event_logs'][0]['params'][0]['value']['arguments'] == []) or (resp['receipt']['event_logs'][0]['params'][0]['value']['arguments']==['0']):
            print("No money")
        else:
            money = int(resp['receipt']['event_logs'][0]['params'][0]['value']['arguments'][0])/1000000000000.0
            print("Have money: " + str(money))
            kms = KMSConnector()
            if kms.withdraw(zilkey.normalise_address(address), money, cfg["baseChainContract"])=="success":
                print("Withdraw submit success")
                time.sleep(300)
                print("Withdraw success")
            elif kms.withdraw(zilkey.normalise_address(address), money, cfg["baseChainContract"]) is None:
                print("KMS server has no response")
            else:
                print("Withdraw submit fail")


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

    #for kms
    for item in _kms_cfg:
        try:
            res[item[0]] = config["KMS"][item[1]]
        except KeyError:
            print("No such key in KMS section:  " + item[1] + " !!")
            exit()

    
    for item in _optional_cfg:
        try:
            res[item[0]] = config[item[1]][item[2]]
        except:
            res[item[0]] = item[3]
    
    return res




if __name__ == "__main__":
    main()

