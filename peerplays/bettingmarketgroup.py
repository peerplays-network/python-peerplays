from peerplays.instance import BlockchainInstance
from .exceptions import BettingMarketGroupDoesNotExistException
from .blockchainobject import BlockchainObject, BlockchainObjects
from .utils import map2dict

HANDICAP_MARKET_LABELS = ["hc", "1x2_hc"]
OVERUNDER_MARKET_LABELS = ["ou"]


class BettingMarketGroup(BlockchainObject):
    """ Read data about a Betting Market Group on the chain

        :param str identifier: Identifier
        :param peerplays blockchain_instance: PeerPlays() instance to use when
            accesing a RPC

    """

    type_id = 24

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
        return self.blockchain.betting_market_resolve(self["id"], results, **kwargs)

    def get_dynamic_type(self):
        assert self.is_dynamic()
        description = map2dict(self["description"])
        return description.get("_dynamic")

    def is_dynamic(self):
        description = map2dict(self["description"])
        return bool(description.get("_dynamic", False))

    def is_dynamic_type(self, other_type):
        our_type = self.get_dynamic_type()
        if our_type in HANDICAP_MARKET_LABELS:
            return other_type in HANDICAP_MARKET_LABELS
        else:
            return other_type in OVERUNDER_MARKET_LABELS


class BettingMarketGroups(BlockchainObjects, BlockchainInstance):
    """ List of all available BettingMarketGroups

        :param strevent_id: Event ID (``1.22.xxx``)
    """

    def __init__(self, event_id, *args, **kwargs):
        self.event_id = event_id
        BlockchainInstance.__init__(self, *args, **kwargs)
        BlockchainObjects.__init__(self, event_id, *args, **kwargs)

    def refresh(self, *args, **kwargs):
        self.bettingmarketgroups = self.blockchain.rpc.list_betting_market_groups(
            self.event_id
        )
        self.store(
            [
                BettingMarketGroup(x, lazy=False, blockchain_instance=self.blockchain)
                for x in self.bettingmarketgroups
            ],
            self.event_id,
        )
