from .instance import BlockchainInstance
from .exceptions import SportDoesNotExistException
from .blockchainobject import BlockchainObject, ObjectCache


class Sport(BlockchainObject):
    """ Read data about a sport on the chain

        :param str identifier: Identifier
        :param peerplays blockchain_instance: PeerPlays() instance to use when
            accesing a RPC

    """
    type_id = 16

    def refresh(self):
        data = self.blockchain.rpc.get_object(self.identifier)
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
    cache = ObjectCache()

    def __init__(self, **kwargs):
        BlockchainInstance.__init__(self, **kwargs)

        if "sports" in Sports.cache:
            self.sports = Sports.cache["sports"]
        else:
            self.sports = self.blockchain.rpc.list_sports()
            Sports.cache["sports"] = self.sports

        super(Sports, self).__init__([
            Sport(x, lazy=False, blockchain_instance=self.blockchain)
            for x in self.sports
        ])
