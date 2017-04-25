from peerplays.instance import shared_peerplays_instance
from .exceptions import BettingMarketGroupDoesNotExistException


class BettingMarketGroup(dict):
    """ Read data about a Betting Market Group on the chain

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
        assert self.identifier[:5] == "1.20.",\
            "Identifier needs to be of form '1.20.xx'"
        data = self.peerplays.rpc.get_object(self.identifier)
        if not data:
            raise BettingMarketGroupDoesNotExistException(self.identifier)
        dict.__init__(data)
