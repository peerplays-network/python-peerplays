from peerplays.instance import shared_peerplays_instance
from .exceptions import BettingMarketGroupDoesNotExistException


class BettingMarketGroup(dict):
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
        self.peerplays = peerplays_instance or shared_peerplays_instance()
        self.cached = False

        if isinstance(identifier, str):
            self.identifier = identifier
            if not lazy:
                self.refresh()
        elif isinstance(identifier, dict):
            self.cached = False
            self.identifier = identifier.get("id")
            super(BettingMarketGroup, self).__init__(identifier)

    def refresh(self):
        assert self.identifier[:5] == "1.20.",\
            "Identifier needs to be of form '1.20.xx'"
        data = self.peerplays.rpc.get_object(self.identifier)
        if not data:
            raise BettingMarketGroupDoesNotExistException(self.identifier)
        super(BettingMarketGroup, self).__init__(data)
        self.cached = True

    def __getitem__(self, key):
        if not self.cached:
            self.refresh()
        return super(BettingMarketGroup, self).__getitem__(key)

    def items(self):
        if not self.cached:
            self.refresh()
        return super(BettingMarketGroup, self).items()

    def __repr__(self):
        return "<BettingMarketGroup %s>" % str(self.identifier)

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
