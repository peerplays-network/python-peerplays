from peerplays.instance import BlockchainInstance
from .exceptions import EventDoesNotExistException
from .blockchainobject import BlockchainObject, ObjectCache


class Event(BlockchainObject):
    """ Read data about an event on the chain

        :param str identifier: Identifier
        :param peerplays blockchain_instance: PeerPlays() instance to use when
            accesing a RPC

    """
    type_id = 18

    def refresh(self):
        data = self.blockchain.rpc.get_object(self.identifier)
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

    def set_status(self, status, scores=[], **kwargs):
        return self.blockchain.event_update_status(
            self["id"],
            status,
            scores=scores,
            **kwargs
        )


class Events(list):
    """ List of all available events in an eventgroup
    """
    cache = ObjectCache()

    def __init__(self, eventgroup_id, *args, **kwargs):
        BlockchainInstance.__init__(self, *args, **kwargs)

        if eventgroup_id in Events.cache:
            self.events = Events.cache[eventgroup_id]
        else:
            self.events = self.blockchain.rpc.list_events_in_group(eventgroup_id)
            Events.cache[eventgroup_id] = self.events

        super(Events, self).__init__([
            Event(x, lazy=False, blockchain_instance=self.blockchain)
            for x in self.events
        ])
