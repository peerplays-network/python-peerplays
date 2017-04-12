from peerplays.instance import shared_peerplays_instance
from .exceptions import EventDoesNotExistException


class Event(dict):
    """ Read data about an event on the chain

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
        assert self.identifier[:5] == "1.19.",\
            "Identifier needs to be of form '1.19.xx'"
        data = self.peerplays.rpc.get_object(self.identifier)
        if not data:
            raise EventDoesNotExistException(self.identifier)
        dict.__init__(data)
