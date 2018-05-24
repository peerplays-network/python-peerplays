import mock
import datetime
import unittest

from mock import MagicMock, PropertyMock
from pprint import pprint

from peerplays import PeerPlays
from peerplays.account import Account
from peerplays.utils import parse_time
from peerplays.instance import set_shared_peerplays_instance
from peerplays.blockchainobject import BlockchainObject, ObjectCache

from peerplaysbase.operationids import getOperationNameForId
from peerplaysbase import operations

wifs = [
    "5KR4dZcS2JTeT7eedB8BvFzUesNhjkyxNR7mwXmqVypAogD35ZX",
    "5KRKC9N5ZvRBA7TWDbznYVE6gxw7Drjs5A36N1sVPJf12MAXag3",
    "5KDQVCFfBMvtc3JEywQPbwiCEvPSzQokJUJPsPUfCayBJVUYVSM"
]

account_id = "1.2.999"
test_operation_dicts = [
    {'active': {'account_auths': [],
                'address_auths': [],
                'key_auths': [['PPY7oA1zCmmK3JWP7uNbJ2Z6Fe8G7fjWos7T6ih2WC3iAvGfMVaYD',
                               1]],
                'weight_threshold': 1},
     'active_special_authority': [0, {}],
     'blacklisted_accounts': [],
     'blacklisting_accounts': [],
     'cashback_vb': '1.13.0',
     'id': account_id,
     'lifetime_referrer': account_id,
     'lifetime_referrer_fee_percentage': 8000,
     'membership_expiration_date': '1969-12-31T23:59:59',
     'name': 'init0',
     'network_fee_percentage': 2000,
     'options': {'extensions': [],
                 'memo_key': 'PPY8R3ZAd6AtQDQK9cin6fHEw9uKUwzzxLbo2w6X1aKC5Wtir8iND',
                 'num_committee': 0,
                 'num_witness': 0,
                 'votes': [],
                 'voting_account': '1.2.5'},
     'owner': {'account_auths': [],
               'address_auths': [],
               'key_auths': [['PPY8Y6f9GoaLnSmLhF8FDSc5YijLddD8ThwdEwGaNGBdCMDD8o7zF',
                              1]],
               'weight_threshold': 1},
     'owner_special_authority': [0, {}],
     'referrer': '1.2.7',
     'referrer_rewards_percentage': 0,
     'registrar': '1.2.7',
     'statistics': '2.6.7',
     'top_n_control_flags': 0,
     'whitelisted_accounts': [],
     'whitelisting_accounts': []}
]


class Testcases(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(Testcases, self).__init__(*args, **kwargs)
        self.ppy = PeerPlays(
            nobroadcast=True,
            keys=wifs
        )
        set_shared_peerplays_instance(self.ppy)
        self.mockAccount()

    def mockAccount(self):
        _cache = ObjectCache(default_expiration=60 * 60 * 1, no_overwrite=True)
        for i in test_operation_dicts:
            _cache[i["id"]] = i
        BlockchainObject._cache = _cache

    def test_finalize(self):
        account = Account(account_id)

        op = operations.Transfer(**{
            "fee": {
                "asset_id": "1.3.0",
                "amount": 1
            },
            "from": account_id,
            "to": '1.2.8',
            "amount": {
                "asset_id": "1.3.0",
                "amount": 1
            }
        })

        tx = self.ppy.finalizeOp(op, account, "active")
        self.assertEqual(len(tx["signatures"]), 1)
