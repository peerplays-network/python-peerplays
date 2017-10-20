from peerplays.instance import shared_peerplays_instance
from .account import Account
from .exceptions import CommitteeMemberDoesNotExistsException
from .blockchainobject import BlockchainObject


class Committee(BlockchainObject):
    """ Read data about a Committee Member in the chain

        :param str member: Name of the Committee Member
        :param peerplays peerplays_instance: PeerPlays() instance to use when accesing a RPC
        :param bool lazy: Use lazy loading

    """
    type_id = 5

    def refresh(self):
        account = Account(self.identifier)
        member = self.peerplays.rpc.get_committee_member_by_account(account["id"])
        if not member:
            raise CommitteeMemberDoesNotExistsException
        super(Committee, self).__init__(member)
        self.account_id = account["id"]

    @property
    def account(self):
        return Account(self.account_id)
