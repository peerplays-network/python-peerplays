import datetime
from getpass import getpass
from pprint import pprint
from peerplays import PeerPlays

ppy = PeerPlays(
    # this account creates the proposal
    proposer="init0",
    # Proposal needs to be approve within 1 hour
    proposal_expiration=60 * 2,
    # For testing, set this to true
    nobroadcast=False,
    # We want to bundle many operations into a single transaction
    bundle=True,
)
ppy.wallet.unlock(getpass())

ppy.sport_create([          # relative id 0.0.0
    ["de", "Fussball"],
    ["en", "Soccer"],
])

ppy.event_group_create([    # relative id 0.0.1
    ["de", "1. Bundesliga"],
    ["en", "First Country League"],
], sport_id="0.0.0")

ppy.event_create(           # relative id 0.0.2
    [["de", "Bundesliga"], ["en", "Germany Scoccer Championship"]],
    [["de", "Januar 2016"], ["en", "January 2016"]],  # season
    datetime.datetime(2016, 1, 1, 0, 0, 0),  # start_time
    event_group_id="0.0.3"   # event group
)

ppy.betting_market_rules_create(    # relative id 0.0.3
    [["de", "Meine Spielregeln"], ["en", "My betting market rules"]],
    [["de", "Erläuterungen"], ["en", "Description"]]
)

ppy.betting_market_group_create(  # relative id 0.0.4
    [["de", "Meine Market Group"], ["en", "My betting market group",]],
    event_id="0.0.2",
    rules_id="0.0.3",
)

ppy.betting_market_create(
    [["de", "Fürth gewinnt"], ["en", "Fürth wins"]],
    group_id="0.0.4",
)

ppy.betting_market_create(
    [["de", "Nürnberg gewinnt"], ["en", "Nuremberg wins"]],
    group_id="0.0.4",
)

# Broadcast the whole transaction
pprint(
    ppy.txbuffer.broadcast()
)
