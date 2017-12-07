from peerplays.instance import shared_peerplays_instance
from .account import Account
from .exceptions import WitnessDoesNotExistsException
from .blockchainobject import BlockchainObject


class Witness(BlockchainObject):
    """ Read data about a witness in the chain

        :param str account_name: Name of the witness
        :param peerplays peerplays_instance: PeerPlays() instance to use when
            accesing a RPC

    """
    type_ids = [6, 2]

    def refresh(self):
        if self.test_valid_objectid(self.identifier):
            _, i, _ = self.identifier.split(".")
            if int(i) == 6:
                witness = self.peerplays.rpc.get_object(self.identifier)
            else:
                witness = self.peerplays.rpc.get_witness_by_account(
                    self.identifier)
        else:
            account = Account(
                self.identifier, peerplays_instance=self.peerplays)
            witness = self.peerplays.rpc.get_witness_by_account(account["id"])
        if not witness:
            raise WitnessDoesNotExistsException
        super(Witness, self).__init__(witness)

    @property
    def account(self):
        return Account(self["witness_account"])


class Witnesses(list):
    """ Obtain a list of **active** witnesses and the current schedule

        :param peerplays peerplays_instance: PeerPlays() instance to use when
            accesing a RPC
    """
    def __init__(self, peerplays_instance=None):
        self.peerplays = peerplays_instance or shared_peerplays_instance()
        self.schedule = self.peerplays.rpc.get_object(
            "2.12.0").get("current_shuffled_witnesses", [])

        super(Witnesses, self).__init__(
            [
                Witness(x, lazy=True, peerplays_instance=self.peerplays)
                for x in self.schedule
            ]
        )
