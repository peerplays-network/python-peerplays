import unittest
from peerplays import PeerPlays, exceptions
from peerplays.instance import set_shared_peerplays_instance
from peerplays.account import Account
from peerplays.committee import Committee
from .fixtures import fixture_data, peerplays


class Testcases(unittest.TestCase):

    def setUp(self):
        fixture_data()

    def test_Committee(self):
        """ Testing for Committee exceptions"""
        with self.assertRaises(
                exceptions.AccountDoesNotExistsException
        ):
            Committee("FOObarNonExisting")

        c = Committee("init2")
        self.assertEqual(c["id"], "1.5.2")
        self.assertIsInstance(c.account, Account)

        with self.assertRaises(
                exceptions.CommitteeMemberDoesNotExistsException
        ):
            Committee("1.5.10000")
