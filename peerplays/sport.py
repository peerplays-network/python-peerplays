from .instance import BlockchainInstance
from .exceptions import SportDoesNotExistException
from .blockchainobject import BlockchainObject, BlockchainObjects


class Sport(BlockchainObject):
    """ Read data about a sport on the chain

        :param str identifier: Identifier
        :param peerplays blockchain_instance: PeerPlays() instance to use when
            accesing a RPC

    """

    type_id = 20

    def refresh(self):
        data = self.blockchain.rpc.get_object(self.identifier)
        if not data:
            raise SportDoesNotExistException(self.identifier)
        super(Sport, self).__init__(data)

    @property
    def eventgroups(self):
        from .eventgroup import EventGroups

        return EventGroups(self["id"])


class Sports(BlockchainObjects, BlockchainInstance):
    """ List of all available sports
    """

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

    def refresh(self, *args, **kargs):
        self._sports = self.blockchain.rpc.list_sports()
        self.store(
            [
                Sport(x, lazy=False, blockchain_instance=self.blockchain)
                for x in self._sports
            ]
        )

    @property
    def sports(self):
        """ DEPRECATED
        """
        return list(self)
