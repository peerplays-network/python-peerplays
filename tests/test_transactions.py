from peerplaysbase import (
    transactions,
    memo,
    account,
    operations,
    objects
)
from peerplaysbase.objects import Operation
from peerplaysbase.signedtransactions import Signed_Transaction
from peerplaysbase.account import PrivateKey
import random
import unittest
from pprint import pprint
from binascii import hexlify

prefix = "PPY"
wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"
ref_block_num = 34294
ref_block_prefix = 3707022213
expiration = "2016-04-06T08:29:27"


class Testcases(unittest.TestCase):

    def test_call_update(self):
            pass

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
            message
        )
        memoStruct = {
            "from": pub,
            "to": pub,
            "nonce": nonce,
            "message": encrypted_memo,
            "chain": prefix
        }
        memoObj = objects.Memo(**memoStruct)
        op = operations.Transfer(**{
            "fee": fee,
            "from": from_account_id,
            "to": to_account_id,
            "amount": amount,
            "memo": memoObj
        })
        ops = [Operation(op)]
        tx = Signed_Transaction(ref_block_num=ref_block_num,
                                ref_block_prefix=ref_block_prefix,
                                expiration=expiration,
                                operations=ops)
        tx = tx.sign([wif], chain=prefix)
        tx.verify([PrivateKey(wif).pubkey], prefix)
        txWire = hexlify(bytes(tx)).decode("ascii")

        compare = ("f68585abf4dce7c804570100000000000000000000000140420"
                   "f0000000000040102c0ded2bc1f1305fb0faac5e6c03ee3a192"
                   "4234985427b6167ca569d13df435cf02c0ded2bc1f1305fb0fa"
                   "ac5e6c03ee3a1924234985427b6167ca569d13df435cf8c94d1"
                   "9817945c5120fa5b6e83079a878e499e2e52a76a7739e9de409"
                   "86a8e3bd8a68ce316cee50b210000011f39e3fa7071b795491e"
                   "3b6851d61e7c959be92cc7deb5d8491cf1c3c8c99a1eb44553c"
                   "348fb8f5001a78b18233ac66727e32fc776d48e92d9639d64f6"
                   "8e641948")
        self.assertEqual(compare[:-130], txWire[:-130])

    def compareConstructedTX(self):
        op = operations.Operations(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "vesting_balance": "1.13.0",
            "owner": "1.2.0",
            "amount": {"amount": 0, "asset_id": "1.3.0"},
            "prefix": prefix,
        })
        ops = [Operation(op)]
        tx = Signed_Transaction(
            ref_block_num=ref_block_num,
            ref_block_prefix=ref_block_prefix,
            expiration=expiration,
            operations=ops
        )
        tx = tx.sign([wif], chain=prefix)
        tx.verify([PrivateKey(wif).pubkey], prefix)
        txWire = hexlify(bytes(tx)).decode("ascii")
        print("=" * 80)
        pprint(tx.json())
        print("=" * 80)

        from grapheneapi.grapheneapi import GrapheneAPI
        rpc = GrapheneAPI("localhost", 8092)
        compare = rpc.serialize_transaction(tx.json())
        print(compare[:-130])
        print(txWire[:-130])
        print(txWire[:-130] == compare[:-130])
        self.assertEqual(compare[:-130], txWire[:-130])


if __name__ == '__main__':
    t = Testcases()
    t.compareConstructedTX()
