from peerplays.instance import shared_peerplays_instance
from .exceptions import CompetitorDoesNotExistException


class Competitor(dict):
    """ Read data about a competitor on the chain

        :param str identifier: Identifier
        :param peerplays peerplays_instance: PeerPlays() instance to use when accesing a RPC

    """
    def __init__(
        self,
        identifier,
        peerplays_instance=None,
    ):
        self.identifier = identifier
        self.peerplays = peerplays_instance or shared_peerplays_instance()
        self.refresh()

    def refresh(self):
        assert self.identifier[:5] == "1.17.",\
            "Identifier needs to be of form '1.17.xx'"
        data = self.peerplays.rpc.get_object(self.identifier)
        if not data:
            raise CompetitorDoesNotExistException(self.identifier)
        dict.__init__(data)
