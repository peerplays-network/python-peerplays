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
GRAPHENE_BETTING_ODDS_PRECISION = 10000


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
        compare = ("f68585abf4dce7c80457012f000000000000000000020264650"
                   "84675c39f62616c6c02656e08466f6f7462616c6c0000011f73"
                   "9bf27286518931950b40ee739e34972bda63a44e3a7901e6686"
                   "7b505f8122f2c9a47df242aad5e3630a5add2ea3aea8e62a92b"
                   "8f2247c05033e8f40eb1836e")
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
        compare = ("f68585abf4dce7c804570131000000000000000000020265"
                   "6e034e484c077a685f48616e7312e59c8be5aeb6e586b0e7"
                   "9083e881afe79b9fd9040000000000010000011f2e739264"
                   "8b843f756c8773a984cb2b218a39558cb7415bf7abc6168a"
                   "2a30336e65a5fe70fa63e6b870e18e2f9e1a8dcc96070e75"
                   "a3e28f9c474e651c5860cea7")
        self.assertEqual(compare[:-130], txWire[:-130])

    def test_event_create(self):
        op = operations.Event_create(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "season": [["en", "2016-17"]],
            "start_time": "2017-03-29T09:15:05",
            "event_group_id": "1.0.1241",
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
        compare = ("f68585abf4dce7c8045701330000000000000000000001026"
                   "56e07323031362d313701197bdb58d9040000000000010000"
                   "012001ef3b40d64a3e82c0b4b35586c708c2d8521918ec4bb"
                   "bc9db7ed395c5a619a953d59f1bc8cc7efa19d12acd69a6f5"
                   "abd57a7cfe95fe9f3468329d7f2fabecd7")
        self.assertEqual(compare[:-130], txWire[:-130])

    def test_betting_market_rules_create(self):
        op = operations.Betting_market_rules_create(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "name": [["en", "NHL Rules v1.0"]],
            "description": [["en", "The winner will be the team with the most points at the end of the game.  The team with fewer points will not be the winner."]],
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
        compare = ("f68585abf4dce7c8045701350000000000000000000102656"
                   "e0e4e484c2052756c65732076312e300102656e7c54686520"
                   "77696e6e65722077696c6c20626520746865207465616d207"
                   "769746820746865206d6f737420706f696e74732061742074"
                   "686520656e64206f66207468652067616d652e20205468652"
                   "07465616d207769746820666577657220706f696e74732077"
                   "696c6c206e6f74206265207468652077696e6e65722e00000"
                   "1204ae5e65355fe4f364de07f09b1858a560d8e4549c1228b"
                   "ac9a31815063d7c1531b374a668a385cfe2154e0d4c1d42de"
                   "0afe8fe3a56fef5b0d4e1f6fd660f8954")
        self.assertEqual(compare[:-130], txWire[:-130])

    #####################
    def test_betting_market_group_create(self):
        op = operations.Betting_market_group_create(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "description": [["en", "Football"], ["de", "Fußball"]],
            "event_id": "1.0.1241",
            "rules_id": "1.22.11",
            "asset_id": "1.3.124",
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
        compare = ("f68585abf4dce7c8045701370000000000000000000202646"
                   "5084675c39f62616c6c02656e08466f6f7462616c6cd90400"
                   "00000000010b000000000016017c0000011f2603de0504424"
                   "dfab0b120e4a258ffe15ee5be333ce8e1404986ea10f1d28e"
                   "e033ae6b3d2eea9202b4a18bf3e3bff6ae5ddfe3b4b9d7713"
                   "fb2ec11f123eaaa39")
        self.assertEqual(compare[:-130], txWire[:-130])

    def test_betting_market_create(self):
        op = operations.Betting_market_create(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "group_id": "1.0.1241",
            "payout_condition": [["en", "Foo == Bar"], ["zh_Hans", "Foo == Bar"]],
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
        compare = ("f68585abf4dce7c804570138000000000000000000d904"
                   "0000000000010202656e0a466f6f203d3d20426172077a"
                   "685f48616e730a466f6f203d3d204261720000011f294a"
                   "2cf8976fe5def4365aa671ca65131a6177789c3c21549f"
                   "ae80302a10a0f35968b7e9f2894d825d818f47b396365c"
                   "f5083c2bcf60949767e054ff2efc0147")
        self.assertEqual(compare[:-130], txWire[:-130])

    def test_betting_market_group_resolve(self):
        op = operations.Betting_market_group_resolve(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "betting_market_group_id": "1.20.1024",
            "resolutions": [
                ["1.21.257", "cancel"],
                ["1.21.256", "cancel"],
            ],
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
        compare = ("f68585abf4dce7c80457013a00000000000000000080080"
                   "28002020000000000000081020200000000000000000001"
                   "1f734163cbe9ae3a81bffcf81d94bf71890f744f99e5184"
                   "1ad7c46063cd661b0717eaaa6415890a56e731c1dd38e96"
                   "c6983f63999e95ec7be1a4926b526177a986")
        self.assertEqual(compare[:-130], txWire[:-130])

    def test_betting_market_group_freeze(self):
        op = operations.Betting_market_group_freeze(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "betting_market_group_id": "1.20.1024",
            "freeze": False,
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
        compare = ("f68585abf4dce7c80457013c0000000000000000008008"
                   "00000001202b5b29f8307788bc8975ef72c46a848ccb6c"
                   "643f88e1809ca700fc7a9ac5bd6204b95e2648339857e6"
                   "9bdb2899e56a9c71dcb3fa5ba3a6baf3d4e225dc5da507")
        self.assertEqual(compare[:-130], txWire[:-130])

    def test_bet_place(self):
        op = operations.Bet_place(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "bettor_id": "1.2.1241",
            "betting_market_id": "1.21.1",
            "amount_to_bet": {"amount": 1000, "asset_id": "1.3.1"},
            "backer_multiplier": 2 * GRAPHENE_BETTING_ODDS_PRECISION,
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
        compare = ("f68585abf4dce7c804570139000000000000000000d909"
                   "01e80300000000000001204e0000a08601000000000000"
                   "000000000000000000011f6436844f2f4d317176e064e6"
                   "4f32d558420ac191193b4425bf215bdb97de807e77743a"
                   "c412e977ba2196a71c11b313eb898b42429af1fcc96096"
                   "16504008794e")
        self.assertEqual(compare[:-130], txWire[:-130])

    def test_bet_cancel(self):
        op = operations.Bet_cancel(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "bettor_id": "1.2.5555",
            "bet_to_cancel": "1.22.1111",
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
        compare = ("f68585abf4dce7c80457013f000000000000000000b32bd70800"
                   "0001201d84eb0e1b0e4490119bd1cc17f7ab0a648ac00c50a36e"
                   "f3b0d7e12012c8ed0f78c7acad5701d9a0df58e38e33d896bad5"
                   "fc68a0f59f2f9b591062a194049518")
        self.assertEqual(compare[:-130], txWire[:-130])

    def compareConstructedTX(self):
        op = operations.Betting_market_rules_create(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "name": [["en", "NHL Rules v1.0"]],
            "description": [["en", "The winner will be the team with the most points at the end of the game.  The team with fewer points will not be the winner."]],
            "prefix": prefix,
        })
        ops = [Operation(op)]

        """
        from peerplays import PeerPlays
        ppy = PeerPlays()
        ops = transactions.addRequiredFees(ppy.rpc, ops)
        """
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
        print("soll: %s" % compare[:-130])
        print("ist:  %s" % txWire[:-130])
        print(txWire[:-130] == compare[:-130])
        self.assertEqual(compare[:-130], txWire[:-130])


if __name__ == '__main__':
    t = Testcases()
    t.compareConstructedTX()
