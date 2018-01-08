import datetime
import unittest
from peerplays import PeerPlays
from peerplays.utils import parse_time
from peerplays.exceptions import ObjectNotInProposalBuffer
from peerplaysbase.operationids import getOperationNameForId
from peerplays.instance import set_shared_peerplays_instance

wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"


class Testcases(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ppy = PeerPlays(
            nobroadcast=True,
            # Overwrite wallet to use this list of wifs only
            wif=[wif]
        )
        set_shared_peerplays_instance(self.ppy)
        self.ppy.set_default_account("init0")

    def test_event_create(self):
        ev = [["de", "1. Bundesliga"], ["en", "First Country League"]]
        desc = [["de", "Bundesliga"], ["en", "Germany Scoccer Championship"]]
        season = [["de", "Januar 2016"], ["en", "January 2016"]]
        start = datetime.datetime(2016, 1, 1, 0, 0, 0)
        rule_name = [["en", "NHL Rules v1.0"]]
        rule = [["en", "The winner will be the team with the most points ..."]]
        bmg_name = [["de", "Meine Market Group"], ["en", "My betting market group"]]
        bm_name = [["de", "Nuernberg gewinnt"], ["en", "Nuremberg wins"]]
        cond = [["de", "Description: Fuerth gewinnt"],
                ["en", "Description: Fuerth wins"]]

        with self.assertRaises(ObjectNotInProposalBuffer):
            self.ppy.event_group_create(ev, sport_id="0.0.0")
        with self.assertRaises(ObjectNotInProposalBuffer):
            self.ppy.event_create(desc, season, start, event_group_id="0.0.0")
        with self.assertRaises(ObjectNotInProposalBuffer):
            self.ppy.betting_market_group_create(bmg_name, event_id="0.0.2", rules_id="0.0.3")
        with self.assertRaises(ObjectNotInProposalBuffer):
            self.ppy.betting_market_group_create(bmg_name, event_id="0.0.3", rules_id="0.0.4")

        proposal = self.ppy.proposal()

        # Sport (0)
        self.ppy.sport_create(["en", "testsport"], append_to=proposal)

        # Eventgroup (1)
        self.ppy.event_group_create(ev, sport_id="0.0.0", append_to=proposal)
        with self.assertRaises(ObjectNotInProposalBuffer):
            self.ppy.event_group_create(ev, sport_id="0.0.1", append_to=proposal)

        # Event (2)
        self.ppy.event_create(desc, season, start, event_group_id="0.0.1", append_to=proposal)
        with self.assertRaises(ObjectNotInProposalBuffer):
            self.ppy.event_create(desc, season, start, event_group_id="0.0.2")
            self.ppy.event_create(desc, season, start, event_group_id="0.0.0")

        # Rule (3)
        self.ppy.betting_market_rules_create(rule_name, rule, append_to=proposal)

        # BMG (4)
        self.ppy.betting_market_group_create(bmg_name, event_id="0.0.2", rules_id="0.0.3", append_to=proposal)
        with self.assertRaises(ObjectNotInProposalBuffer):
            self.ppy.betting_market_group_create(bmg_name, event_id="0.0.3", rules_id="0.0.4", append_to=proposal)
            self.ppy.betting_market_group_create(bmg_name, event_id="0.0.1", rules_id="0.0.4", append_to=proposal)

        # BM (5)
        self.ppy.betting_market_create(cond, bm_name, group_id="0.0.4", append_to=proposal)
        with self.assertRaises(ObjectNotInProposalBuffer):
            self.ppy.betting_market_create(cond, bm_name, group_id="0.0.3", append_to=proposal)
            self.ppy.betting_market_create(cond, bm_name, group_id="0.0.5", append_to=proposal)
