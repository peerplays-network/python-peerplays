from peerplays.instance import shared_peerplays_instance
from .account import Account
from .exceptions import WitnessDoesNotExistsException


class Witness(dict):
    """ Read data about a witness in the chain

        :param str account_name: Name of the witness
        :param peerplays peerplays_instance: PeerPlays() instance to use when accesing a RPC

    """
    def __init__(
        self,
        witness,
        peerplays_instance=None,
    ):
        self.witness = witness
        self.peerplays = peerplays_instance or shared_peerplays_instance()
        self.refresh()

    def refresh(self):
        account = Account(self.witness)
        witness = self.peerplays.rpc.get_witness_by_account(account["id"])
        if not witness:
            raise WitnessDoesNotExistsException
        super(Witness, self).__init__(witness)

    @property
    def account(self):
        return Account(self.witness)
