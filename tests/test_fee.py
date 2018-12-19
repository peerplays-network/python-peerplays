import unittest
from pprint import pprint
from peerplays import PeerPlays
from peerplays.instance import set_shared_peerplays_instance
from .fixtures import fixture_data, peerplays


class Testcases(unittest.TestCase):

    def setUp(self):
        fixture_data()

    """
    Test has been temporary removed until proper CER is installed on chain!
    """
    """
    def test_fee_on_transfer(self):
        tx = peerplays.transfer("init1", 1, "1.3.0", account="init0", fee_asset="1.3.1")
        op = tx["operations"][0][1]
        self.assertEqual(op["fee"]["asset_id"], "1.3.1")

    def test_feeasset_on_transfer(self):
        tx = peerplays.transfer("init1", 1, "1.3.0", account="init0", fee_asset="BTF")
        op = tx["operations"][0][1]
        self.assertEqual(op["fee"]["asset_id"], "1.3.1")
    """
