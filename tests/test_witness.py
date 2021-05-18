import unittest
from peerplays import PeerPlays
from peerplays.witness import Witnesses


class Testcases(unittest.TestCase):
    def test__contains__(self):
        witnesses = Witnesses(peerplays_instance=PeerPlays())
        self.assertNotIn("committee-account", witnesses)
        self.assertNotIn("1.2.6", witnesses)
        self.assertNotIn("1.6.1000", witnesses)
