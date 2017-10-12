import unittest
from pprint import pprint
from peerplays import PeerPlays

wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"


class Testcases(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ppy = PeerPlays(
            nobroadcast=True,
            # this account creates the proposal
            proposer="init2",
            # Proposal needs to be approve within 1 hour
            proposal_expiration=60 * 60 * 24 * 14,
            # We want to bundle many operations into a single transaction
            bundle=True,
            # Overwrite wallet to use this list of wifs only
            wif=[wif]
        )

    def test_sport_create(self):
        self.ppy.sport_create([          # relative id 0.0.0
            ["de", "Fussball"],
            ["en", "Soccer"],
        ])
        tx = self.ppy.tx()
        ops = tx["operations"]
        prop = ops[0][1]
        self.assertEqual(len(ops), 1)
        self.assertEqual(ops[0][0], 22)
        self.assertEqual(len(prop["proposed_ops"]), 1)
        self.assertEqual(prop["proposed_ops"][0]["op"][0], 47)

    def test_two_sport_create(self):
        self.ppy.sport_create([          # relative id 0.0.0
            ["de", "Fussball"],
            ["en", "Soccer"],
        ])
        self.ppy.sport_create([          # relative id 0.0.0
            ["de", "Fussball"],
            ["en", "Soccer"],
        ])
        tx = self.ppy.tx()
        pprint(tx)
        ops = tx["operations"]
        prop = ops[0][1]
        self.assertEqual(len(ops), 1)
        self.assertEqual(ops[0][0], 22)
        self.assertEqual(len(prop["proposed_ops"]), 2)
        self.assertEqual(prop["proposed_ops"][0]["op"][0], 47)
