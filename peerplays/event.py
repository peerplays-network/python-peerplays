from peerplays.instance import BlockchainInstance
from .exceptions import EventDoesNotExistException
from .blockchainobject import BlockchainObject, BlockchainObjects


class Event(BlockchainObject):
    """ Read data about an event on the chain

        :param str identifier: Identifier
        :param peerplays blockchain_instance: PeerPlays() instance to use when
            accesing a RPC

    """

    type_id = 22

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
            self["id"], status, scores=scores, **kwargs
        )


class Events(BlockchainObjects, BlockchainInstance):
    """ List of all available events in an eventgroup
    """

    def __init__(self, eventgroup_id, *args, **kwargs):
        self.eventgroup_id = eventgroup_id
        BlockchainInstance.__init__(self, *args, **kwargs)
        BlockchainObjects.__init__(self, eventgroup_id, *args, **kwargs)

    def refresh(self, *args, **kwargs):
        self.events = self.blockchain.rpc.list_events_in_group(self.eventgroup_id)
        self.store(
            [
                Event(x, lazy=False, blockchain_instance=self.blockchain)
                for x in self.events
            ],
            self.eventgroup_id,
        )
