import datetime
from pprint import pprint
from peerplays import PeerPlays

ppy = PeerPlays(
    # this account creates the proposal
    proposer="init0",
    # Proposal needs to be approve within 1 hour
    proposal_expiration=60 * 5,
    # For testing, set this to true
    nobroadcast=False,
    # We want to bundle many operations into a single transaction
    bundle=True,
)
ppy.wallet.unlock("")

ppy.betting_market_group_freeze(
    "1.20.0", True
)

# Broadcast the whole transaction
pprint(
    ppy.txbuffer.broadcast()
)
