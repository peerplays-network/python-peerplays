from peerplays.instance import BlockchainInstance
from .exceptions import EventGroupDoesNotExistException
from .blockchainobject import BlockchainObject, ObjectCache


class EventGroup(BlockchainObject):
    """ Read data about an event group on the chain

        :param str identifier: Identifier
        :param peerplays blockchain_instance: PeerPlays() instance to use when
            accesing a RPC

    """
    type_id = 17

    def refresh(self):
        data = self.blockchain.rpc.get_object(self.identifier)
        if not data:
            raise EventGroupDoesNotExistException(self.identifier)
        super(EventGroup, self).__init__(data)
        self.cached = True

    @property
    def sport(self):
        from .sport import Sport
        return Sport(self["sport_id"])

    @property
    def events(self):
        from .event import Events
        return Events(self["id"])


class EventGroups(list):
    """ List of all available EventGroups

        :param str sport_id: Sport ID (``1.16.xxx``)
    """
    cache = ObjectCache()

    def __init__(self, sport_id, *args, **kwargs):
        BlockchainInstance.__init__(self, *args, **kwargs)
        if sport_id in EventGroups.cache:
            self.eventgroups = EventGroups.cache[sport_id]
        else:
            self.eventgroups = self.blockchain.rpc.list_event_groups(sport_id)
            EventGroups.cache[sport_id] = self.eventgroups

        super(EventGroups, self).__init__([
            EventGroup(x, lazy=False, blockchain_instance=self.blockchain)
            for x in self.eventgroups
        ])
