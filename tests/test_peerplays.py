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
        ops1 = tx1["operations"]
        ops2 = tx2["operations"]
        self.assertEqual(len(ops1), 2)
        self.assertEqual(len(ops2), 1)

    def test_finalizeOps_proposal(self):
        ppy = self.ppy
        # proposal = ppy.new_proposal(ppy.tx())
        proposal = ppy.proposal()
        self.ppy.transfer("init1", 1, "PPY", append_to=proposal)
        tx = ppy.tx().json()  # default tx buffer
        pprint(tx)
        ops = tx["operations"]
        self.assertEqual(len(ops), 1)
        self.assertEqual(ops[0][0], 22)
        prop = ops[0][1]
        self.assertEqual(len(prop["proposed_ops"]), 1)
        self.assertEqual(prop["proposed_ops"][0]["op"][0], 0)

    def test_finalizeOps_combined_proposal(self):
        ppy = self.ppy
        parent = ppy.new_tx()
        proposal = ppy.new_proposal(parent)
        self.ppy.transfer("init1", 1, "PPY", append_to=proposal)
        self.ppy.transfer("init1", 1, "PPY", append_to=parent)
        tx = parent.json()
        ops = tx["operations"]
        self.assertEqual(len(ops), 2)
        self.assertEqual(ops[0][0], 22)
        self.assertEqual(ops[1][0], 0)
        prop = ops[0][1]
        self.assertEqual(len(prop["proposed_ops"]), 1)
        self.assertEqual(prop["proposed_ops"][0]["op"][0], 0)


if __name__ == "__main__":
    unittest.main()
