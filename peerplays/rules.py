from .account import Account
from .exceptions import RuleDoesNotExistsException
from .blockchainobject import BlockchainObject


class Rules(BlockchainObject):
    """ Read data about a Rules object

        :param str identifier: Identifier for the rules
        :param peerplays peerplays_instance: PeerPlays() instance to use when accesing a RPC

    """

    type_id = 19

    def refresh(self):
        rule = self.peerplays.rpc.get_object(self.identifier)
        if not rule:
            raise RuleDoesNotExistsException
        super().__init__(rule)
