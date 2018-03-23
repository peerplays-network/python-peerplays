import mock
import string
import unittest
import random
from pprint import pprint
from peerplays import PeerPlays
from peerplaysbase.operationids import getOperationNameForId
from peerplays.amount import Amount
from peerplaysbase.account import PrivateKey
from peerplays.instance import set_shared_peerplays_instance

wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"
core_unit = "PPY"


class Testcases(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ppy = PeerPlays(
            nobroadcast=True,
            wif=[wif]
        )
        # from getpass import getpass
        # self.ppy.wallet.unlock(getpass())
        set_shared_peerplays_instance(self.ppy)
        self.ppy.set_default_account("init0")

    def test_connect(self):
        self.ppy.connect()

    def test_set_default_account(self):
        self.ppy.set_default_account("init0")

    def test_info(self):
        info = self.ppy.info()
        for key in ['current_witness',
                    'head_block_id',
                    'head_block_number',
                    'id',
                    'last_irreversible_block_num',
                    'next_maintenance_time',
                    'random',
                    'recently_missed_count',
                    'time']:
            self.assertTrue(key in info)

    def test_finalizeOps(self):
        ppy = self.ppy
        tx1 = ppy.new_tx()
        tx2 = ppy.new_tx()
        self.ppy.transfer("init1", 1, core_unit, append_to=tx1)
        self.ppy.transfer("init1", 2, core_unit, append_to=tx2)
        self.ppy.transfer("init1", 3, core_unit, append_to=tx1)
        tx1 = tx1.json()
        tx2 = tx2.json()
        ops1 = tx1["operations"]
        ops2 = tx2["operations"]
        self.assertEqual(len(ops1), 2)
        self.assertEqual(len(ops2), 1)

    def test_transfer(self):
        ppy = self.ppy
        tx = ppy.transfer(
            "1.2.8", 1.33, core_unit, memo="Foobar", account="1.2.7")
        self.assertEqual(
            getOperationNameForId(tx["operations"][0][0]),
            "transfer"
        )
        op = tx["operations"][0][1]
        self.assertIn("memo", op)
        self.assertEqual(op["from"], "1.2.7")
        self.assertEqual(op["to"], "1.2.8")
        amount = Amount(op["amount"])
        self.assertEqual(float(amount), 1.33)

    def test_create_account(self):
        ppy = self.ppy
        name = ''.join(random.choice(string.ascii_lowercase) for _ in range(12))
        key1 = PrivateKey()
        key2 = PrivateKey()
        key3 = PrivateKey()
        key4 = PrivateKey()
        tx = ppy.create_account(
            name,
            registrar="init0",   # 1.2.7
            referrer="init1",    # 1.2.8
            referrer_percent=33,
            owner_key=str(key1.pubkey),
            active_key=str(key2.pubkey),
            memo_key=str(key3.pubkey),
            additional_owner_keys=[str(key4.pubkey)],
            additional_active_keys=[str(key4.pubkey)],
            additional_owner_accounts=["committee-account"],  # 1.2.0
            additional_active_accounts=["committee-account"],
            proxy_account="init0",
            storekeys=False
        )
        self.assertEqual(
            getOperationNameForId(tx["operations"][0][0]),
            "account_create"
        )
        op = tx["operations"][0][1]
        role = "active"
        self.assertIn(
            str(key2.pubkey),
            [x[0] for x in op[role]["key_auths"]])
        self.assertIn(
            str(key4.pubkey),
            [x[0] for x in op[role]["key_auths"]])
        self.assertIn(
            "1.2.0",
            [x[0] for x in op[role]["account_auths"]])
        role = "owner"
        self.assertIn(
            str(key1.pubkey),
            [x[0] for x in op[role]["key_auths"]])
        self.assertIn(
            str(key4.pubkey),
            [x[0] for x in op[role]["key_auths"]])
        self.assertIn(
            "1.2.0",
            [x[0] for x in op[role]["account_auths"]])
        self.assertEqual(
            op["options"]["voting_account"],
            "1.2.7")
        self.assertEqual(
            op["registrar"],
            "1.2.7")
        self.assertEqual(
            op["referrer"],
            "1.2.8")
        self.assertEqual(
            op["referrer_percent"],
            33 * 100)

    def test_weight_threshold(self):
        ppy = self.ppy

        auth = {'account_auths': [['1.2.0', '1']],
                'extensions': [],
                'key_auths': [
                    ['PPY55VCzsb47NZwWe5F3qyQKedX9iHBHMVVFSc96PDvV7wuj7W86n', 1],
                    ['PPY7GM9YXcsoAJAgKbqW2oVj7bnNXFNL4pk9NugqKWPmuhoEDbkDv', 1]],
                'weight_threshold': 3}  # threshold fine
        ppy._test_weights_treshold(auth)
        auth = {'account_auths': [['1.2.0', '1']],
                'extensions': [],
                'key_auths': [
                    ['PPY55VCzsb47NZwWe5F3qyQKedX9iHBHMVVFSc96PDvV7wuj7W86n', 1],
                    ['PPY7GM9YXcsoAJAgKbqW2oVj7bnNXFNL4pk9NugqKWPmuhoEDbkDv', 1]],
                'weight_threshold': 4}  # too high

        with self.assertRaises(ValueError):
            ppy._test_weights_treshold(auth)

    def test_allow(self):
        ppy = self.ppy
        tx = ppy.allow(
            "PPY55VCzsb47NZwWe5F3qyQKedX9iHBHMVVFSc96PDvV7wuj7W86n",
            weight=1,
            threshold=1,
            permission="owner"
        )
        self.assertEqual(
            getOperationNameForId(tx["operations"][0][0]),
            "account_update"
        )
        op = tx["operations"][0][1]
        self.assertIn("owner", op)
        self.assertIn(
            ["PPY55VCzsb47NZwWe5F3qyQKedX9iHBHMVVFSc96PDvV7wuj7W86n", '1'],
            op["owner"]["key_auths"])
        self.assertEqual(op["owner"]["weight_threshold"], 1)

    """ Disable this test until we can test with an actual setup on the
        main/testnet
    def test_disallow(self):
        ppy = self.ppy
        with self.assertRaisesRegex(ValueError, ".*Changes nothing.*"):
            ppy.disallow(
                "PPY55VCzsb47NZwWe5F3qyQKedX9iHBHMVVFSc96PDvV7wuj7W86n",
                weight=1,
                threshold=1,
                permission="owner"
            )
        with self.assertRaisesRegex(ValueError, ".*Cannot have threshold of 0.*"):
            ppy.disallow(
                "PPY6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV",
                weight=1,
                threshold=1,
                permission="owner"
            )
    """

    def test_update_memo_key(self):
        ppy = self.ppy
        tx = ppy.update_memo_key("PPY55VCzsb47NZwWe5F3qyQKedX9iHBHMVVFSc96PDvV7wuj7W86n")
        self.assertEqual(
            getOperationNameForId(tx["operations"][0][0]),
            "account_update"
        )
        op = tx["operations"][0][1]
        self.assertEqual(
            op["new_options"]["memo_key"],
            "PPY55VCzsb47NZwWe5F3qyQKedX9iHBHMVVFSc96PDvV7wuj7W86n")

    def test_approvewitness(self):
        ppy = self.ppy
        tx = ppy.approvewitness("init0")
        self.assertEqual(
            getOperationNameForId(tx["operations"][0][0]),
            "account_update"
        )
        op = tx["operations"][0][1]
        self.assertIn(
            "1:0",
            op["new_options"]["votes"])

    def test_approvecommittee(self):
        ppy = self.ppy
        tx = ppy.approvecommittee("init0")
        self.assertEqual(
            getOperationNameForId(tx["operations"][0][0]),
            "account_update"
        )
        op = tx["operations"][0][1]
        self.assertIn(
            "0:11",
            op["new_options"]["votes"])
