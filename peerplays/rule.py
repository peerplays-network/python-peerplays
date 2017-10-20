from .instance import shared_peerplays_instance
from .exceptions import RuleDoesNotExistException
from .blockchainobject import BlockchainObject


class Rule(BlockchainObject):
    """ Read data about a Rule object

        :param str identifier: Identifier for the rule
        :param peerplays peerplays_instance: PeerPlays() instance to use
                when accesing a RPC

    """

    type_id = 19

    def refresh(self):
        rule = self.peerplays.rpc.get_object(self.identifier)
        if not rule:
            raise RuleDoesNotExistException
        super().__init__(rule)


class Rules(list):
    """ List of all Rules
    """
    def __init__(self, limit=1000, peerplays_instance=None):
        self.peerplays = peerplays_instance or shared_peerplays_instance()
        self.rules = self.peerplays.rpc.get_objects([
            "1.19.{}".format(id) for id in range(0, limit)
        ])

        super(Rules, self).__init__([
            Rule(x, peerplays_instance=peerplays_instance)
            for x in self.rules if x
        ])
