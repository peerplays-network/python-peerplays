from .account import Account
from .exceptions import GenesisBalanceDoesNotExistsException
from .instance import BlockchainInstance
from .blockchainobject import BlockchainObject

from peerplaysbase.account import Address, PublicKey
from peerplaysbase import operations


class GenesisBalance(BlockchainObject):
    """ Read data about a Committee Member in the chain

        :param str member: Name of the Committee Member
        :param peerplays blockchain_instance: PeerPlays() instance to use when
            accesing a RPC
        :param bool lazy: Use lazy loading

    """
    type_id = 15

    def refresh(self):
        balance = self.blockchain.rpc.get_object(self.identifier)
        if not balance:
            raise GenesisBalanceDoesNotExistsException
        super(GenesisBalance, self).__init__(
            balance, blockchain_instance=self.blockchain)

    def claim(self, account=None, **kwargs):
        """ Claim a balance from the genesis block

            :param str balance_id: The identifier that identifies the balance
                to claim (1.15.x)
            :param str account: (optional) the account that owns the bet
                (defaults to ``default_account``)
        """
        from peerplaysbase.account import Address, PublicKey
        if not account:
            if "default_account" in self.blockchain.config:
                account = self.blockchain.config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        account = Account(account)
        pubkeys = self.blockchain.wallet.getPublicKeys()
        addresses = dict()
        for p in pubkeys:
            pubkey = PublicKey(p)
            addresses[str(Address.from_pubkey(pubkey, compressed=False, version=0))] = pubkey
            addresses[str(Address.from_pubkey(pubkey, compressed=True, version=0))] = pubkey
            addresses[str(Address.from_pubkey(pubkey, compressed=False, version=56))] = pubkey
            addresses[str(Address.from_pubkey(pubkey, compressed=True, version=56))] = pubkey

        if self["owner"] not in addresses.keys():
            raise MissingKeyError(
                "Need key for address {}".format(self["owner"]))

        op = operations.Balance_claim(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "deposit_to_account": account["id"],
            "balance_to_claim": self["id"],
            "balance_owner_key": addresses[self["owner"]],
            "total_claimed": self["balance"],
            "prefix": self.blockchain.prefix
        })
        signers = [
            account["name"],               # The fee payer and receiver account
            addresses.get(self["owner"])   # The genesis balance!
        ]
        return self.blockchain.finalizeOp(op, signers, "active", **kwargs)


class GenesisBalances(list):
    """ List genesis balances that can be claimed from the
        keys in the wallet
    """
    def __init__(self, **kwargs):
        BlockchainInstance.__init__(self, **kwargs)

        pubkeys = self.blockchain.wallet.getPublicKeys()
        addresses = list()
        for p in pubkeys:
            pubkey = PublicKey(p)
            addresses.append(str(Address.from_pubkey(pubkey, compressed=False, version=0)))
            addresses.append(str(Address.from_pubkey(pubkey, compressed=True, version=0)))
            addresses.append(str(Address.from_pubkey(pubkey, compressed=False, version=56)))
            addresses.append(str(Address.from_pubkey(pubkey, compressed=True, version=56)))

        balancess = self.blockchain.rpc.get_balance_objects(addresses)

        super(GenesisBalances, self).__init__(
            [
                GenesisBalance(x, **kwargs, blockchain_instance=self.blockchain)
                for x in balancess
            ]
        )
