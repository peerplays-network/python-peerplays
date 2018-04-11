from .exceptions import BetDoesNotExistException
from .blockchainobject import BlockchainObject


class Bet(BlockchainObject):
    """ Read data about a Bet on the chain

        :param str identifier: Identifier
        :param peerplays blockchain_instance: PeerPlays() instance to use when accesing a RPC

    """
    type_id = 22

    def refresh(self):
        data = self.blockchain.rpc.get_object(self.identifier)
        if not data:
            raise BetDoesNotExistException(self.identifier)
        dict.__init__(self, data)
