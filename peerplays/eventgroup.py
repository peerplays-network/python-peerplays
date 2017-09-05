from peerplays.instance import shared_peerplays_instance
from .exceptions import EventGroupDoesNotExistException
from .blockchainobject import BlockchainObject


class EventGroup(BlockchainObject):
    """ Read data about an event group on the chain

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
        assert self.identifier[:5] == "1.18.",\
            "Identifier needs to be of form '1.18.xx'"
        data = self.peerplays.rpc.get_object(self.identifier)
        if not data:
            raise EventGroupDoesNotExistException(self.identifier)
        super(EventGroup, self).__init__(data)
        self.cached = True

    @property
    def sport(self):
        from .sport import Sport
        return Sport(self["sport_id"])


class EventGroups(list):
    """ List of all available EventGroups

        :param str sport_id: Sport ID (``1.16.xxx``)
    """
    def __init__(self, sport_id, peerplays_instance=None):
        self.peerplays = peerplays_instance or shared_peerplays_instance()
        self.eventgroups = self.peerplays.rpc.list_event_groups(sport_id)

        super(EventGroups, self).__init__([
            EventGroup(x, lazy=True, peerplays_instance=peerplays_instance)
            for x in self.eventgroups
        ])
