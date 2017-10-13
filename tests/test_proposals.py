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

    def test_finalizeOps_proposal(self):
        ppy = self.ppy
        # proposal = ppy.new_proposal(ppy.tx())
        proposal = ppy.proposal()
        self.ppy.transfer("init1", 1, "PPY", append_to=proposal)
        tx = ppy.tx().json()  # default tx buffer
        ops = tx["operations"]
        self.assertEqual(len(ops), 1)
        self.assertEqual(ops[0][0], 22)
        prop = ops[0][1]
        self.assertEqual(len(prop["proposed_ops"]), 1)
        self.assertEqual(prop["proposed_ops"][0]["op"][0], 0)

    def test_finalizeOps_proposal2(self):
        ppy = self.ppy
        proposal = ppy.new_proposal()
        # proposal = ppy.proposal()
        self.ppy.transfer("init1", 1, "PPY", append_to=proposal)
        tx = ppy.tx().json()  # default tx buffer
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

    def test_finalizeOps_changeproposer_new(self):
        ppy = self.ppy
        proposal = ppy.proposal(proposer="init5")
        ppy.transfer("init1", 1, "PPY", append_to=proposal)
        tx = ppy.tx().json()
        ops = tx["operations"]
        self.assertEqual(len(ops), 1)
        self.assertEqual(ops[0][0], 22)
        prop = ops[0][1]
        self.assertEqual(len(prop["proposed_ops"]), 1)
        self.assertEqual(prop["fee_paying_account"], "1.2.12")
        self.assertEqual(prop["proposed_ops"][0]["op"][0], 0)

    def test_finalizeOps_changeproposer_legacy(self):
        ppy = self.ppy
        ppy.proposer = "init5"
        tx = ppy.transfer("init1", 1, "PPY")
        ops = tx["operations"]
        self.assertEqual(len(ops), 1)
        self.assertEqual(ops[0][0], 22)
        prop = ops[0][1]
        self.assertEqual(len(prop["proposed_ops"]), 1)
        self.assertEqual(prop["fee_paying_account"], "1.2.12")
        self.assertEqual(prop["proposed_ops"][0]["op"][0], 0)

    def test_new_proposals(self):
        ppy = self.ppy
        p1 = ppy.new_proposal()
        p2 = ppy.new_proposal()
        self.assertIsNotNone(id(p1), id(p2))

    def test_new_txs(self):
        ppy = self.ppy
        p1 = ppy.new_tx()
        p2 = ppy.new_tx()
        self.assertIsNotNone(id(p1), id(p2))
