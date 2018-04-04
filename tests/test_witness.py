import unittest
from peerplays import PeerPlays
from peerplays.instance import set_shared_peerplays_instance
from peerplays.witness import Witnesses


class Testcases(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ppy = PeerPlays()
        self.ppy.set_default_account("init0")
        set_shared_peerplays_instance(self.ppy)

    def test__contains__(self):
        witnesses = Witnesses()
        self.assertIn("init0", witnesses)
        self.assertIn("1.2.7", witnesses)
        self.assertIn("1.6.1", witnesses)
        self.assertNotIn("nathan", witnesses)
