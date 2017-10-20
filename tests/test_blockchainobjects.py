import time
import unittest
from peerplays import PeerPlays, exceptions
from peerplays.instance import set_shared_peerplays_instance
from peerplays.blockchainobject import ObjectCache


class Testcases(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ppy = PeerPlays(
            nobroadcast=True,
        )
        set_shared_peerplays_instance(self.ppy)

    def test_cache(self):
        cache = ObjectCache(default_expiration=1)
        cache["foo"] = "bar"
        self.assertIn("foo", cache)
        self.assertEqual(cache["foo"], "bar")
        time.sleep(2)
        self.assertNotIn("foo", cache)
