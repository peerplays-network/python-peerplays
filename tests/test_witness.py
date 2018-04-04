import unittest
from peerplays import PeerPlays
from peerplays.instance import set_shared_peerplays_instance
from peerplays.witness import Witnesses


class Testcases(unittest.TestCase):

    def test__contains__(self):
        witnesses = Witnesses()
        self.assertIn("init0", witnesses)
        self.assertIn("1.2.7", witnesses)
        self.assertIn("1.6.1", witnesses)
        self.assertNotIn("nathan", witnesses)
