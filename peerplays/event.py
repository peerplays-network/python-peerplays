from peerplays.instance import shared_peerplays_instance
from .exceptions import EventDoesNotExistException
from .blockchainobject import BlockchainObject


class Event(BlockchainObject):
    """ Read data about an event on the chain

        :param str identifier: Identifier
        :param peerplays peerplays_instance: PeerPlays() instance to use when accesing a RPC

    """
    type_id = 19

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


class Events(list):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError("Missing API calls")
