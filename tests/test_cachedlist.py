import time
import unittest
from mock import MagicMock
from peerplays import PeerPlays
from peerplays.sport import Sports
from peerplays.eventgroup import EventGroups
from peerplays.event import Events
from peerplays.bettingmarketgroup import BettingMarketGroups
from peerplays.bettingmarket import BettingMarkets
import logging

logging.basicConfig(level=logging.DEBUG)


class Testcases(unittest.TestCase):
    def test_evg(self):
        EventGroups("1.20.0")
        EventGroups("1.20.0")

        Sports()
        Sports()

        Events("1.21.12")
        Events("1.21.12")

        BettingMarketGroups("1.22.12")
        BettingMarketGroups("1.22.12")

        BettingMarkets("1.24.241")
        BettingMarkets("1.24.241")

    """
    def test_proposals(self):
        from peerplays.proposal import Proposals

        Proposals("witness-account")
        Proposals("witness-account")
        time.sleep(11)
        Proposals("witness-account")

    def test_bms(self):
        from peerplays.bettingmarket import BettingMarkets

        BettingMarkets("1.20.0")
        BettingMarkets("1.20.0")
        time.sleep(11)
        BettingMarkets("1.20.0")
    """
