from peerplays.instance import BlockchainInstance
from .exceptions import BettingMarketDoesNotExistException
from .blockchainobject import BlockchainObject, BlockchainObjects


class BettingMarket(BlockchainObject):
    """ Read data about a Betting Market on the chain

        :param str identifier: Identifier
        :param peerplays blockchain_instance: PeerPlays() instance to use when
            accesing a RPC

    """

    type_id = 25

    def refresh(self):
        assert (
            self.identifier[:5] == "1.25."
        ), "Identifier needs to be of form '1.25.xx'"
        data = self.blockchain.rpc.get_object(self.identifier)
        if not data:
            raise BettingMarketDoesNotExistException(self.identifier)
        super(BettingMarket, self).__init__(data)
        self.cached = True

    @property
    def bettingmarketgroup(self):
        from .bettingmarketgroup import BettingMarketGroup

        return BettingMarketGroup(self["group_id"])


class BettingMarkets(BlockchainObjects, BlockchainInstance):
    """ List of all available BettingMarkets

        :param str betting_market_group_id: Market Group ID (``1.24.xxx``)
    """

    def __init__(self, betting_market_group_id, *args, **kwargs):
        self.betting_market_group_id = betting_market_group_id
        BlockchainInstance.__init__(self, *args, **kwargs)
        BlockchainObjects.__init__(self, betting_market_group_id, *args, **kwargs)

    def refresh(self, *args, **kwargs):

        self.bettingmarkets = self.blockchain.rpc.list_betting_markets(
            self.betting_market_group_id
        )
        self.store(
            [
                BettingMarket(x, lazy=False, blockchain_instance=self.blockchain)
                for x in self.bettingmarkets
            ],
            self.betting_market_group_id,
        )
