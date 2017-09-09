from peerplays.instance import shared_peerplays_instance
from .exceptions import SportDoesNotExistException
from .blockchainobject import BlockchainObject


class Sport(BlockchainObject):
    """ Read data about a sport on the chain

        :param str identifier: Identifier
        :param peerplays peerplays_instance: PeerPlays() instance to use when accesing a RPC

    """
    type_id = 16

    def refresh(self):
        data = self.peerplays.rpc.get_object(self.identifier)
        if not data:
            raise SportDoesNotExistException(self.identifier)
        super(Sport, self).__init__(data)

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
