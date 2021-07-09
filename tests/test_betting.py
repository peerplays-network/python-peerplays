import datetime
import unittest
import mock
from pprint import pprint
from peerplays import exceptions
from peerplays.amount import Amount
from peerplays.utils import parse_time
from peerplaysbase.operationids import getOperationNameForId, operations
from peerplays.instance import set_shared_peerplays_instance
from peerplays.sport import Sport, Sports
from peerplays.eventgroup import EventGroup, EventGroups
from peerplays.event import Event, Events
from peerplays.rule import Rule, Rules
from peerplays.bettingmarketgroup import BettingMarketGroup, BettingMarketGroups
from peerplays.bettingmarket import BettingMarket, BettingMarkets
from peerplays.bet import Bet
from .fixtures import fixture_data, peerplays


class Testcases(unittest.TestCase):
    def setUp(self):
        fixture_data()

    def test_bet_place(self):
        peerplays.nobroadcast = True
        tx = peerplays.bet_place("1.25.2950", Amount(1244, "1.3.0"), 2, "back")
        ops = tx["operations"]
        op = ops[0][1]
        self.assertEqual(len(ops), 1)
        self.assertEqual(getOperationNameForId(ops[0][0]), "bet_place")
        self.assertEqual(
            op["amount_to_bet"], {"amount": 124400000, "asset_id": "1.3.0"}
        )
        self.assertEqual(op["back_or_lay"], "back")
        self.assertEqual(op["backer_multiplier"], 2 * 10000)
        self.assertEqual(op["betting_market_id"], "1.25.2950")
        self.assertEqual(op["bettor_id"], "1.2.7")
        peerplays.nobroadcast = False

    def test_bet_cancel(self):
        peerplays.nobroadcast = True
        tx = peerplays.bet_cancel("1.26.13")
        ops = tx["operations"]
        op = ops[0][1]
        self.assertEqual(len(ops), 1)
        self.assertEqual(getOperationNameForId(ops[0][0]), "bet_cancel")
        self.assertEqual(op["bet_to_cancel"], "1.26.13")
        self.assertEqual(op["bettor_id"], "1.2.7")
        peerplays.nobroadcast = False

    def test_Bet_init(self):

        with self.assertRaises(exceptions.BetDoesNotExistException):
            Bet("1.{}.99999999999".format(Bet.type_id))

        def get_object(self, *args, **kwargs):
            return {"id": "1.{}.0".format(Bet.type_id)}

        with mock.patch(
            "peerplaysapi.node.PeerPlaysNodeRPC.get_object", new=get_object
        ):
            Bet("1.{}.0".format(Bet.type_id))

    def test_BettingMarket_init(self):

        with self.assertRaises(exceptions.BettingMarketDoesNotExistException):
            BettingMarket("1.{}.99999999999".format(BettingMarket.type_id))

        def get_object(self, *args, **kwargs):
            return {
                "id": "1.{}.0".format(BettingMarket.type_id),
                "group_id": "1.{}.0".format(BettingMarketGroup.type_id),
            }

        with mock.patch(
            "peerplaysapi.node.PeerPlaysNodeRPC.get_object", new=get_object
        ):
            m = BettingMarket("1.{}.0".format(BettingMarket.type_id))
            self.assertIsInstance(m.bettingmarketgroup, BettingMarketGroup)

    def test_BettingMarketGroup_init(self):
        bmg = BettingMarketGroup("1.{}.211".format(BettingMarketGroup.type_id))
        self.assertIsInstance(bmg.event, Event)

    def test_Event_init(self):

        with self.assertRaises(exceptions.EventDoesNotExistException):
            Event("1.{}.99999999999".format(Event.type_id))

        def get_object(self, *args, **kwargs):
            return {
                "id": "1.{}.0".format(Event.type_id),
                "event_group_id": "1.{}.0".format(EventGroup.type_id),
            }

        with mock.patch(
            "peerplaysapi.node.PeerPlaysNodeRPC.get_object", new=get_object
        ):
            event = Event("1.{}.0".format(Event.type_id))
            self.assertIsInstance(event.eventgroup, EventGroup)

    def test_EventGroup_init(self):

        with self.assertRaises(exceptions.EventGroupDoesNotExistException):
            EventGroup("1.{}.99999999999".format(EventGroup.type_id))

        def get_object(self, *args, **kwargs):
            return {
                "id": "1.{}.0".format(EventGroup.type_id),
                "sport_id": "1.{}.0".format(Sport.type_id),
            }

        with mock.patch(
            "peerplaysapi.node.PeerPlaysNodeRPC.get_object", new=get_object
        ):
            eg = EventGroup("1.{}.0".format(EventGroup.type_id))
            self.assertIsInstance(eg.sport, Sport)

    def test_Sport_init(self):

        with self.assertRaises(exceptions.SportDoesNotExistException):
            Sport("1.{}.99999999999".format(Sport.type_id))

        def get_object(self, *args, **kwargs):
            return {"id": "1.{}.0".format(Sport.type_id)}

        with mock.patch(
            "peerplaysapi.node.PeerPlaysNodeRPC.get_object", new=get_object
        ):
            s = Sport("1.{}.0".format(Sport.type_id))
            self.assertIsInstance(s.eventgroups, list)

    def test_Rule_init(self):

        with self.assertRaises(exceptions.RuleDoesNotExistException):
            Rule("1.{}.99999999999".format(Rule.type_id))

        def get_object(self, *args, **kwargs):
            return {"id": "1.{}.0".format(Rule.type_id)}

        with mock.patch(
            "peerplaysapi.node.PeerPlaysNodeRPC.get_object", new=get_object
        ):
            Rule("1.{}.0".format(Rule.type_id))

    def test_lists(self):
        self.assertIsInstance(Sports(), list)
        self.assertIsInstance(EventGroups("1.20.2"), list)
        self.assertIsInstance(Events("1.21.2"), list)
        self.assertIsInstance(BettingMarketGroups("1.22.2"), list)
        self.assertIsInstance(Rules(), list)
        self.assertIsInstance(BettingMarkets("1.24.2"), list)

    def test_event_status_update(self):
        peerplays.nobroadcast = True
        tx = peerplays.event_update_status("1.22.2241", "settled", ["0-0"])
        self.assertEqual(tx["operations"][0][0], operations["event_update_status"])

        self.assertEqual(tx["operations"][0][1]["event_id"], "1.22.2241")
        self.assertEqual(tx["operations"][0][1]["status"], "settled")
        self.assertEqual(tx["operations"][0][1]["scores"], ["0-0"])
        peerplays.nobroadcast = False
