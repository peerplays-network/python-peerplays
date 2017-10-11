import unittest
from pprint import pprint
from peerplays import PeerPlays

wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"


class Testcases(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ppy = PeerPlays(
            nobroadcast=True,
            wif={
                "active": wif
            })

        self.t1 = 0
        self.t2 = self.ppy.new_txbuffer()

    def test_addops(self):
        ppy = self.ppy
        self.assertEqual(self.t1, 0)
        self.assertEqual(self.t2, 1)

        ppy.set_txbuffer(self.t1)
        ppy.transfer("init0", 1, "PPY")
        tx = ppy.transfer("init0", 2, "PPY")
        # Only one Operation in Tx
        self.assertEqual(len(tx["operations"]), 1)

        ppy.bundle = True
        ppy.set_txbuffer(self.t2)
        ppy.transfer("init0", 3, "PPY")
        ppy.transfer("init0", 4, "PPY")
        ppy.transfer("init0", 5, "PPY")
        # Two ops need to be here!
        tx2 = ppy.get_txbuffer(self.t2)
        self.assertEqual(len(tx2.json()["operations"]), 3)

        # After broadcast, there should not be anything left in the buffer
        tx2.broadcast()
        self.assertEqual(len(tx2.json()["operations"]), 0)

        # After tx1, there should not be anything left in the buffer
        tx1 = ppy.get_txbuffer(self.t1)
        self.assertEqual(len(tx1.json()["operations"]), 0)
