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

prefix = "PPY1"
wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"
ref_block_num = 34294
ref_block_prefix = 3707022213
expiration = "2016-04-06T08:29:27"


class Testcases(unittest.TestCase):

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
        op = operations.Transfer(**{
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
            "prefix": prefix
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

    def test_create_account(self):
        s = {"fee": {"amount": 1467634,
                     "asset_id": "1.3.0"
                     },
             "registrar": "1.2.33",
             "referrer": "1.2.27",
             "referrer_percent": 3,
             "name": "foobar-f124",
             "owner": {"weight_threshold": 1,
                       "account_auths": [],
                       'key_auths': [[prefix + '6pbVDAjRFiw6fkiKYCrkz7PFeL7XNAfefrsREwg8MKpJ9VYV9x',
                                     1], [
                                     prefix + '6zLNtyFVToBsBZDsgMhgjpwysYVbsQD6YhP3kRkQhANUB4w7Qp',
                                     1]],
                       "address_auths": []
                       },
             "active": {"weight_threshold": 1,
                        "account_auths": [],
                        'key_auths': [[prefix + '6pbVDAjRFiw6fkiKYCrkz7PFeL7XNAfefrsREwg8MKpJ9VYV9x',
                                       1], [
                                      prefix + '6zLNtyFVToBsBZDsgMhgjpwysYVbsQD6YhP3kRkQhANUB4w7Qp',
                                      1], [
                                      prefix + '8CemMDjdUWSV5wKotEimhK6c4dY7p2PdzC2qM1HpAP8aLtZfE7',
                                      1
                                      ]],
                        "address_auths": []
                        },
             "options": {"memo_key": prefix + '5TPTziKkLexhVKsQKtSpo4bAv5RnB8oXcG4sMHEwCcTf3r7dqE',
                         "voting_account": "1.2.5",
                         "num_witness": 0,
                         "num_committee": 0,
                         "votes": [],
                         "extensions": []
                         },
             "extensions": {},
             "prefix": prefix
             }
        op = operations.Account_create(**s)
        ops = [Operation(op)]
        tx = Signed_Transaction(ref_block_num=ref_block_num,
                                ref_block_prefix=ref_block_prefix,
                                expiration=expiration,
                                operations=ops)
        tx = tx.sign([wif], chain=prefix)
        tx.verify([PrivateKey(wif).pubkey], prefix)
        txWire = hexlify(bytes(tx)).decode("ascii")
        compare = ("f68585abf4dce7c804570105f26416000000000000211b03000b666f"
                   "6f6261722d6631323401000000000202fe8cc11cc8251de6977636b5"
                   "5c1ab8a9d12b0b26154ac78e56e7c4257d8bcf6901000314aa202c91"
                   "58990b3ec51a1aa49b2ab5d300c97b391df3beb34bb74f3c62699e01"
                   "000001000000000303b453f46013fdbccb90b09ba169c388c34d8445"
                   "4a3b9fbec68d5a7819a734fca0010002fe8cc11cc8251de6977636b5"
                   "5c1ab8a9d12b0b26154ac78e56e7c4257d8bcf6901000314aa202c91"
                   "58990b3ec51a1aa49b2ab5d300c97b391df3beb34bb74f3c62699e01"
                   "0000024ab336b4b14ba6d881675d1c782912783c43dbbe31693aa710"
                   "ac1896bd7c3d61050000000000000000011f61ad276120bc3f189296"
                   "2bfff7db5e8ce04d5adec9309c80529e3a978a4fa1073225a6d56929"
                   "e34c9d2a563e67a8f4a227e4fadb4a3bb6ec91bfdf4e57b80efd")
        self.assertEqual(compare[:-130], txWire[:-130])

    def test_upgrade_account(self):
        op = operations.Account_upgrade(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "account_to_upgrade": "1.2.0",
            "upgrade_to_lifetime_member": True,
            "prefix": prefix,
        })
        ops = [Operation(op)]
        tx = Signed_Transaction(ref_block_num=ref_block_num,
                                ref_block_prefix=ref_block_prefix,
                                expiration=expiration,
                                operations=ops)
        tx = tx.sign([wif], chain=prefix)
        tx.verify([PrivateKey(wif).pubkey], prefix)
        txWire = hexlify(bytes(tx)).decode("ascii")
        compare = ("f68585abf4dce7c804570108000000000000000000000100000"
                   "11f4e42562ada1d3fed8f8eb51dd58117e3a4024959c46955a0"
                   "0d2a7e7e8b40ae7204f4617913aaaf028248d43e8c3463b8776"
                   "0ca569007dba99a2c49de75bd69b3")
        self.assertEqual(compare[:-130], txWire[:-130])

    def test_proposal_update(self):
        op = operations.Proposal_update(**{
            'fee_paying_account': "1.2.1",
            'proposal': "1.10.90",
            'active_approvals_to_add': ["1.2.5"],
            "fee": {"amount": 0, "asset_id": "1.3.0"},
        })
        ops = [Operation(op)]
        tx = Signed_Transaction(ref_block_num=ref_block_num,
                                ref_block_prefix=ref_block_prefix,
                                expiration=expiration,
                                operations=ops)
        tx = tx.sign([wif], chain=prefix)
        tx.verify([PrivateKey(wif).pubkey], prefix)
        txWire = hexlify(bytes(tx)).decode("ascii")
        compare = ("f68585abf4dce7c804570117000000000000000000015a01050000000"
                   "000000001200b28528d1436564f4b4a9faf38b77c17d69ea85476076e"
                   "bafebbad9733ac014411b044a7570ef103a518d2e17f7250e1cd8e31c"
                   "f19272395c8fe9bbce0b4bfb4")
        self.assertEqual(compare[:-130], txWire[:-130])

    def test_create_proposal(self):
        op = operations.Proposal_create(**{
            "fee": {"amount": 0,
                    "asset_id": "1.3.0"
                    },
            "fee_paying_account": "1.2.0",
            "expiration_time": "1970-01-01T00:00:00",
            "proposed_ops": [{
                "op": [
                    0, {"fee": {"amount": 0,
                                "asset_id": "1.3.0"
                                },
                        "from": "1.2.0",
                        "to": "1.2.0",
                        "amount": {"amount": 0,
                                   "asset_id": "1.3.0"
                                   },
                        "extensions": []}]}],
            "extensions": []
        })
        ops = [Operation(op)]
        tx = Signed_Transaction(ref_block_num=ref_block_num,
                                ref_block_prefix=ref_block_prefix,
                                expiration=expiration,
                                operations=ops)
        tx = tx.sign([wif], chain=prefix)
        tx.verify([PrivateKey(wif).pubkey], prefix)
        txWire = hexlify(bytes(tx)).decode("ascii")
        compare = ("f68585abf4dce7c80457011600000000000000000000000000"
                   "00010000000000000000000000000000000000000000000000"
                   "00000001204baf7f11a7ff12337fc097ac6e82e7b68f82f02c"
                   "c7e24231637c88a91ae5716674acec8a1a305073165c65e520"
                   "a64769f5f62c0301ce21ab4f7c67a6801b4266")
        self.assertEqual(compare[:-130], txWire[:-130])

    def test_sport_create(self):
        op = operations.Sport_create(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "name": [["en", "Football"], ["de", "Fußball"]],
            "prefix": prefix,
        })
        ops = [Operation(op)]
        tx = Signed_Transaction(ref_block_num=ref_block_num,
                                ref_block_prefix=ref_block_prefix,
                                expiration=expiration,
                                operations=ops)
        tx = tx.sign([wif], chain=prefix)
        tx.verify([PrivateKey(wif).pubkey], prefix)
        txWire = hexlify(bytes(tx)).decode("ascii")
        compare = ("f68585abf4dce7c80457012d000000000000000000020264650"
                   "84675c39f62616c6c02656e08466f6f7462616c6c0000011f14"
                   "eb892a0c4a6c28e0a54852d45526b0d8e017edc4eaac1c0c54c"
                   "6f944ff1d7e5e909157257fe6e71a4532563564c8c063f38846"
                   "5f8a9420459d5b6cb1fdfcc1")
        self.assertEqual(compare[:-130], txWire[:-130])

    def test_competitor_create(self):
        op = operations.Competitor_create(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "name": [["en", "Fuerth"], ["de", "Greuther Fürth"]],
            "sport_id": "1.0.1241",
            "prefix": prefix,
        })
        ops = [Operation(op)]
        tx = Signed_Transaction(ref_block_num=ref_block_num,
                                ref_block_prefix=ref_block_prefix,
                                expiration=expiration,
                                operations=ops)
        tx = tx.sign([wif], chain=prefix)
        tx.verify([PrivateKey(wif).pubkey], prefix)
        txWire = hexlify(bytes(tx)).decode("ascii")
        compare = ("f68585abf4dce7c80457012e000000000000000000020264"
                   "650f47726575746865722046c3bc72746802656e06467565"
                   "727468d9040000000000010000012068e0417811ad383306"
                   "1dde84281b17daf22e8dfe879506ee06eb6d9c324297a811"
                   "e04fa8e5983001bb7eee47d3e9fd0e7c48590c10abfa6a6f"
                   "2a33ed50a2d424")
        self.assertEqual(compare[:-130], txWire[:-130])

    def test_event_group_create(self):
        op = operations.Event_group_create(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "name": [["en", "NHL"], ["zh_Hans", "國家冰球聯盟"]],
            "sport_id": "1.0.1241",
            "prefix": prefix,
        })
        ops = [Operation(op)]
        tx = Signed_Transaction(ref_block_num=ref_block_num,
                                ref_block_prefix=ref_block_prefix,
                                expiration=expiration,
                                operations=ops)
        tx = tx.sign([wif], chain=prefix)
        tx.verify([PrivateKey(wif).pubkey], prefix)
        txWire = hexlify(bytes(tx)).decode("ascii")
        compare = ("f68585abf4dce7c80457012f000000000000000000020265"
                   "6e034e484c077a685f48616e7312e59c8be5aeb6e586b0e7"
                   "9083e881afe79b9fd9040000000000010000011f15a6cb74"
                   "7df1d9bb3e7e607d8094624b3f27010ad461dd8d833590b0"
                   "e0f72c946082083f90686e9bc225f5b28fd50c63c8150b8c"
                   "45956c336a182702e17d800d")
        self.assertEqual(compare[:-130], txWire[:-130])

    def test_event_create(self):
        op = operations.Event_create(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "season": [["en", "2016-17"]],
            "start_time": "2017-03-29T09:15:05",
            "event_group_id": "1.0.1241",
            "competitors": ["0.0.0", "0.0.1"],
            "prefix": prefix,
        })
        ops = [Operation(op)]
        tx = Signed_Transaction(ref_block_num=ref_block_num,
                                ref_block_prefix=ref_block_prefix,
                                expiration=expiration,
                                operations=ops)
        tx = tx.sign([wif], chain=prefix)
        tx.verify([PrivateKey(wif).pubkey], prefix)
        txWire = hexlify(bytes(tx)).decode("ascii")
        compare = ("f68585abf4dce7c8045701300000000000000000000001026"
                   "56e07323031362d313701197bdb58d9040000000000010200"
                   "0000000000000001000000000000000000011f2f6eccc426e"
                   "56925b29293610505598a8580dc56fc594fef541d25a7cfc8"
                   "120d7b82dc6fb929bd6bb1fb8f2ab976559ea29c9adc7a9b5"
                   "df9788b909c7fafe232")
        self.assertEqual(compare[:-130], txWire[:-130])

    def test_betting_market_group_create(self):
        op = operations.Betting_market_group_create(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "event_id": "1.0.1241",
            "options": [2, {"score": 100}],
            "prefix": prefix,
        })
        ops = [Operation(op)]
        tx = Signed_Transaction(ref_block_num=ref_block_num,
                                ref_block_prefix=ref_block_prefix,
                                expiration=expiration,
                                operations=ops)
        tx = tx.sign([wif], chain=prefix)
        tx.verify([PrivateKey(wif).pubkey], prefix)
        txWire = hexlify(bytes(tx)).decode("ascii")
        compare = ("f68585abf4dce7c804570131000000000000000000d904000"
                   "0000000010264000000000001206e69065a3cd673843f4a66"
                   "000d7143b2a10f27015d4c49600ffb5c94f6fc95fe40f3577"
                   "264b9288b44e4fe3e0aa5397d1c7973054cc55c6bb611c23b"
                   "397f5bb0")
        self.assertEqual(compare[:-130], txWire[:-130])

    def test_betting_market_create(self):
        op = operations.Betting_market_create(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "group_id": "1.0.1241",
            "payout_condition": [["en", "Foo == Bar"], ["zh_Hans", "Foo == Bar"]],
            "asset_id": "1.3.10",
            "prefix": prefix,
        })
        ops = [Operation(op)]
        tx = Signed_Transaction(ref_block_num=ref_block_num,
                                ref_block_prefix=ref_block_prefix,
                                expiration=expiration,
                                operations=ops)
        tx = tx.sign([wif], chain=prefix)
        tx.verify([PrivateKey(wif).pubkey], prefix)
        txWire = hexlify(bytes(tx)).decode("ascii")
        compare = ("f68585abf4dce7c804570132000000000000000000d904"
                   "0000000000010202656e0a466f6f203d3d20426172077a"
                   "685f48616e730a466f6f203d3d204261720a0000011f33"
                   "a517c8eec3f3d8eaf9653d96037bed0feb3ae6496a6fde"
                   "201816de06187fb4768be89dc7092626b816440f41d7b0"
                   "92be3cc1b54eb340868a0638ddd93b4448")
        self.assertEqual(compare[:-130], txWire[:-130])

    def test_bet_place(self):
        op = operations.Bet_place(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "bettor_id": "1.2.1241",
            "betting_market_id": "1.21.1",
            "amount_to_bet": 100000,
            "amount_to_win": 20000,
            "amount_reserved_for_fees": 100000,
            "back_or_lay": "back",
            "prefix": prefix,
        })
        ops = [Operation(op)]
        tx = Signed_Transaction(ref_block_num=ref_block_num,
                                ref_block_prefix=ref_block_prefix,
                                expiration=expiration,
                                operations=ops)
        tx = tx.sign([wif], chain=prefix)
        tx.verify([PrivateKey(wif).pubkey], prefix)
        txWire = hexlify(bytes(tx)).decode("ascii")
        compare = ("f68585abf4dce7c804570133000000000000000000d909"
                   "01a086010000000000204e000000000000a08601000000"
                   "0000000000011f0fcb636b68993dde7b680f9b34ea375e"
                   "2790b1b6a43621e2048712f21d2868fd553851b5254b5e"
                   "a2d4995e535813a4d8f76b18bb62ad2722a4b2bb83558c"
                   "55e0")
        self.assertEqual(compare[:-130], txWire[:-130])

    def compareConstructedTX(self):
        op = operations.Proposal_update(**{
            'fee_paying_account': "1.2.1",
            'proposal': "1.10.90",
            'active_approvals_to_add': ["1.2.5"],
            "fee": {"amount": 0, "asset_id": "1.3.0"},
        })
        """
        op = operations.Betting_market_resolve(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "betting_market_id": "1.21.1",
            "resolution": "win",
            "prefix": prefix,
        })
        op = operations.Bet_cancel_operation(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "bettor_id": "1.2.1241",
            "bet_to_cancel": "1.22.10",
            "prefix": prefix,
        })
        """
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
