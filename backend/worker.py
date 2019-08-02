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


'''


'''


import click



@click.command()
@click.argument('config',   default="config.ini",   type=click.Path(exists=True))
@click.option(  '--network',default="local",        type=click.Choice(['mainnet','testnet','local']), help="The network choice")
@click.option(  '--host',   default="127.0.0.1:4201", help="The rpc server address")
def main(config,network,host):
    click.echo(config)
    



if __name__ == "__main__":
    main()

