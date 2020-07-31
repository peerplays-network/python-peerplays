import unittest
from pprint import pprint
from peerplays import PeerPlays
from peerplaysbase.operationids import getOperationNameForId
from peerplays.instance import set_shared_peerplays_instance
from .fixtures import fixture_data, peerplays, core_unit


class Testcases(unittest.TestCase):

    def setUp(self):
        fixture_data()

    def test_finalizeOps_proposal(self):
        # proposal = peerplays.new_proposal(peerplays.tx())
        proposal = peerplays.proposal()
        peerplays.transfer("init1", 1, core_unit, append_to=proposal)
        tx = peerplays.tx().json()  # default tx buffer
        ops = tx["operations"]
        self.assertEqual(len(ops), 1)
        self.assertEqual(
            getOperationNameForId(ops[0][0]),
            "proposal_create")
        prop = ops[0][1]
        self.assertEqual(len(prop["proposed_ops"]), 1)
        self.assertEqual(
            getOperationNameForId(prop["proposed_ops"][0]["op"][0]),
            "transfer")

    def test_finalizeOps_proposal2(self):
        proposal = peerplays.new_proposal()
        # proposal = peerplays.proposal()
        peerplays.transfer("init1", 1, core_unit, append_to=proposal)
        tx = peerplays.tx().json()  # default tx buffer
        ops = tx["operations"]
        self.assertEqual(len(ops), 1)
        self.assertEqual(
            getOperationNameForId(ops[0][0]),
            "proposal_create")
        prop = ops[0][1]
        self.assertEqual(len(prop["proposed_ops"]), 1)
        self.assertEqual(
            getOperationNameForId(prop["proposed_ops"][0]["op"][0]),
            "transfer")

    def test_finalizeOps_combined_proposal(self):
        parent = peerplays.new_tx()
        proposal = peerplays.new_proposal(parent)
        peerplays.transfer("init1", 1, core_unit, append_to=proposal)
        peerplays.transfer("init1", 1, core_unit, append_to=parent)
        tx = parent.json()
        ops = tx["operations"]
        self.assertEqual(len(ops), 2)
        self.assertEqual(
            getOperationNameForId(ops[0][0]),
            "proposal_create")
        self.assertEqual(
            getOperationNameForId(ops[1][0]),
            "transfer")
        prop = ops[0][1]
        self.assertEqual(len(prop["proposed_ops"]), 1)
        self.assertEqual(
            getOperationNameForId(prop["proposed_ops"][0]["op"][0]),
            "transfer")

    def test_finalizeOps_changeproposer_new(self):
        proposal = peerplays.proposal(proposer="init5")
        peerplays.transfer("init1", 1, core_unit, append_to=proposal)
        tx = peerplays.tx().json()
        ops = tx["operations"]
        self.assertEqual(len(ops), 1)
        self.assertEqual(
            getOperationNameForId(ops[0][0]),
            "proposal_create")
        prop = ops[0][1]
        self.assertEqual(len(prop["proposed_ops"]), 1)
        self.assertEqual(prop["fee_paying_account"], "1.2.12")
        self.assertEqual(
            getOperationNameForId(prop["proposed_ops"][0]["op"][0]),
            "transfer")

    def test_finalizeOps_changeproposer_legacy(self):
        peerplays.proposer = "init5"
        tx = peerplays.transfer("init1", 1, core_unit)
        ops = tx["operations"]
        self.assertEqual(len(ops), 1)
        self.assertEqual(
            getOperationNameForId(ops[0][0]),
            "proposal_create")
        prop = ops[0][1]
        self.assertEqual(len(prop["proposed_ops"]), 1)
        self.assertEqual(prop["fee_paying_account"], "1.2.12")
        self.assertEqual(
            getOperationNameForId(prop["proposed_ops"][0]["op"][0]),
            "transfer")

    def test_new_proposals(self):
        p1 = peerplays.new_proposal()
        p2 = peerplays.new_proposal()
        self.assertIsNotNone(id(p1), id(p2))

    def test_new_txs(self):
        p1 = peerplays.new_tx()
        p2 = peerplays.new_tx()
        self.assertIsNotNone(id(p1), id(p2))


if __name__ == "__main__":
    unittest.main()
