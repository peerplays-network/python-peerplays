*****
Stati
*****

List of statis and types used within PeerPlays:

.. code-block:: python

    class BetType(Enum):
        options = [
            "back",
            "lay",
        ]


    class BettingMarketResolution(Enum):
        options = [
            "win",
            "not_win",
            "cancel",
            "BETTING_MARKET_RESOLUTION_COUNT",
        ]


    class BettingMarketStatus(Enum):
        options = [
            "unresolved",  # no grading  has been published for this betting market
            "frozen",      # bets are suspended, no bets allowed
            "graded",      # grading of win or not_win has been published
            "canceled",    # the betting market is canceled, no further bets are allowed
            "settled",     # the betting market has been paid out
            "BETTING_MARKET_STATUS_COUNT"
        ]


    class BettingMarketGroupStatus(Enum):
        options = [
            "upcoming",    # betting markets are accepting bets, will never go "in_play"
            "in_play",     # betting markets are delaying bets
            "closed",      # betting markets are no longer accepting bets
            "graded",      # witnesses have published win/not win for the betting markets
            "re_grading",  # initial win/not win grading has been challenged
            "settled",     # paid out
            "frozen",      # betting markets are not accepting bets
            "canceled",    # canceled
            "BETTING_MARKET_GROUP_STATUS_COUNT"
        ]


    class EventStatus(Enum):
        options = [
            "upcoming",     # Event has not started yet, betting is allowed
            "in_progress",  # Event is in progress, if "in-play" betting is enabled, bets will be delayed
            "frozen",       # Betting is temporarily disabled
            "finished",     # Event has finished, no more betting allowed
            "canceled",     # Event has been canceled, all betting markets have been canceled
            "settled",      # All betting markets have been paid out
            "STATUS_COUNT"
        ]
