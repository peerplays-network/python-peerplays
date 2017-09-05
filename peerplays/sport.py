from peerplays.instance import shared_peerplays_instance
from .exceptions import SportDoesNotExistException
from .blockchainobject import BlockchainObject


class Sport(BlockchainObject):
    """ Read data about a sport on the chain

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
        assert self.identifier[:5] == "1.16.",\
            "Identifier needs to be of form '1.16.xx'"
        data = self.peerplays.rpc.get_object(self.identifier)
        if not data:
            raise SportDoesNotExistException(self.identifier)
        super(Sport, self).__init__(data)
        self.cached = True

    @property
    def eventgroups(self):
        from .eventgroup import EventGroups
        return EventGroups(self["id"])


class Sports(list):
    """ List of all available sports
    """
    def __init__(self, peerplays_instance=None):
        self.peerplays = peerplays_instance or shared_peerplays_instance()
        self.sports = self.peerplays.rpc.list_sports()

        super(Sports, self).__init__([
            Sport(x, lazy=True, peerplays_instance=peerplays_instance)
            for x in self.sports
        ])
