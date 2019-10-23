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

from web3 import Web3, HTTPProvider
from ethereum import (
    block,
    transactions,
    utils
)
import rlp
from trie import HexaryTrie
from trie.constants import (
    BLANK_NODE,
    BLANK_NODE_HASH,
    NODE_TYPE_BLANK,
    NODE_TYPE_LEAF,
    NODE_TYPE_EXTENSION,
    NODE_TYPE_BRANCH,
    BLANK_HASH,
)
from trie.utils.nodes import *
from trie.utils.nibbles import encode_nibbles, decode_nibbles, bytes_to_nibbles
import math
from eth_hash.auto import (
    keccak,
)
from rlp.codec import encode_raw


def rec_hex(x):
    if isinstance(x, list):
        return [rec_hex(elem) for elem in x]
    else:
        return utils.encode_hex(x)


def rec_bin(x):
    if isinstance(x, list):
        return [rec_bin(elem) for elem in x]
    elif isinstance(x, int):
        return x
    elif isinstance(x, str):
        if x.startswith("0x"):
            if len(x) != 2:
                return utils.decode_hex(x[2:])
            else:
                return 0
        else:
            return utils.decode_hex(x)
    elif x is None:
        return 0


def normalize_bytes(hash):
    if isinstance(hash, str):
        if hash.startswith("0x"):
            hash = hash[2:]
        if len(hash) % 2 != 0:
            hash = '0' + hash
        return utils.decode_hex(hash)
    elif isinstance(hash, int):
        return hash.to_bytes(length=(math.ceil(hash.bit_length() / 8)),
                             byteorder="big",
                             signed=False)
    else:
        return bytes(hash)


class Verifier:
    def __init__(self, chain):
        self.web3 = Web3(HTTPProvider(chain))

    def verify_transaction(self, tx_hash):
        # verify the block hash
        target_tx = self.web3.eth.getTransaction(tx_hash)
        if target_tx is None:
            return False
        block_info = self.web3.eth.getBlock(target_tx.blockHash, True)
        if not self.verify_block_hash(block_info):
            return False
        if not self.verify_transaction_hash(block_info, tx_hash):
            return False
        return True

    @staticmethod
    def verify_block_hash(block_info):
        # get block header from block info
        header = block.BlockHeader(
            normalize_bytes(block_info["parentHash"]),
            normalize_bytes(block_info["sha3Uncles"]),
            utils.normalize_address(block_info["miner"]),
            normalize_bytes(block_info["stateRoot"]),
            normalize_bytes(block_info["transactionsRoot"]),
            normalize_bytes(block_info["receiptsRoot"]),
            utils.bytes_to_int(normalize_bytes(block_info["logsBloom"])),
            utils.parse_as_int(block_info['difficulty']),
            utils.parse_as_int(block_info['number']),
            utils.parse_as_int(block_info['gasLimit']),
            utils.parse_as_int(block_info['gasUsed']),
            utils.parse_as_int(block_info['timestamp']),
            normalize_bytes(block_info["extraData"]),
            normalize_bytes(block_info["mixHash"]),
            normalize_bytes(block_info["nonce"]),
        )
        # calculate the block hash
        # compare the block hash with trusted block hash
        if normalize_bytes(block_info.hash) != header.hash:
            return False
        else:
            return True

    def verify_transaction_hash(self, block_info, tx_hash):
        txns = block_info.transactions
        tx_index = 0
        # generate the mpt
        mpt = HexaryTrie(db={})
        for tx_dict in txns:
            if tx_dict.hash == tx_hash:
                tx_index = tx_dict.transactionIndex
            key = rlp.encode(utils.parse_as_int(tx_dict['transactionIndex']))
            mpt.set(key, self.rlp_transaction(tx_dict))
        # verify the tx root
        if mpt.root_hash != normalize_bytes(block_info.transactionsRoot):
            return False
        # generate the proof
        mpt_key_nibbles = bytes_to_nibbles(rlp.encode(tx_index))
        stack = self.generate_proof(mpt, mpt_key_nibbles)
        print(stack)
        print(mpt.get_proof(rlp.encode(tx_index)))
        # print("=======")
        # print(mpt.root_hash)
        # print("--------")
        # for node in stack:
        #     print(keccak(encode_raw(node)))

    @staticmethod
    def rlp_transaction(tx_dict: dict):
        t = transactions.Transaction(
            utils.parse_as_int(tx_dict['nonce']),
            utils.parse_as_int(tx_dict['gasPrice']),
            utils.parse_as_int(tx_dict['gas']),
            normalize_bytes(tx_dict['to'] or ''),
            utils.parse_as_int(tx_dict['value']),
            utils.decode_hex(tx_dict['input']),
            utils.parse_as_int(tx_dict['v']),
            utils.bytes_to_int(normalize_bytes(tx_dict['r'])),
            utils.bytes_to_int(normalize_bytes(tx_dict['s'])),
        )
        if normalize_bytes(tx_dict['hash']) != t.hash:
            print("False transaction hash")
            return None
        return rlp.encode(t)

    @staticmethod
    def get_node_type(node):
        if node == BLANK_NODE:
            return NODE_TYPE_BLANK
        elif len(node) == 2:
            key, _ = node
            nibbles = decode_nibbles(key)
            if is_nibbles_terminated(nibbles):
                return NODE_TYPE_LEAF
            else:
                return NODE_TYPE_EXTENSION
        elif len(node) == 17:
            return NODE_TYPE_BRANCH
        else:
            raise InvalidNode("Unable to determine node type")

    @staticmethod
    def generate_proof(mpt, mpt_key_nibbles: bytes):
        if not all(0 <= nibble < 16 for nibble in mpt_key_nibbles):
            raise ValueError("mpt_key_nibbles has non-nibble elements {}".format(str(mpt_key_nibbles)))
        stack_indexes = []
        stack = []

        def aux(node_hash, mpt_key_nibbles):
            nonlocal stack_indexes
            nonlocal stack

            node = mpt.get_node(node_hash)
            if get_node_type(node) == NODE_TYPE_BLANK:
                return
            elif get_node_type(node) == NODE_TYPE_BRANCH:
                if mpt_key_nibbles:
                    i = mpt_key_nibbles[0]
                    stack_indexes.append(i)
                    stack.append(node)
                    aux(node[i], mpt_key_nibbles[1:])
                else:
                    i = 16
                    stack_indexes.append(i)
                    stack.append(node)
            elif get_node_type(node) in [NODE_TYPE_EXTENSION, NODE_TYPE_LEAF]:
                key = extract_key(node)
                prefix, key_remainder, mpt_key_nibbles_remainder = \
                    consume_common_prefix(key, mpt_key_nibbles)
                if not key_remainder:
                    stack_indexes.append(1)
                    stack.append(node)
                    if get_node_type(node) == NODE_TYPE_EXTENSION:
                        aux(node[1], mpt_key_nibbles_remainder)
                else:
                    stack_indexes.append(0xff)
                    stack.append(node)
            else:
                raise ValueError("Unknown node type: {}".format(
                    get_node_type(node)))

        root_node = mpt.get_node(mpt.root_hash)
        if get_node_type(root_node) != NODE_TYPE_BLANK:
            aux(mpt.root_hash, mpt_key_nibbles)
        return stack


if __name__ == "__main__":
    verifier = Verifier("http://192.168.11.57:8545")
    verifier.verify_transaction("0xdc369d8038adedea391c91d4e3516a4eebb393842157fed25f02b11f1204510a")
