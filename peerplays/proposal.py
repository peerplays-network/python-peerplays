from .instance import shared_peerplays_instance
from .account import Account
from .exceptions import ProposalDoesNotExistException
import logging
log = logging.getLogger(__name__)


class Proposal(dict):
    """ Read data about a Proposal Balance in the chain

        :param str id: Id of the proposal
        :param peerplays peerplays_instance: Peerplays() instance to use when accesing a RPC

    """
    def __init__(
        self,
        id,
        peerplays_instance=None,
    ):
        self.peerplays = peerplays_instance or shared_peerplays_instance()
        if isinstance(id, str):
            self.id = id
            self.refresh()
        elif isinstance(id, dict) and "id" in id:
            self.id = id["id"]
            a, b, c = self.id.split(".")
            assert int(a) == 1 and int(b) == 10, "Valid proposal ids are 1.10.x"
            super(Proposal, self).__init__(id)

    def refresh(self):
        a, b, c = self.id.split(".")
        assert int(a) == 1 and int(b) == 10, "Valid proposal ids are 1.10.x"
        proposal = self.peerplays.rpc.get_objects([self.id])
        if not any(proposal):
            raise ProposalDoesNotExistException
        super(Proposal, self).__init__(proposal[0])


class Proposals(list):
    """ Obtain a list of pending proposals for an account

        :param str account: Account name
        :param peerplays peerplays_instance: PeerPlays() instance to use when accesing a RPC
    """
    def __init__(self, account, peerplays_instance=None):
        self.peerplays = peerplays_instance or shared_peerplays_instance()

        account = Account(account)
        proposals = self.peerplays.rpc.get_proposed_transactions(account["id"])

        super(Proposals, self).__init__(
            [
                Proposal(x, peerplays_instance=self.peerplays)
                for x in proposals
            ]
        )
