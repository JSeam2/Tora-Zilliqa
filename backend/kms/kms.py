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
A module for to manage secret keys of TEE in two ways:
1. local encryted storage
2. remote KMS service           --- the priority



TODO: 
Stub Module currently..

Key for test:

addr: 0x71F119Dc662Fd0086c7c90C58e5237d74403a0C0
pk:   020748e12e9dfc0f83c88eec4528b9a1b1084e80d410158be97953e9980351f254
sk:   42914050bd0700e2be7c4772b586adb5f3cb5a340caec372a070038086f32891

'''

import socket, ssl
import os

HOST, PORT = '127.0.0.1', 1234


class KMSConnector:
    oracle_owner_address = ''
    rpcserver = ''
    version = ''
    networkid = ''

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
        conn = context.wrap_socket(sock, server_hostname=HOST)
        return conn

    def new_master_tee(self, password):
        conn = self.__get_conn()
        try:
            conn.connect((HOST, PORT))
            conn.write(('3'+password).encode('utf-8'))
            result = conn.recv().decode('utf-8')
            if result == "":
                return "Have no authority"
            else:
                return result.split(',')
        except:
            return None
        finally:
            conn.close()

    def get_master_tee_pubkey(self):
        conn = self.__get_conn()
        try:
            conn.connect((HOST, PORT))
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
            conn.connect((HOST, PORT))
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
            conn.connect((HOST, PORT))
            conn.sendall('2'.encode('utf-8') + message + b'STOP')
            signature = conn.recv().decode()
            # self.conn.close()
            return signature
        except:
            return None
        finally:
            conn.close()

    def withdraw(self, address, money, tora_addr):
        conn = self.__get_conn()
        try:
            conn.connect((HOST, PORT))
            conn.write(('4'+address+','+str(money)+','+tora_addr+','+KMSConnector.rpcserver+','+KMSConnector.version+','+KMSConnector.networkid).encode('utf-8'))
            result = conn.recv().decode()
            # self.conn.close()
            return result
        except:
            return None
        finally:
            conn.close()



if __name__ == '__main__':
    kms = KMSConnector()
    # kms.get_master_tee_pubkey()
    # kms.get_master_tee_nonce()
    # kms.sign_message(
    #     b'\x08\x81\x80\xb4\n\x10\x07\x1a\x14~\xae\xdc\x9e\t\xbc?\xba\xd7QS\x03\xf4m\x16\xff\xfa\x15\xd6v"#\n!\x03\xf8\x96\x0c$K\xc9\xfdO\x80\xf7\x8f\xe7\x95lP\xdc,\xf7)6\xb4\xe1\x94\xe7]E}RG+\x0e\xe8*\x12\n\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x002\x12\n\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00;\x9a\xca\x008\x90NJ\xbb\x03{"_tag": "responseString", "params": [{"vname": "id", "type": "Uint32", "value": "0"}, {"vname": "proof", "type": "ByStr64", "value": "0xD14E8CE1289BDEAFDFA6A50FB5D77A3863BD9AE2DBA36F29FD6175A6A8652E8561CA066F2BC0AFF4C39E077FDBCFCA0F2929CE6440203C41DB1C038FEB8C66CA"}, {"vname": "result", "type": "String", "value": "result string"}, {"vname": "oracle_owner_address", "type": "ByStr20", "value": "0x7dcB18944157BD73A36DbB61a1700FcFd0182680"}]}')
    print(kms.new_master_tee("Zilliqa"))
