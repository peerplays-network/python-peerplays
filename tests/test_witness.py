import unittest
from peerplays import PeerPlays
from peerplays.witness import Witnesses


class Testcases(unittest.TestCase):
    def test__contains__(self):
        witnesses = Witnesses(peerplays_instance=PeerPlays())
        self.assertNotIn("init0", witnesses)
        self.assertNotIn("1.2.7", witnesses)
        self.assertNotIn("1.6.1", witnesses)
