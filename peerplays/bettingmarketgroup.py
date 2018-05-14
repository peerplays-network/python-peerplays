from peerplays.instance import BlockchainInstance
from .exceptions import BettingMarketGroupDoesNotExistException
from .blockchainobject import BlockchainObject, ObjectCache


class BettingMarketGroup(BlockchainObject):
    """ Read data about a Betting Market Group on the chain

        :param str identifier: Identifier
        :param peerplays blockchain_instance: PeerPlays() instance to use when
            accesing a RPC

    """
    type_id = 20

    def refresh(self):
        data = self.blockchain.rpc.get_object(self.identifier)
        if not data:
            raise BettingMarketGroupDoesNotExistException(self.identifier)
        super(BettingMarketGroup, self).__init__(data)
        self.cached = True

    @property
    def event(self):
        from .event import Event
        return Event(self["event_id"])

    @property
    def bettingmarkets(self):
        from .bettingmarket import BettingMarkets
        return BettingMarkets(self["id"])

    def resolve(self, results, **kwargs):
        return self.blockchain.betting_market_resolve(
            self["id"], results, **kwargs
        )


class BettingMarketGroups(list):
    """ List of all available BettingMarketGroups

        :param strevent_id: Event ID (``1.18.xxx``)
    """
    cache = ObjectCache()

    def __init__(self, event_id, *args, **kwargs):
        BlockchainInstance.__init__(self, *args, **kwargs)

        if event_id in BettingMarketGroups.cache:
            self.bettingmarketgroups = BettingMarketGroups.cache[event_id]
        else:
            self.bettingmarketgroups = self.blockchain.rpc.list_betting_market_groups(
                event_id)
            BettingMarketGroups.cache[event_id] = self.bettingmarketgroups

        super(BettingMarketGroups, self).__init__([
            BettingMarketGroup(
                x, lazy=False, blockchain_instance=self.blockchain)
            for x in self.bettingmarketgroups
        ])
