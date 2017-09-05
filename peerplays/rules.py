from .account import Account
from .exceptions import RuleDoesNotExistsException
from .blockchainobject import BlockchainObject


class Rules(BlockchainObject):
    """ Read data about a Rules object

        :param str identifier: Identifier for the rules
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
        a, b, _ = self.identifier.split(".")
        assert int(a) == 1 and int(b) == 19, "Rules id's need to be 1.19.x!"
        rule = self.peerplays.rpc.get_object(self.identifier)
        if not rule:
            raise RuleDoesNotExistsException
        super().__init__(rule)
