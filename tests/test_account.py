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
import string
import random


class Testcases(unittest.TestCase):

    def setUp(self):
        # fixture_data()
        peerplays.nobroadcast = False
        peerplays.blocking = True
        pass

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
        # self.assertEqual(str(account), "<Account witness-account>")
        self.assertIsInstance(Account(account), Account)

    def test_account_creation(self):
        peerplays.blocking = True
        account_name = "".join(random.choices(string.ascii_lowercase, k=10))
        account_name = account_name + "".join(random.choices(string.digits, k=10))
        print("account_name:", account_name)
        peerplays.blocking = True
        print("peerplays blocking:", peerplays.blocking)
        op_res = peerplays.create_account(
            account_name,
            referrer="1.2.7",
            password=account_name,
            blocking=True
        )
        print("op_res_keys:", op_res.keys())
        print("op_res:", op_res)
        print("op_res_keys:", op_res.keys())
        self.assertTrue(op_res["operation_results"][0][0])
        account_id = op_res["operation_results"][0][1]
        account_name_from_chain = peerplays.rpc.get_object(account_id)["name"]
        self.assertEqual(account_name, account_name_from_chain)
        peerplays.transfer(account_name, 10000, "TEST", account="nathan")
        tx = peerplays.upgrade_account(account_name)
        account = Account(account_name)
        # tx = account.upgrade()
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
