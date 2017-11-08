import unittest
import mock
from pprint import pprint
from peerplays import PeerPlays
from peerplays.account import Account
from peerplays.amount import Amount
from peerplays.asset import Asset
from peerplays.instance import set_shared_peerplays_instance
from peerplaysbase.operationids import getOperationNameForId

wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"


class Testcases(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ppy = PeerPlays(
            nobroadcast=True,
            # We want to bundle many operations into a single transaction
            bundle=True,
            # Overwrite wallet to use this list of wifs only
            wif=[wif]
        )
        set_shared_peerplays_instance(self.ppy)

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
        account = Account("witness-account")
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
            "1.2.1",
        )
