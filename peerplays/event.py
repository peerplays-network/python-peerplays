from peerplays.instance import shared_peerplays_instance
from .exceptions import EventDoesNotExistException
from .blockchainobject import BlockchainObject


class Event(BlockchainObject):
    """ Read data about an event on the chain

        :param str identifier: Identifier
        :param peerplays peerplays_instance: PeerPlays() instance to use when
            accesing a RPC

    """
    type_id = 18

    def refresh(self):
        data = self.peerplays.rpc.get_object(self.identifier)
        if not data:
            raise EventDoesNotExistException(self.identifier)
        super(Event, self).__init__(data)
        self.cached = True

    @property
    def eventgroup(self):
        from .eventgroup import EventGroup
        return EventGroup(self["event_group_id"])

    @property
    def bettingmarketgroups(self):
        from .bettingmarketgroup import BettingMarketGroups
        return BettingMarketGroups(self["id"])


class Events(list):
    """ List of all available events in an eventgroup
    """
    def __init__(self, eventgroup_id, peerplays_instance=None):
        self.peerplays = peerplays_instance or shared_peerplays_instance()
        self.events = self.peerplays.rpc.list_events_in_group(eventgroup_id)

        super(Events, self).__init__([
            Event(x, lazy=True, peerplays_instance=peerplays_instance)
            for x in self.events
        ])
