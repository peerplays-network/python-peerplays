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
        self.id = id

        self.peerplays = peerplays_instance or shared_peerplays_instance()
        self.refresh()

    def refresh(self):
        a, b, c = self.id.split(".")
        assert int(a) == 1 and int(b) == 10, "Valid proposal ids are 1.10.x"
        proposal = self.peerplays.rpc.get_objects([self.id])
        if not any(proposal):
            raise ProposalDoesNotExistException
        super(Proposal, self).__init__(proposal[0])
