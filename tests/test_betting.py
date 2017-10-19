import datetime
import unittest
import mock
from pprint import pprint
from peerplays import PeerPlays
from peerplays.amount import Amount
from peerplays.utils import parse_time
from peerplays.bettingmarket import BettingMarket
from peerplaysbase.operationids import getOperationNameForId

wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"


class Testcases(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ppy = PeerPlays(
            nobroadcast=True,
            # We want to bundle many operations into a single transaction
            bundle=True,
            # Overwrite wallet to use this list of wifs only
            wif=[wif]
        )

    def test_bet_place(self):
        def new_refresh(self):
            dict.__init__(
                self,
                {"id": "1.21.11123"}
            )

        with mock.patch(
            "peerplays.bettingmarket.BettingMarket.refresh",
            new=new_refresh
        ):
            self.ppy.bet_place(
                "1.21.11123",
                Amount(1244, "PPY"),
                2,
                "back",
            )
            tx = self.ppy.tx().json()
            ops = tx["operations"]
            op = ops[0][1]
            self.assertEqual(len(ops), 1)
            self.assertEqual(
                getOperationNameForId(ops[0][0]),
                "bet_place"
            )
            self.assertEqual(
                op["amount_to_bet"],
                {'amount': 124400000, 'asset_id': '1.3.0'}
            )
            self.assertEqual(
                op["back_or_lay"],
                "back"
            )
            self.assertEqual(
                op["backer_multiplier"],
                2 * 10000
            )
            self.assertEqual(
                op["betting_market_id"],
                "1.21.11123",
            )
            self.assertEqual(
                op["bettor_id"],
                "1.2.7",
            )

    def test_bet_cancel(self):
        def new_refresh(self):
            dict.__init__(
                self,
                {"id": "1.22.13"}
            )

        with mock.patch(
            "peerplays.bet.Bet.refresh",
            new=new_refresh
        ):
            self.ppy.bet_cancel(
                "1.22.13",
            )
            tx = self.ppy.tx().json()
            ops = tx["operations"]
            op = ops[0][1]
            self.assertEqual(len(ops), 1)
            self.assertEqual(
                getOperationNameForId(ops[0][0]),
                "bet_cancel"
            )
            self.assertEqual(
                op["bet_to_cancel"],
                "1.22.13",
            )
            self.assertEqual(
                op["bettor_id"],
                "1.2.7",
            )
