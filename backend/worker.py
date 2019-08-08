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
import click
import logging
import configparser
import monitor


# --||
# registry of required config entries
# client works only when all have been set correctly. 
# --||
_required_cfg = [
    ["master-host","auth","master-host"],
    ["TEE-address","auth","TEE-address"],
    ["rpc-server","zilliqa","rpc-server"],

]

# --||
#
_optional_cfg = [
    ["log-level","debug","level",   "DEBUG"],
    ["log-file", "debug","log-file","worker.log"],
]

#
_log_level_map ={
    "DEBUG":    logging.DEBUG,
    "INFO":     logging.INFO,
    "WARNING":  logging.WARNING,
    "ERROR":    logging.ERROR,
    "CRITICAL": logging.CRITICAL

}


@click.group()
@click.pass_context
@click.option(  '--config',         default="/",    type=click.Path(exists=True))
@click.option(  '--network',        default="",     type=click.Choice(['mainnet','testnet','local','']), help="The network choice")
@click.option(  '--rpcserver',      default="",     help="The rpc server address")
@click.option(  '--teeaddress',     default="",     help="The address of an registered TEE")
def main(ctx,config,network,rpcserver,teeaddress):
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

    #jump to init() here if "init" command is caught
    if ctx.invoked_subcommand != "init":

        if(config != "/"):
            cfg = _parse_config(config)
        else:
            ##TODO: Handler of seperately declared arguments
            print("Please declare arguments in a config file and pass it through '--config' option >.<!!")


        logging.basicConfig(filename=cfg["log-file"],
                            format='%(asctime)s %(levelname)s:%(message)s',
                            level=_log_level_map[cfg["log-level"]])


    ##TODO:invoke KMS
    ##TODO:launch Monitor

    
        
@main.command()
@click.option(  '--account',        default="",                       help="The account of the beneficiary")
@click.option(  '--master',         default="",                       help="The server address of a master TEE")
def init(account, master):
    '''
    Init procedure should be invoked in advance by a newly added oracle node.
    It will generate a config file for later use.

    Args:
        account:
        master:
        output:
    
    Returns:
        None
    
    '''

    #TODO: invoke KMS
    #Here is a stub

    res = {"TEE-address":"0x71F119Dc662Fd0086c7c90C58e5237d74403a0C0",
           "sig":        "0000000000000000000000000000000000000000000000000000000000001111"}
    
    #TODO: invoke the register function in Tora contract 


    #Generate the config file
    config = configparser.ConfigParser()
    config['auth'] = {"master-host":master,
                      "TEE-address":res["TEE-address"]} 

    config['zilliqa'] = {"rpc-server":"127.0.0.1:4201"}
    config['debug'] = {"level":"DEBUG",
                       "log-file":"worker.log"}

    with open('config.ini.default', 'w') as configfile:
        config.write(configfile)

    print("config.ini.default generated!")







def _parse_config(path):
    '''
    The procedure to parse the config file. It will be triggered on receiving valid config path from cli.

    Args:
        path:

    Returns:
        A dict mapping keys to config entries
        which contains all item in _required_cfg and _optional_cfg
        
    '''


    config = configparser.ConfigParser()
    if(os.path.isabs(path)):
        config_path = path
    else:
        curpath = os.path.dirname(os.path.realpath(__file__))
        config_path = os.path.join(curpath, path)

    config.read(config_path, encoding="utf-8")


    res={}

    for item in _required_cfg:
        try:
            res[item[0]] = config[item[1]][item[2]]
        except KeyError:
            print("No such key in your config file:  " + item[2] + " !!")
            exit()
    
    for item in _optional_cfg:
        try:
            res[item[0]] = config[item[1]][item[2]]
        except:
            res[item[0]] = item[3]
    
    return res




if __name__ == "__main__":
    main()

