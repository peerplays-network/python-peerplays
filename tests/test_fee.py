import unittest
from pprint import pprint
from peerplays import PeerPlays
from peerplays.instance import set_shared_peerplays_instance

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
        self.ppy.set_default_account("init0")

    def test_fee_on_transfer(self):
        tx = self.ppy.transfer("init1", 1, "1.3.0", account="init0", fee_asset="1.3.1")
        op = tx["operations"][0][1]
        self.assertEqual(op["fee"]["asset_id"], "1.3.1")

    def test_feeasset_on_transfer(self):
        tx = self.ppy.transfer("init1", 1, "1.3.0", account="init0", fee_asset="BTF")
        op = tx["operations"][0][1]
        self.assertEqual(op["fee"]["asset_id"], "1.3.1")
