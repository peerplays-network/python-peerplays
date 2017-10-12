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
            # bundle=True,
            # Overwrite wallet to use this list of wifs only
            wif=[wif]
        )

    def test_sport_create(self):
        tx = self.ppy.sport_create([          # relative id 0.0.0
            ["de", "Fussball"],
            ["en", "Soccer"],
        ])
        pprint(tx)
