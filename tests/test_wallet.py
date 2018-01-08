import unittest
import mock
from pprint import pprint
from peerplays import PeerPlays
from peerplays.account import Account
from peerplays.amount import Amount
from peerplays.asset import Asset
from peerplays.instance import set_shared_peerplays_instance
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
        self.ppy.set_default_account("init0")
        set_shared_peerplays_instance(self.ppy)
