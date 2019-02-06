from peerplays.instance import BlockchainInstance
from .exceptions import EventGroupDoesNotExistException
from .blockchainobject import BlockchainObject, BlockchainObjects


class EventGroup(BlockchainObject):
    """ Read data about an event group on the chain

        :param str identifier: Identifier
        :param peerplays blockchain_instance: PeerPlays() instance to use when
            accesing a RPC

    """

    type_id = 21

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


class EventGroups(BlockchainObjects, BlockchainInstance):
    """ List of all available EventGroups

        :param str sport_id: Sport ID (``1.20.xxx``)
    """

    def __init__(self, sport_id, *args, **kwargs):
        self.sport_id = sport_id
        BlockchainInstance.__init__(self, *args, **kwargs)
        BlockchainObjects.__init__(self, sport_id, *args, **kwargs)

    def refresh(self, *args, **kwargs):
        self.eventgroups = self.blockchain.rpc.list_event_groups(self.sport_id)
        self.store(
            [
                EventGroup(x, lazy=False, blockchain_instance=self.blockchain)
                for x in self.eventgroups
            ],
            self.sport_id,
        )
