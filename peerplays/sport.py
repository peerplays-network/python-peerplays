from peerplays.instance import shared_peerplays_instance
from .exceptions import SportDoesNotExistException


class Sport(dict):
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
        self.peerplays = peerplays_instance or shared_peerplays_instance()
        self.cached = False

        if isinstance(identifier, str):
            self.identifier = identifier
            if not lazy:
                self.refresh()
        elif isinstance(identifier, dict):
            self.cached = False
            self.identifier = identifier.get("id")
            super(Sport, self).__init__(identifier)


    def refresh(self):
        assert self.identifier[:5] == "1.16.",\
            "Identifier needs to be of form '1.16.xx'"
        data = self.peerplays.rpc.get_object(self.identifier)
        if not data:
            raise SportDoesNotExistException(self.identifier)
        super(Sport, self).__init__(data)
        self.cached = True

    def __getitem__(self, key):
        if not self.cached:
            self.refresh()
        return super(Sport, self).__getitem__(key)

    def items(self):
        if not self.cached:
            self.refresh()
        return super(Sport, self).items()

    def __repr__(self):
        return "<Sport %s>" % str(self.identifier)

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
