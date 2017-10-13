import unittest
from pprint import pprint
from peerplays import PeerPlays

wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"


class Testcases(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ppy = PeerPlays(
            nobroadcast=True,
            wif=[wif]
        )
        # from getpass import getpass
        # self.ppy.wallet.unlock(getpass())

    def test_connect(self):
        self.ppy.connect()

    def test_info(self):
        info = self.ppy.info()
        for key in ['current_witness',
                    'head_block_id',
                    'head_block_number',
                    'id',
                    'last_irreversible_block_num',
                    'next_maintenance_time',
                    'random',
                    'recently_missed_count',
                    'time']:
            self.assertTrue(key in info)

    def test_finalizeOps(self):
        ppy = self.ppy
        tx1 = ppy.new_tx()
        tx2 = ppy.new_tx()
        self.ppy.transfer("init1", 1, "PPY", append_to=tx1)
        self.ppy.transfer("init1", 2, "PPY", append_to=tx2)
        self.ppy.transfer("init1", 3, "PPY", append_to=tx1)
        tx1 = tx1.json()
        tx2 = tx2.json()
        pprint(tx1)
        pprint(tx2)
        ops1 = tx1["operations"]
        ops2 = tx2["operations"]
        self.assertEqual(len(ops1), 2)
        self.assertEqual(len(ops2), 1)


if __name__ == "__main__":
    unittest.main()
