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

TEST_AGAINST_CLI_WALLET = False

prefix = "PPY"
wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"
ref_block_num = 34294
ref_block_prefix = 3707022213
expiration = "2016-04-06T08:29:27"
GRAPHENE_BETTING_ODDS_PRECISION = 10000


class Testcases(unittest.TestCase):

    def doit(self, printWire=False):
        ops = [Operation(self.op)]
        tx = Signed_Transaction(ref_block_num=ref_block_num,
                                ref_block_prefix=ref_block_prefix,
                                expiration=expiration,
                                operations=ops)
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
        self.op = operations.Transfer(**{
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
        self.cm = ("f68585abf4dce7c804570100000000000000000000000140420"
                   "f0000000000040102c0ded2bc1f1305fb0faac5e6c03ee3a192"
                   "4234985427b6167ca569d13df435cf02c0ded2bc1f1305fb0fa"
                   "ac5e6c03ee3a1924234985427b6167ca569d13df435cf8c94d1"
                   "9817945c5120fa5b6e83079a878e499e2e52a76a7739e9de409"
                   "86a8e3bd8a68ce316cee50b210000011f39e3fa7071b795491e"
                   "3b6851d61e7c959be92cc7deb5d8491cf1c3c8c99a1eb44553c"
                   "348fb8f5001a78b18233ac66727e32fc776d48e92d9639d64f6"
                   "8e641948")
        self.doit()

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
        self.op = operations.Account_create(**s)
        self.cm = ("f68585abf4dce7c804570105f26416000000000000211b03000b666f"
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
        self.doit()

    def test_upgrade_account(self):
        self.op = operations.Account_upgrade(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "account_to_upgrade": "1.2.0",
            "upgrade_to_lifetime_member": True,
            "prefix": prefix,
        })
        self.cm = ("f68585abf4dce7c804570108000000000000000000000100000"
                   "11f4e42562ada1d3fed8f8eb51dd58117e3a4024959c46955a0"
                   "0d2a7e7e8b40ae7204f4617913aaaf028248d43e8c3463b8776"
                   "0ca569007dba99a2c49de75bd69b3")
        self.doit()

    def test_proposal_update(self):
        self.op = operations.Proposal_update(**{
            'fee_paying_account': "1.2.1",
            'proposal': "1.10.90",
            'active_approvals_to_add': ["1.2.5"],
            "fee": {"amount": 0, "asset_id": "1.3.0"},
        })
        self.cm = ("f68585abf4dce7c804570117000000000000000000015a01050000000"
                   "000000001200b28528d1436564f4b4a9faf38b77c17d69ea85476076e"
                   "bafebbad9733ac014411b044a7570ef103a518d2e17f7250e1cd8e31c"
                   "f19272395c8fe9bbce0b4bfb4")
        self.doit()

    def test_create_proposal(self):
        self.op = operations.Proposal_create(**{
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
        self.cm = ("f68585abf4dce7c80457011600000000000000000000000000"
                   "00010000000000000000000000000000000000000000000000"
                   "00000001204baf7f11a7ff12337fc097ac6e82e7b68f82f02c"
                   "c7e24231637c88a91ae5716674acec8a1a305073165c65e520"
                   "a64769f5f62c0301ce21ab4f7c67a6801b4266")
        self.doit()

    def test_sport_create(self):
        self.op = operations.Sport_create(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "name": [["en", "Football"], ["de", "Fußball"]],
            "prefix": prefix,
        })
        self.cm = ("f68585abf4dce7c80457012f000000000000000000020264650"
                   "84675c39f62616c6c02656e08466f6f7462616c6c0000011f73"
                   "9bf27286518931950b40ee739e34972bda63a44e3a7901e6686"
                   "7b505f8122f2c9a47df242aad5e3630a5add2ea3aea8e62a92b"
                   "8f2247c05033e8f40eb1836e")
        self.doit()

    def test_event_group_create(self):
        self.op = operations.Event_group_create(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "name": [["en", "NHL"], ["zh_Hans", "國家冰球聯盟"]],
            "sport_id": "1.0.1241",
            "prefix": prefix,
        })
        self.cm = ("f68585abf4dce7c804570131000000000000000000020265"
                   "6e034e484c077a685f48616e7312e59c8be5aeb6e586b0e7"
                   "9083e881afe79b9fd9040000000000010000011f2e739264"
                   "8b843f756c8773a984cb2b218a39558cb7415bf7abc6168a"
                   "2a30336e65a5fe70fa63e6b870e18e2f9e1a8dcc96070e75"
                   "a3e28f9c474e651c5860cea7")
        self.doit()

    def test_event_create(self):
        self.op = operations.Event_create(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "name": [["en", "My Event name"]],
            "season": [["en", "2016-17"]],
            "start_time": "2017-03-29T09:15:05",
            "event_group_id": "1.0.1241",
            "prefix": prefix,
        })
        self.cm = ("f68585abf4dce7c8045701330000000000000000000102656"
                   "e0d4d79204576656e74206e616d650102656e07323031362d"
                   "313701197bdb58d9040000000000010000011f22c306e6b51"
                   "0a66a1f1bf1acb537360a5d2d0f7b788f9da359b451ffc676"
                   "54cb594144f23476c71d6caeb94162237de346abc485d1096"
                   "86d17a55e9e9992439a")
        self.doit()

    def test_betting_market_rules_create(self):
        self.op = operations.Betting_market_rules_create(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "name": [["en", "NHL Rules v1.0"]],
            "description": [["en", "The winner will be the team with the most points at the end of the game.  The team with fewer points will not be the winner."]],
            "prefix": prefix,
        })
        self.cm = ("f68585abf4dce7c8045701350000000000000000000102656"
                   "e0e4e484c2052756c65732076312e300102656e7c54686520"
                   "77696e6e65722077696c6c20626520746865207465616d207"
                   "769746820746865206d6f737420706f696e74732061742074"
                   "686520656e64206f66207468652067616d652e20205468652"
                   "07465616d207769746820666577657220706f696e74732077"
                   "696c6c206e6f74206265207468652077696e6e65722e00000"
                   "1204ae5e65355fe4f364de07f09b1858a560d8e4549c1228b"
                   "ac9a31815063d7c1531b374a668a385cfe2154e0d4c1d42de"
                   "0afe8fe3a56fef5b0d4e1f6fd660f8954")
        self.doit()

    def test_betting_market_group_create(self):
        self.op = operations.Betting_market_group_create(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "description": [["en", "Football"], ["de", "Fußball"]],
            "event_id": "1.0.1241",
            "rules_id": "1.22.11",
            "asset_id": "1.3.124",
            "prefix": prefix,
        })
        self.cm = ("f68585abf4dce7c8045701370000000000000000000202646"
                   "5084675c39f62616c6c02656e08466f6f7462616c6cd90400"
                   "00000000010b000000000016017c0000011f2603de0504424"
                   "dfab0b120e4a258ffe15ee5be333ce8e1404986ea10f1d28e"
                   "e033ae6b3d2eea9202b4a18bf3e3bff6ae5ddfe3b4b9d7713"
                   "fb2ec11f123eaaa39")
        self.doit()

    def test_betting_market_create(self):
        self.op = operations.Betting_market_create(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "description": [["en", "Betting Market description"]],
            "group_id": "1.0.1241",
            "payout_condition": [["en", "Foo == Bar"], ["zh_Hans", "Foo == Bar"]],
            "prefix": prefix,
        })
        self.cm = ("f68585abf4dce7c804570138000000000000000000d904"
                   "0000000000010102656e1a42657474696e67204d61726b"
                   "6574206465736372697074696f6e0202656e0a466f6f20"
                   "3d3d20426172077a685f48616e730a466f6f203d3d2042"
                   "6172000001201b335c7806bc13383c85ab66fbe0908258"
                   "be15fbdd9a24fccc9a66edf324086d385718c3cb537e55"
                   "cf89f7539f3dbf6c0ed420e0bed67744f069ceb535d65a"
                   "ee")
        self.doit()

    def test_betting_market_group_resolve(self):
        self.op = operations.Betting_market_group_resolve(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "betting_market_group_id": "1.20.1024",
            "resolutions": [
                ["1.21.257", "cancel"],
                ["1.21.256", "cancel"],
            ],
            "prefix": prefix,
        })
        self.cm = ("f68585abf4dce7c80457013a00000000000000000080080"
                   "2800204810204000001201f978ef488f7e2a23568c42943"
                   "84332575b602d727e64a467e4fa351b04348134300db2f9"
                   "59045b7b67f3822192279d9a6ef5a4a4a6203d644c668f7"
                   "0dc42421")
        self.doit()

    def test_bet_place(self):
        self.op = operations.Bet_place(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "bettor_id": "1.2.1241",
            "betting_market_id": "1.21.1",
            "amount_to_bet": {"amount": 1000, "asset_id": "1.3.1"},
            "backer_multiplier": 2 * GRAPHENE_BETTING_ODDS_PRECISION,
            "back_or_lay": "lay",
            "prefix": prefix,
        })
        self.cm = ("f68585abf4dce7c804570139000000000000000000d909"
                   "01e80300000000000001204e0000020000011f2255c9c3"
                   "47ca766db54cbbece1243f3b3f4958ae94fb215c8e504e"
                   "780329098d622782c809b28cb9094dfbd17d919a15c202"
                   "837baf0844605b56ea4a48510de0")
        self.doit()

    def test_bet_cancel(self):
        self.op = operations.Bet_cancel(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "bettor_id": "1.2.5555",
            "bet_to_cancel": "1.22.1111",
            "prefix": prefix,
        })
        self.cm = ("f68585abf4dce7c80457013f000000000000000000b32bd70800"
                   "0001201d84eb0e1b0e4490119bd1cc17f7ab0a648ac00c50a36e"
                   "f3b0d7e12012c8ed0f78c7acad5701d9a0df58e38e33d896bad5"
                   "fc68a0f59f2f9b591062a194049518")
        self.doit()

    def test_sport_update(self):
        self.op = operations.Sport_update(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "sport_id": "1.16.1241",
            "new_name": [["en", "Football"], ["de", "Fußball"]],
            "prefix": prefix,
        })
        self.cm = ("f68585abf4dce7c804570130000000000000000000d90901020"
                   "26465084675c39f62616c6c02656e08466f6f7462616c6c0000"
                   "012046e4c042915f933b7a3717806c92bcad8f6e08eff756685"
                   "1de6a209eacf4b6726fe1db5013ec0853acab6c96a572503dd7"
                   "b0a899d144d1ece18021a52b2c5ff3")
        self.doit()

    def test_event_update(self):
        self.op = operations.Event_update(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "event_id": "1.18.12414",
            "new_event_group_id": "1.0.1241",
            "new_name": [["en", "My Event name"]],
            "new_season": [["en", "2016-17"]],
            "new_start_time": "2017-03-29T09:15:05",
            "is_live_market": True,
            "prefix": prefix,
        })
        self.cm = ("f68585abf4dce7c804570134000000000000000000fe6001d90"
                   "4000000000001010102656e0d4d79204576656e74206e616d65"
                   "010102656e07323031362d313701197bdb580101000001207e7"
                   "3251603500baea831cda528dfcbec55fa34994f8fca23fe2b2a"
                   "21e0edbb2c033df02e267129c29a61a74588b21b16539be116f"
                   "97e1f477ef0203d77a46046")
        self.doit()

    def test_event_group_update(self):
        self.op = operations.Event_group_update(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "event_group_id": "1.17.12",
            "new_sport_id": "1.16.1241",
            "new_name": [["en", "NHL"], ["zh_Hans", "國家冰球聯盟"]],
            "prefix": prefix,
        })
        self.cm = ("f68585abf4dce7c80457013200000000000000000001d904000"
                   "000001001010202656e034e484c077a685f48616e7312e59c8b"
                   "e5aeb6e586b0e79083e881afe79b9f0c000001201eea42229a7"
                   "15506ec419d41a459d546cad9247f7100d62015fdf187747e9b"
                   "78378b538cbde9902afb6b9ac95736999927146759174b60fbe"
                   "3d477e007611080")
        self.doit()

    def test_betting_market_rules_update(self):
        self.op = operations.Betting_market_rules_update(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "betting_market_rules_id": "1.19.2324",
            "new_name": [["en", "NHL Rules v1.0"]],
            "new_description": [["en", "The winner will be the team with the most points at the end of the game.  The team with fewer points will not be the winner."]],
            "prefix": prefix,
        })
        self.cm = ("f68585abf4dce7c804570136000000000000000000010102656"
                   "e0e4e484c2052756c65732076312e30010102656e7c54686520"
                   "77696e6e65722077696c6c20626520746865207465616d20776"
                   "9746820746865206d6f737420706f696e747320617420746865"
                   "20656e64206f66207468652067616d652e20205468652074656"
                   "16d207769746820666577657220706f696e74732077696c6c20"
                   "6e6f74206265207468652077696e6e65722e009412000120576"
                   "68943d630b9c55f0f37157907d7c82563fe80cebd17023e14ba"
                   "8ad1a5270d1c86825e153a1d9caace868487e76bd7590ffdab1"
                   "39c5eebbf41f12d52e55405")
        self.doit()

    def test_betting_market_group_update(self):
        self.op = operations.Betting_market_group_update(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "betting_market_group_id": "1.20.24124",
            "new_description": [["en", "Football"], ["de", "Fußball"]],
            "new_event_id": "1.0.1241",
            "new_rules_id": "1.22.11",
            "freeze": False,
            "delay_bets": False,
            "prefix": prefix,
        })
        self.cm = ("f68585abf4dce7c804570146000000000000000000bcbc01010"
                   "2026465084675c39f62616c6c02656e08466f6f7462616c6c01"
                   "0b00000000001601010001000000011f50b9bc677bcdfd5eb44"
                   "d22ae8ebd0ad1a14b30edeeece0caffeee5ae884bb6836ba454"
                   "35314d7c74720ebd9512e86624e28fa47096e23ab2adc543ac1"
                   "064dc35")
        self.doit()

    def test_betting_market_update(self):
        self.op = operations.Betting_market_update(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "betting_market_id": "1.21.124",
            "new_group_id": "1.0.1241",
            "new_description": [["en", "Betting market description"]],
            "new_payout_condition": [["en", "Foo == Bar"], ["zh_Hans", "Foo == Bar"]],
            "prefix": prefix,
        })
        self.cm = ("f68585abf4dce7c8045701470000000000000000007c01d9040"
                   "00000000001010102656e1a42657474696e67206d61726b6574"
                   "206465736372697074696f6e010202656e0a466f6f203d3d204"
                   "26172077a685f48616e730a466f6f203d3d204261720000011f"
                   "0e15c672784026c1cd5459f11ae7f1a43cefe23bed4a86fd677"
                   "402db5d5815ab0882a16847a74cfa6d7e32dc8d3fcad919fe36"
                   "02ddeb1ee739489921805f1326")
        self.doit()

    def test_asset_create(self):
        self.op = operations.Asset_create(**{
            "fee": {
                "amount": 0,
                "asset_id": "1.3.0"
            },
            "issuer": "1.2.0",
            "symbol": "THING",
            "precision": 0,
            "common_options": {
                "max_supply": "1000000000000000",
                "market_fee_percent": 0,
                "max_market_fee": "1000000000000000",
                "issuer_permissions": 79,
                "flags": 0,
                "core_exchange_rate": {
                    "base": {
                        "amount": 0,
                        "asset_id": "1.3.0"
                    },
                    "quote": {
                        "amount": 0,
                        "asset_id": "1.3.0"
                    }
                },
                "whitelist_authorities": ["1.2.0"],
                "blacklist_authorities": ["1.2.1"],
                "whitelist_markets": ["1.3.0"],
                "blacklist_markets": ["1.3.1"],
                "description": "Foobar think",
                "extensions": []
            },
            "bitasset_opts": {
                "feed_lifetime_sec": 86400,
                "minimum_feeds": 7,
                "force_settlement_delay_sec": 86400,
                "force_settlement_offset_percent": 100,
                "maximum_force_settlement_volume": 50,
                "short_backing_asset": "1.3.0",
                "extensions": []
            },
            "is_prediction_market": False,
            "extensions": []
        })
        self.cm = ("f68585abf4dce7c80457010a000000000000000000000554484"
                   "94e47000080c6a47e8d030000000080c6a47e8d03004f000000"
                   "000000000000000000000000000000000000010001010100010"
                   "10c466f6f626172207468696e6b000180510100078051010064"
                   "0032000000000000011f1b8ac491bb327921d9346d543e530d8"
                   "8acb68bade58296a7a27b0a74a28eaca762260dbb905a6415f6"
                   "225a8028a810de6290badc29d16fea0ffd88bc8c0cbec4")
        self.doit()

    def test_asset_update(self):
        self.op = operations.Asset_update(**{
            "fee": {
                "amount": 0,
                "asset_id": "1.3.0"
            },
            "issuer": "1.2.0",
            "asset_to_update": "1.3.0",
            "new_options": {
                "max_supply": "1000000000000000",
                "market_fee_percent": 0,
                "max_market_fee": "1000000000000000",
                "issuer_permissions": 79,
                "flags": 0,
                "core_exchange_rate": {
                    "base": {
                        "amount": 0,
                        "asset_id": "1.3.0"
                    },
                    "quote": {
                        "amount": 0,
                        "asset_id": "1.3.0"
                    }
                },
                "whitelist_authorities": [],
                "blacklist_authorities": [],
                "whitelist_markets": [],
                "blacklist_markets": [],
                "description": "",
                "extensions": []
            },
            "extensions": []
        })
        self.cm = ("f68585abf4dce7c80457010b000000000000000000000000008"
                   "0c6a47e8d030000000080c6a47e8d03004f0000000000000000"
                   "000000000000000000000000000000000000000000011f51477"
                   "1af6ac47a12a387979b6452afcd3f50514277efd7938f5227a7"
                   "fe7287db529d251e2b7c31d4a2d8ed59035b78b64f95e6011d9"
                   "58ab9504008a56c83cbb6")
        self.doit()

    def test_asset_update_bitasset(self):
        self.op = operations.Asset_update_bitasset(**{
            "fee": {
                "amount": 0,
                "asset_id": "1.3.0"
            },
            "issuer": "1.2.0",
            "asset_to_update": "1.3.0",
            "new_options": {
                "feed_lifetime_sec": 86400,
                "minimum_feeds": 1,
                "force_settlement_delay_sec": 86400,
                "force_settlement_offset_percent": 0,
                "maximum_force_settlement_volume": 2000,
                "short_backing_asset": "1.3.0",
                "extensions": []
            },
            "extensions": []
        })
        self.cm = ("f68585abf4dce7c80457010c000000000000000000000080510"
                   "10001805101000000d0070000000001205e7fed2110783b4fe9"
                   "ec1f1a71ad0325fce04fd11d03a534baac5cf18c52c91e6fdae"
                   "b76cff9d480a96500cbfde214cadd436e8f66aa61ad3f14973e"
                   "42406eca")
        self.doit()

    def compareConstructedTX(self):
        self.op = operations.Asset_update_bitasset(**{
            "fee": {
                "amount": 0,
                "asset_id": "1.3.0"
            },
            "issuer": "1.2.0",
            "asset_to_update": "1.3.0",
            "new_options": {
                "feed_lifetime_sec": 86400,
                "minimum_feeds": 1,
                "force_settlement_delay_sec": 86400,
                "force_settlement_offset_percent": 0,
                "maximum_force_settlement_volume": 2000,
                "short_backing_asset": "1.3.0",
                "extensions": []
            },
            "extensions": []
        })
        ops = [Operation(self.op)]

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
        self.cm = rpc.serialize_transaction(tx.json())
        print("soll: %s" % self.cm)
        print("ist:  %s" % txWire)
        print(txWire[:-130] == self.cm[:-130])
        self.assertEqual(self.cm[:-130], txWire[:-130])


if __name__ == '__main__':
    t = Testcases()
    t.compareConstructedTX()
