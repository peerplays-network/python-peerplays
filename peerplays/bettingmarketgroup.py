from peerplays.instance import shared_peerplays_instance
from .exceptions import BettingMarketGroupDoesNotExistException
from .blockchainobject import BlockchainObject


class BettingMarketGroup(BlockchainObject):
    """ Read data about a Betting Market Group on the chain

        :param str identifier: Identifier
        :param peerplays peerplays_instance: PeerPlays() instance to use when accesing a RPC

    """
    def __init__(
        self,
        identifier,
        lazy=False,
        peerplays_instance=None,
    ):
        super().__init__(
            identifier,
            lazy=lazy,
            peerplays_instance=peerplays_instance,
        )

    def refresh(self):
        assert self.identifier[:5] == "1.20.",\
            "Identifier needs to be of form '1.20.xx'"
        data = self.peerplays.rpc.get_object(self.identifier)
        if not data:
            raise BettingMarketGroupDoesNotExistException(self.identifier)
        super(BettingMarketGroup, self).__init__(data)
        self.cached = True

    @property
    def event(self):
        from .event import Event
        return Event(self["event_id"])


class BettingMarketGroups(list):
    """ List of all available BettingMarketGroups

        :param strevent_id: Event ID (``1.19.xxx``)
    """
    def __init__(self, event_id, peerplays_instance=None):
        self.peerplays = peerplays_instance or shared_peerplays_instance()
        self.bettingmarketgroups = self.peerplays.rpc.list_betting_market_groups(event_id)

        super(BettingMarketGroups, self).__init__([
            BettingMarketGroup(x, lazy=True, peerplays_instance=peerplays_instance)
            for x in self.bettingmarketgroups
        ])
