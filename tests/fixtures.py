""" Setup script for the test cases """
import os
import yaml

from peerplays.peerplays2 import PeerPlays as PeerPlays2
from peerplays import PeerPlays
from peerplays.account import Account
from peerplays.instance import set_shared_peerplays_instance
from peerplays.sport import Sports, Sport
from peerplays.bet import Bet
from peerplays.event import Events, Event
from peerplays.rule import Rules, Rule
from peerplays.proposal import Proposals, Proposal
from peerplays.eventgroup import EventGroups, EventGroup
from peerplays.bettingmarketgroup import BettingMarketGroups, BettingMarketGroup
from peerplays.bettingmarket import BettingMarkets, BettingMarket
from peerplays.witness import Witnesses, Witness
from peerplaysbase.operationids import operations

# default wifs key for testing
wifs = [
    "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3",
    "5KCBDTcyDqzsqehcb52tW5nU6pXife6V2rX9Yf7c3saYSzbDZ5W",
]
wif = wifs[0]
publicKey = "TEST6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV"
core_unit = "TEST"

# urlWalletServer = "http://10.11.12.101:8091"
# peerplays2 = PeerPlays2(urlWalletServer=urlWalletServer)
# peerplays2.unlock("password")

# peerplays instance
peerplays = PeerPlays(
    # "ws://10.11.12.101:8090", keys=wifs, nobroadcast=False, num_retries=1, blocking=True 
    # "wss://api.ppy-beatrice.blckchnd.com", keys=wifs, nobroadcast=True, num_retries=1
    "wss://mint.peerplays.download/api", keys=wifs, nobroadcast=False, num_retries=1, blocking=True
    # "wss://irona.peerplays.download/api", keys=wifs, nobroadcast=False, num_retries=1, blocking=True
    # "wss://fred.peerplays.download/api", keys=wifs, nobroadcast=False, num_retries=1, blocking=True
    # "wss://hercules.peerplays.download/api", keys=wifs, nobroadcast=False, num_retries=1, blocking=True
)
# Set defaults
# peerplays.set_default_account("init0")
set_shared_peerplays_instance(peerplays)

# Ensure we are not going to transaction anythin on chain!
# assert peerplays.nobroadcast


def fixture_data():
    peerplays.clear()
    BettingMarkets.clear_cache()
    Rules.clear_cache()
    BettingMarketGroups.clear_cache()
    Proposals.clear_cache()
    Witnesses.clear_cache()
    Events.clear_cache()
    EventGroups.clear_cache()
    Sports.clear_cache()

    with open(os.path.join(os.path.dirname(__file__), "fixtures.yaml")) as fid:
        data = yaml.safe_load(fid)

    [Account(x) for x in data.get("accounts", [])]
    [Account(x).store(x, "name") for x in data.get("accounts", [])]
    Witnesses.cache_objects([Witness(x) for x in data.get("witnesses", [])])
    Sports.cache_objects([Sport(x) for x in data.get("sports", [])])
    EventGroups.cache_objects([EventGroup(x) for x in data.get("eventgroups", [])])
    Events.cache_objects([Event(x) for x in data.get("events", [])])
    BettingMarketGroups.cache_objects(
        [BettingMarketGroup(x) for x in data.get("bettingmarketgroups", [])]
    )
    BettingMarkets.cache_objects(
        [BettingMarket(x) for x in data.get("bettingmarkets", [])]
    )
    Rules.cache_objects([Rule(x) for x in data.get("rules", [])])
    [Bet(x) for x in data.get("bets", [])]

    proposals = []
    for proposal in data.get("proposals", []):
        ops = list()
        for _op in proposal["operations"]:
            for opName, op in _op.items():
                ops.append([operations[opName], op])
        # Proposal!
        proposal_id = proposal["proposal_id"]
        proposal_data = {
            "available_active_approvals": [],
            "available_key_approvals": [],
            "available_owner_approvals": [],
            "expiration_time": "2018-05-29T10:23:13",
            "id": proposal_id,
            "proposed_transaction": {
                "expiration": "2018-05-29T10:23:13",
                "extensions": [],
                "operations": ops,
                "ref_block_num": 0,
                "ref_block_prefix": 0,
            },
            "proposer": "1.2.7",
            "required_active_approvals": ["1.2.1"],
            "required_owner_approvals": [],
        }
        proposals.append(Proposal(proposal_data))

    Proposals.cache_objects(proposals, "1.2.1")
    Proposals.cache_objects(proposals, "witness-account")
