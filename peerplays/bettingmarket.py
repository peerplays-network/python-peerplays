from peerplays.instance import shared_peerplays_instance
from .exceptions import BettingMarketDoesNotExistException


class BettingMarket(dict):
    """ Read data about a Betting Market on the chain

        :param str identifier: Identifier
        :param peerplays peerplays_instance: PeerPlays() instance to use when accesing a RPC

    """
    def __init__(
        self,
        identifier,
        lazy=False,
        peerplays_instance=None,
    ):
        self.peerplays = peerplays_instance or shared_peerplays_instance()
        self.cached = False

        if isinstance(identifier, str):
            self.identifier = identifier
            if not lazy:
                self.refresh()
        elif isinstance(identifier, dict):
            self.cached = False
            self.identifier = identifier.get("id")
            super(BettingMarket, self).__init__(identifier)

    def refresh(self):
        assert self.identifier[:5] == "1.21.",\
            "Identifier needs to be of form '1.21.xx'"
        data = self.peerplays.rpc.get_object(self.identifier)
        if not data:
            raise BettingMarketDoesNotExistException(self.identifier)
        super(BettingMarket, self).__init__(data)
        self.cached = True

    def __getitem__(self, key):
        if not self.cached:
            self.refresh()
        return super(BettingMarket, self).__getitem__(key)

    def items(self):
        if not self.cached:
            self.refresh()
        return super(BettingMarket, self).items()

    def __repr__(self):
        return "<BettingMarket %s>" % str(self.identifier)

    @property
    def bettingmarketgroup(self):
        from .bettingmarketgroup import BettingMarketGroup
        return BettingMarketGroup(self["group_id"])


class BettingMarkets(list):
    """ List of all available BettingMarkets

        :param str betting_market_group_id: Market Group ID (``1.20.xxx``)
    """
    def __init__(self, betting_market_group_id, peerplays_instance=None):
        self.peerplays = peerplays_instance or shared_peerplays_instance()
        self.bettingmarkets = self.peerplays.rpc.list_betting_markets(betting_market_group_id)

        super(BettingMarkets, self).__init__([
            BettingMarket(x, lazy=True, peerplays_instance=peerplays_instance)
            for x in self.bettingmarkets
        ])
