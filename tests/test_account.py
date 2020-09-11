import numpy as np
import unittest
import mock
from pprint import pprint
from peerplays import PeerPlays
from peerplays.account import Account
from peerplays.amount import Amount
from peerplays.asset import Asset
from peerplays.instance import set_shared_peerplays_instance
from peerplaysbase.operationids import getOperationNameForId
from .fixtures import fixture_data, peerplays


class Testcases(unittest.TestCase):

    def setUp(self):
        fixture_data()

    def test_account(self):
        Account("witness-account")
        Account("1.2.3")
        asset = Asset("1.3.0")
        symbol = asset["symbol"]
        account = Account("witness-account", full=True)
        self.assertEqual(account.name, "witness-account")
        self.assertEqual(account["name"], account.name)
        self.assertEqual(account["id"], "1.2.1")
        self.assertIsInstance(account.balance("1.3.0"), Amount)
        self.assertIsInstance(account.balance({"symbol": symbol}), Amount)
        self.assertIsInstance(account.balances, list)
        for h in account.history(limit=1):
            pass

        # BlockchainObjects method
        account.cached = False
        self.assertTrue(account.items())
        account.cached = False
        self.assertIn("id", account)
        account.cached = False
        self.assertEqual(account["id"], "1.2.1")
        self.assertEqual(str(account), "<Account 1.2.1>")
        self.assertIsInstance(Account(account), Account)

    def test_account_upgrade(self):
        name = 'j1-' + str(np.random.randint(100000000000000000))
        peerplays.create_account(
            account_name=name,
            registrar="jemshid",
            owner_key='TEST6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV',
            active_key='TEST6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV',
            memo_key='TEST6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV')
        peerplays.transfer(name, 100000, "TEST")
        account = Account(name)
        tx = account.upgrade()
        ops = tx["operations"]
        op = ops[0][1]
        self.assertEqual(len(ops), 1)
        self.assertEqual(
            getOperationNameForId(ops[0][0]),
            "account_upgrade"
        )
        self.assertTrue(
            op["upgrade_to_lifetime_member"]
        )
        self.assertEqual(
            op["account_to_upgrade"],
            account["id"],
        )
