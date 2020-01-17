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

"""
A module for to manage secret keys of TEE in two ways:
1. local encryted storage
2. remote KMS service           --- the priority
"""

import socket, ssl
import os


class KMSConnector:
    oracle_owner_address = ''
    rpcserver = ''
    version = ''
    networkid = ''
    host = ''
    port = ''

    @staticmethod
    def set_oracle_owner_address(oracle_owner_addr):
        KMSConnector.oracle_owner_address = oracle_owner_addr

    def __get_conn(self):
        sock = socket.socket(socket.AF_INET)
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.load_cert_chain(certfile=os.path.abspath(os.path.join(os.path.dirname(__file__), "./client.crt"))
                                , keyfile=os.path.abspath(os.path.join(os.path.dirname(__file__), "./client.key")))
        context.load_verify_locations(os.path.abspath(os.path.join(os.path.dirname(__file__),"./root.pem")))
        context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # optional
        ssl.match_hostname = lambda cert, hostname: hostname == cert['subjectAltName'][0][1]
        conn = context.wrap_socket(sock, server_hostname=KMSConnector.host)
        return conn

    def get_master_tee_pubkey(self):
        conn = self.__get_conn()
        try:
            conn.connect((KMSConnector.host, KMSConnector.port))
            conn.write('0'.encode('utf-8'))
            pubkey_bytes = conn.recv()
            return pubkey_bytes
        except:
            return None
        finally:
            conn.close()

    def get_master_tee_nonce(self):
        conn = self.__get_conn()
        try:
            conn.connect((KMSConnector.host, KMSConnector.port))
            conn.write(('1'+KMSConnector.rpcserver+','+KMSConnector.version+','+KMSConnector.networkid).encode('utf-8'))
            nonce = conn.recv().decode()
            return int(nonce)
        except:
            return None
        finally:
            conn.close()

    def sign_message(self, message):
        conn = self.__get_conn()
        try:
            conn.connect((KMSConnector.host, KMSConnector.port))
            conn.sendall('2'.encode('utf-8') + message + b'STOP')
            signature = conn.recv().decode()
            return signature
        except:
            return None
        finally:
            conn.close()

    def withdraw(self, address, money, tora_addr):
        conn = self.__get_conn()
        try:
            conn.connect((KMSConnector.host, KMSConnector.port))
            conn.write(('4'+address+','+str(money)+','+tora_addr+','+KMSConnector.rpcserver+','+KMSConnector.version+','+KMSConnector.networkid).encode('utf-8'))
            result = conn.recv().decode()
            return result
        except:
            return None
        finally:
            conn.close()


if __name__ == '__main__':
    KMSConnector.host = '120.132.103.34'
    KMSConnector.port = 1234
    kms = KMSConnector()
    # kms.get_master_tee_pubkey()
    print(kms.get_master_tee_nonce())
