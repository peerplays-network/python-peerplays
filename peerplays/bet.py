from peerplays.instance import shared_peerplays_instance
from .exceptions import BetDoesNotExistException
from .blockchainobject import BlockchainObject


class Bet(BlockchainObject):
    """ Read data about a Bet on the chain

        :param str identifier: Identifier
        :param peerplays peerplays_instance: PeerPlays() instance to use when accesing a RPC

    """
    def __init__(
        self,
        identifier,
        peerplays_instance=None,
    ):
        super().__init__(
            identifier,
            peerplays_instance=peerplays_instance,
        )

    def refresh(self):
        assert self.identifier[:5] == "1.22.",\
            "Identifier needs to be of form '1.22.xx'"
        data = self.peerplays.rpc.get_object(self.identifier)
        if not data:
            raise BetDoesNotExistException(self.identifier)
        dict.__init__(data)
