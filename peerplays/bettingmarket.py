from peerplays.instance import BlockchainInstance
from .exceptions import BettingMarketDoesNotExistException
from .blockchainobject import BlockchainObject


class BettingMarket(BlockchainObject):
    """ Read data about a Betting Market on the chain

        :param str identifier: Identifier
        :param peerplays blockchain_instance: PeerPlays() instance to use when
            accesing a RPC

    """
    type_id = 21

    def refresh(self):
        assert self.identifier[:5] == "1.21.",\
            "Identifier needs to be of form '1.21.xx'"
        data = self.blockchain.rpc.get_object(self.identifier)
        if not data:
            raise BettingMarketDoesNotExistException(self.identifier)
        super(BettingMarket, self).__init__(data)
        self.cached = True

    @property
    def bettingmarketgroup(self):
        from .bettingmarketgroup import BettingMarketGroup
        return BettingMarketGroup(self["group_id"])


class BettingMarkets(list, BlockchainInstance):
    """ List of all available BettingMarkets

        :param str betting_market_group_id: Market Group ID (``1.20.xxx``)
    """
    def __init__(self, betting_market_group_id, *args, **kwargs):
        BlockchainInstance.__init__(self, *args, **kwargs)
        self.bettingmarkets = self.blockchain.rpc.list_betting_markets(
            betting_market_group_id)

        super(BettingMarkets, self).__init__([
            BettingMarket(x, lazy=True, blockchain_instance=self.blockchain)
            for x in self.bettingmarkets
        ])
