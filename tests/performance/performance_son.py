#!/usr/bin/env python
# -*- coding: utf-8 -*-

import multiprocessing
import time
import random


from binascii import hexlify
from pprint import pprint

from peerplaysbase import memo, account, operations, objects
from peerplaysbase.account import PrivateKey, PublicKey
from peerplaysbase.objects import Operation
from peerplaysbase.signedtransactions import Signed_Transaction
# from tests.fixtures import peerplays
from peerplays import PeerPlays

TEST_AGAINST_CLI_WALLET = False

prefix = "TEST"
wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"
ref_block_num = 34294
ref_block_prefix = 3707022213
expiration = "2016-04-06T08:29:27"
GRAPHENE_BETTING_ODDS_PRECISION = 10000
# peerplays.blocking = True

wifs = [
    "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3",
    "5KCBDTcyDqzsqehcb52tW5nU6pXife6V2rX9Yf7c3saYSzbDZ5W",
]
wif = wifs[0]
core_unit = "TEST"

class Testcases():
    def doit(self, printWire=False):
        ops = [Operation(self.op)]
        tx = Signed_Transaction(
            ref_block_num=ref_block_num,
            ref_block_prefix=ref_block_prefix,
            expiration=expiration,
            operations=ops,
        )
        tx = tx.sign([wif], chain=prefix)
        tx.verify([PrivateKey(wif).pubkey], prefix)
        txWire = hexlify(bytes(tx)).decode("ascii")
        if printWire:
            print()
            print(txWire)
            print()
        self.assertEqual(self.cm[:-130], txWire[:-130])

        if TEST_AGAINST_CLI_WALLET:
            from grapheneapi.grapheneapi import GrapheneAPI

            rpc = GrapheneAPI("localhost", 8092)
            self.cm = rpc.serialize_transaction(tx.json())
            # print("soll: %s" % self.cm[:-130])
            # print("ist:  %s" % txWire[:-130])
            # print(txWire[:-130] == self.cm[:-130])
            self.assertEqual(self.cm[:-130], txWire[:-130])

        # Test against Bitshares backened
        live = peerplays.rpc.get_transaction_hex(tx.json())

        # Compare expected result with online result
        self.assertEqual(live[:-130], txWire[:-130])

        # Compare expected result with online backend
        self.assertEqual(live[:-130], self.cm[:-130])

    def test_Transfer(self):
        pub = format(account.PrivateKey(wif).pubkey, prefix)
        from_account_id = "1.2.0"
        to_account_id = "1.2.1"
        amount = 1000000
        asset_id = "1.3.4"
        message = "abcdefgABCDEFG0123456789"
        nonce = "5862723643998573708"

        fee = objects.Asset(amount=0, asset_id="1.3.0")
        amount = objects.Asset(amount=int(amount), asset_id=asset_id)
        encrypted_memo = memo.encode_memo(
            account.PrivateKey(wif),
            account.PublicKey(pub, prefix=prefix),
            nonce,
            message,
        )
        self.op = operations.Transfer(
            **{
                "fee": fee,
                "from": from_account_id,
                "to": to_account_id,
                "amount": amount,
                "memo": {
                    "from": pub,
                    "to": pub,
                    "nonce": nonce,
                    "message": encrypted_memo,
                },
                "prefix": prefix,
            }
        )
        self.cm = (
            "f68585abf4dce7c804570100000000000000000000000140420"
            "f0000000000040102c0ded2bc1f1305fb0faac5e6c03ee3a192"
            "4234985427b6167ca569d13df435cf02c0ded2bc1f1305fb0fa"
            "ac5e6c03ee3a1924234985427b6167ca569d13df435cf8c94d1"
            "9817945c5120fa5b6e83079a878e499e2e52a76a7739e9de409"
            "86a8e3bd8a68ce316cee50b210000011f39e3fa7071b795491e"
            "3b6851d61e7c959be92cc7deb5d8491cf1c3c8c99a1eb44553c"
            "348fb8f5001a78b18233ac66727e32fc776d48e92d9639d64f6"
            "8e641948"
        )
        self.doit()

    def transfer_On_Chain(self):
        from tests.fixtures import peerplays as pp

        pp = PeerPlays(
            "ws://10.11.12.101:8090", keys=wifs, nobroadcast=False, num_retries=1, blocking=False
            # "wss://api.ppy-beatrice.blckchnd.com", keys=wifs, nobroadcast=True, num_retries=1
            # "wss://elizabeth.peerplays.download/api", keys=wifs, nobroadcast=False, num_retries=1, blocking=True
            # "wss://irona.peerplays.download/api", keys=wifs, nobroadcast=False, num_retries=1, blocking=True
            # "wss://fred.peerplays.download/api", keys=wifs, nobroadcast=False, num_retries=1, blocking=True
            # "wss://hercules.peerplays.download/api", keys=wifs, nobroadcast=False, num_retries=1, blocking=True
            )
        pp.transfer ("1.2.9", 1, "TEST", memo="", account="1.2.8") #, blocking=False) 
        print("transfer done")
        # time.sleep(6)
        # pp.close()

testcases = Testcases()

def task(x):
    print("   ")
    # rand = random.randint(1000,2000)
    rand = x
    print("-------------", rand, "------------------", "Started")
    # time.sleep(1)
    testcases.transfer_On_Chain()
    print(rand, "Done")
    print("------------------------------", rand, "---------------", "Ended")
    print ("   ") 
    return x

if __name__ == "__main__":
    # pool = multiprocessing.pool.Pool()
    countTask = 2
    p = multiprocessing.Pool(countTask)
    tic = time.time()
    p.map(task, range(countTask))
    toc = time.time()

    timePerTask = (toc - tic) / countTask 

    print("timePerTask:", timePerTask)

