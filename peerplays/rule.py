from .instance import BlockchainInstance
from .exceptions import RuleDoesNotExistException
from .blockchainobject import BlockchainObject, ObjectCache


class Rule(BlockchainObject):
    """ Read data about a Rule object

        :param str identifier: Identifier for the rule
        :param peerplays blockchain_instance: PeerPlays() instance to use
                when accesing a RPC

    """

    type_id = 19

    def refresh(self):
        rule = self.blockchain.rpc.get_object(self.identifier)
        if not rule:
            raise RuleDoesNotExistException
        super().__init__(rule)

    @property
    def grading(self):
        import json
        from .utils import map2dict
        desc = map2dict(self["description"])
        assert "grading" in desc, "Rule {} has no grading!".format(
            self["id"])
        grading = json.loads(desc.get("grading", {}))
        assert "metric" in grading
        assert "resolutions" in grading
        return grading


class Rules(list):
    """ List of all Rules
    """
    cache = ObjectCache()

    def __init__(self, limit=1000, **kwargs):
        BlockchainInstance.__init__(self, **kwargs)

        if "rules" in Rules.cache:
            self.rules = Rules.cache["rules"]
        else:
            self.rules = self.blockchain.rpc.get_objects([
                "1.19.{}".format(id) for id in range(0, limit)
            ])
            Rules.cache["rules"] = self.rules

        super(Rules, self).__init__([
            Rule(x, lazy=False, blockchain_instance=self.blockchain)
            for x in self.rules if x
        ])
