import unittest
import mock
from peerplays import PeerPlays
from peerplays.message import Message
from peerplays.instance import set_shared_peerplays_instance
from .fixtures import fixture_data, peerplays, core_unit


class Testcases(unittest.TestCase):

    def setUp(self):
        fixture_data()

    """
    def test_sign_message(self):
        p = Message("message foobar").sign()
        Message(p).verify()
    """
