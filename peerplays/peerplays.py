import logging

from datetime import datetime
from peerplaysapi.node import PeerPlaysNodeRPC
from peerplaysbase.account import PublicKey
from peerplaysbase import operations
from .asset import Asset
from .account import Account
from .amount import Amount
from .witness import Witness
from .committee import Committee
from .storage import configStorage as config
from .sport import Sport
from .eventgroup import EventGroup
from .event import Event
from .rule import Rule
from .bettingmarketgroup import BettingMarketGroup
from .bettingmarket import BettingMarket
from .bet import Bet
from .genesisbalance import GenesisBalance

from .exceptions import (
    AccountExistsException,
    MissingKeyError
)
from .wallet import Wallet
from .transactionbuilder import TransactionBuilder, ProposalBuilder
from .utils import formatTime, test_proposal_in_buffer

log = logging.getLogger(__name__)


class PeerPlays(object):
    """ Connect to the PeerPlays network.

        :param str node: Node to connect to *(optional)*
        :param str rpcuser: RPC user *(optional)*
        :param str rpcpassword: RPC password *(optional)*
        :param bool nobroadcast: Do **not** broadcast a transaction!
            *(optional)*
        :param bool debug: Enable Debugging *(optional)*
        :param array,dict,string keys: Predefine the wif keys to shortcut the
            wallet database *(optional)*
        :param bool offline: Boolean to prevent connecting to network (defaults
            to ``False``) *(optional)*
        :param str proposer: Propose a transaction using this proposer
            *(optional)*
        :param int proposal_expiration: Expiration time (in seconds) for the
            proposal *(optional)*
        :param int proposal_review: Review period (in seconds) for the proposal
            *(optional)*
        :param int expiration: Delay in seconds until transactions are supposed
            to expire *(optional)*
        :param str blocking: Wait for broadcasted transactions to be included
            in a block and return full transaction (can be "head" or
            "irrversible")
        :param bool bundle: Do not broadcast transactions right away, but allow
            to bundle operations *(optional)*

        Three wallet operation modes are possible:

        * **Wallet Database**: Here, the peerplayslibs load the keys from the
          locally stored wallet SQLite database (see ``storage.py``).
          To use this mode, simply call ``PeerPlays()`` without the
          ``keys`` parameter
        * **Providing Keys**: Here, you can provide the keys for
          your accounts manually. All you need to do is add the wif
          keys for the accounts you want to use as a simple array
          using the ``keys`` parameter to ``PeerPlays()``.
        * **Force keys**: This more is for advanced users and
          requires that you know what you are doing. Here, the
          ``keys`` parameter is a dictionary that overwrite the
          ``active``, ``owner``, or ``memo`` keys for
          any account. This mode is only used for *foreign*
          signatures!

        If no node is provided, it will connect to the node of
        http://ppy-node.peerplays.eu. It is **highly** recommended that you
        pick your own node instead. Default settings can be changed with:

        .. code-block:: python

            peerplays set node <host>

        where ``<host>`` starts with ``ws://`` or ``wss://``.

        The purpose of this class it to simplify interaction with
        PeerPlays.

        The idea is to have a class that allows to do this:

        .. code-block:: python

            from peerplays import PeerPlays
            peerplays = PeerPlays()
            print(peerplays.info())

        All that is requires is for the user to have added a key with
        ``peerplays``

        .. code-block:: bash

            peerplays addkey

        and setting a default author:

        .. code-block:: bash

            peerplays set default_account xeroc

        This class also deals with edits, votes and reading content.
    """

    def __init__(self,
                 node="",
                 rpcuser="",
                 rpcpassword="",
                 debug=False,
                 **kwargs):

        # More specific set of APIs to register to
        if "apis" not in kwargs:
            kwargs["apis"] = [
                "database",
                "network_broadcast",
            ]

        self.rpc = None
        self.debug = debug

        self.offline = bool(kwargs.get("offline", False))
        self.nobroadcast = bool(kwargs.get("nobroadcast", False))
        self.unsigned = bool(kwargs.get("unsigned", False))
        self.expiration = int(kwargs.get("expiration", 30))
        self.bundle = bool(kwargs.get("bundle", False))
        self.blocking = bool(kwargs.get("blocking", False))

        # Legacy Proposal attributes
        self.proposer = kwargs.get("proposer", None)
        self.proposal_expiration = int(
            kwargs.get("proposal_expiration", 60 * 60 * 24))
        self.proposal_review = int(kwargs.get("proposal_review", 0))

        # Store config for access through other Classes
        self.config = config

        if not self.offline:
            self.connect(node=node,
                         rpcuser=rpcuser,
                         rpcpassword=rpcpassword,
                         **kwargs)

        # txbuffers/propbuffer are initialized and cleared
        self.clear()

        self.wallet = Wallet(blockchain_instance=self, **kwargs)

    # -------------------------------------------------------------------------
    # Basic Calls
    # -------------------------------------------------------------------------
    def connect(self,
                node="",
                rpcuser="",
                rpcpassword="",
                **kwargs):
        """ Connect to PeerPlays network (internal use only)
        """
        if not node:
            if "node" in config:
                node = config["node"]
            else:
                raise ValueError("A PeerPlays node needs to be provided!")

        if not rpcuser and "rpcuser" in config:
            rpcuser = config["rpcuser"]

        if not rpcpassword and "rpcpassword" in config:
            rpcpassword = config["rpcpassword"]

        self.rpc = PeerPlaysNodeRPC(node, rpcuser, rpcpassword, **kwargs)

    def is_connected(self):
        return bool(self.rpc)

    @property
    def prefix(self):
        return self.rpc.chain_params["prefix"]

    def set_default_account(self, account):
        """ Set the default account to be used
        """
        Account(account)
        config["default_account"] = account

    def set_blocking(self, block=True):
        """ This sets a flag that forces the broadcast to block until the
            transactions made it into a block
        """
        self.blocking = block

    def finalizeOp(self, ops, account, permission, **kwargs):
        """ This method obtains the required private keys if present in
            the wallet, finalizes the transaction, signs it and
            broadacasts it

            :param operation ops: The operation (or list of operaions) to
                broadcast
            :param operation account: The account that authorizes the
                operation
            :param string permission: The required permission for
                signing (active, owner, posting)
            :param object append_to: This allows to provide an instance of
                ProposalsBuilder (see :func:`peerplays.new_proposal`) or
                TransactionBuilder (see :func:`peerplays.new_tx()`) to specify
                where to put a specific operation.

            ... note:: ``append_to`` is exposed to every method used in the
                PeerPlays class

            ... note::

                If ``ops`` is a list of operation, they all need to be
                signable by the same key! Thus, you cannot combine ops
                that require active permission with ops that require
                posting permission. Neither can you use different
                accounts for different operations!

            ... note:: This uses ``peerplays.txbuffer`` as instance of
                :class:`peerplays.transactionbuilder.TransactionBuilder`.
                You may want to use your own txbuffer
        """
        if "append_to" in kwargs and kwargs["append_to"]:
            if self.proposer:
                log.warn(
                    "You may not use append_to and peerplays.proposer at "
                    "the same time. Append peerplays.new_proposal(..) instead"
                )
            # Append to the append_to and return
            append_to = kwargs["append_to"]
            parent = append_to.get_parent()
            assert isinstance(append_to, (TransactionBuilder, ProposalBuilder))
            append_to.appendOps(ops)
            # Add the signer to the buffer so we sign the tx properly
            if isinstance(append_to, ProposalBuilder):
                parent.appendSigner(append_to.proposer, permission)
            else:
                parent.appendSigner(account, permission)
            # This returns as we used append_to, it does NOT broadcast, or sign
            return append_to.get_parent()
        elif self.proposer:
            # Legacy proposer mode!
            proposal = self.proposal()
            proposal.set_proposer(self.proposer)
            proposal.set_expiration(self.proposal_expiration)
            proposal.set_review(self.proposal_review)
            proposal.appendOps(ops)
            # Go forward to see what the other options do ...
        else:
            # Append tot he default buffer
            self.txbuffer.appendOps(ops)

        # The API that obtains the fee only allows to specify one particular
        # fee asset for all operations in that transaction even though the
        # blockchain itself could allow to pay multiple operations with
        # different fee assets.
        if "fee_asset" in kwargs and kwargs["fee_asset"]:
            fee_asset = Asset(kwargs["fee_asset"], blockchain_instance=self)
            self.txbuffer.set_fee_asset(fee_asset)

        # Add signing information, signer, sign and optionally broadcast
        if self.unsigned:
            # In case we don't want to sign anything
            self.txbuffer.addSigningInformation(account, permission)
            return self.txbuffer
        elif self.bundle:
            # In case we want to add more ops to the tx (bundle)
            self.txbuffer.appendSigner(account, permission)
            return self.txbuffer.json()
        else:
            # default behavior: sign + broadcast
            self.txbuffer.appendSigner(account, permission)
            self.txbuffer.sign()
            return self.txbuffer.broadcast()

    def sign(self, tx=None, wifs=[]):
        """ Sign a provided transaction witht he provided key(s)

            :param dict tx: The transaction to be signed and returned
            :param string wifs: One or many wif keys to use for signing
                a transaction. If not present, the keys will be loaded
                from the wallet as defined in "missing_signatures" key
                of the transactions.
        """
        if tx:
            txbuffer = TransactionBuilder(tx, blockchain_instance=self)
        else:
            txbuffer = self.txbuffer
        txbuffer.appendWif(wifs)
        txbuffer.appendMissingSignatures()
        txbuffer.sign()
        return txbuffer.json()

    def broadcast(self, tx=None):
        """ Broadcast a transaction to the PeerPlays network

            :param tx tx: Signed transaction to broadcast
        """
        if tx:
            # If tx is provided, we broadcast the tx
            return TransactionBuilder(
                tx, blockchain_instance=self).broadcast()
        else:
            return self.txbuffer.broadcast()

    def info(self):
        """ Returns the global properties
        """
        return self.rpc.get_dynamic_global_properties()

    # -------------------------------------------------------------------------
    # Wallet stuff
    # -------------------------------------------------------------------------
    def newWallet(self, pwd):
        """ Create a new wallet. This method is basically only calls
            :func:`peerplays.wallet.create`.

            :param str pwd: Password to use for the new wallet
            :raises peerplays.exceptions.WalletExists: if there is already a
                wallet created
        """
        return self.wallet.create(pwd)

    def unlock(self, *args, **kwargs):
        """ Unlock the internal wallet
        """
        return self.wallet.unlock(*args, **kwargs)

    # -------------------------------------------------------------------------
    # Transaction Buffers
    # -------------------------------------------------------------------------
    @property
    def txbuffer(self):
        """ Returns the currently active tx buffer
        """
        return self.tx()

    @property
    def propbuffer(self):
        """ Return the default proposal buffer
        """
        return self.proposal()

    def tx(self):
        """ Returns the default transaction buffer
        """
        return self._txbuffers[0]

    def proposal(
        self,
        proposer=None,
        proposal_expiration=None,
        proposal_review=None
    ):
        """ Return the default proposal buffer

            ... note:: If any parameter is set, the default proposal
               parameters will be changed!
        """
        if not self._propbuffer:
            return self.new_proposal(
                self.tx(),
                proposer,
                proposal_expiration,
                proposal_review
            )
        if proposer:
            self._propbuffer[0].set_proposer(proposer)
        if proposal_expiration:
            self._propbuffer[0].set_expiration(proposal_expiration)
        if proposal_review:
            self._propbuffer[0].set_review(proposal_review)
        return self._propbuffer[0]

    def new_proposal(
        self,
        parent=None,
        proposer=None,
        proposal_expiration=None,
        proposal_review=None,
        **kwargs
    ):
        if not parent:
            parent = self.tx()
        if not proposal_expiration:
            proposal_expiration = self.proposal_expiration

        if not proposal_review:
            proposal_review = self.proposal_review

        if not proposer:
            if "default_account" in config:
                proposer = config["default_account"]

        # Else, we create a new object
        proposal = ProposalBuilder(
            proposer,
            proposal_expiration,
            proposal_review,
            blockchain_instance=self,
            parent=parent,
            **kwargs
        )
        if parent:
            parent.appendOps(proposal)
        self._propbuffer.append(proposal)
        return proposal

    def new_tx(self, *args, **kwargs):
        """ Let's obtain a new txbuffer

            :returns int txid: id of the new txbuffer
        """
        builder = TransactionBuilder(
            *args,
            blockchain_instance=self,
            **kwargs
        )
        self._txbuffers.append(builder)
        return builder

    def clear(self):
        self._txbuffers = []
        self._propbuffer = []
        # Base/Default proposal/tx buffers
        self.new_tx()
        # self.new_proposal()

    # -------------------------------------------------------------------------
    # Simple Transfer
    # -------------------------------------------------------------------------
    def transfer(self, to, amount, asset, memo="", account=None, **kwargs):
        """ Transfer an asset to another account.

            :param str to: Recipient
            :param float amount: Amount to transfer
            :param str asset: Asset to transfer
            :param str memo: (optional) Memo, may begin with `#` for encrypted
                messaging
            :param str account: (optional) the source account for the transfer
                if not ``default_account``
        """
        from .memo import Memo
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        account = Account(account, blockchain_instance=self)
        amount = Amount(amount, asset, blockchain_instance=self)
        to = Account(to, blockchain_instance=self)

        memoObj = Memo(
            from_account=account,
            to_account=to,
            blockchain_instance=self
        )

        op = operations.Transfer(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "from": account["id"],
            "to": to["id"],
            "amount": {
                "amount": int(amount),
                "asset_id": amount.asset["id"]
            },
            "memo": memoObj.encrypt(memo),
            "prefix": self.prefix
        })
        return self.finalizeOp(op, account, "active", **kwargs)

    # -------------------------------------------------------------------------
    # Account related calls
    # -------------------------------------------------------------------------
    def create_account(
        self,
        account_name,
        registrar=None,
        referrer="1.2.0",
        referrer_percent=50,
        owner_key=None,
        active_key=None,
        memo_key=None,
        password=None,
        additional_owner_keys=[],
        additional_active_keys=[],
        additional_owner_accounts=[],
        additional_active_accounts=[],
        proxy_account="proxy-to-self",
        storekeys=True,
        **kwargs
    ):
        """ Create new account on PeerPlays

            The brainkey/password can be used to recover all generated keys
            (see `peerplaysbase.account` for more details.

            By default, this call will use ``default_account`` to
            register a new name ``account_name`` with all keys being
            derived from a new brain key that will be returned. The
            corresponding keys will automatically be installed in the
            wallet.

            .. warning:: Don't call this method unless you know what
                          you are doing! Be sure to understand what this
                          method does and where to find the private keys
                          for your account.

            .. note:: Please note that this imports private keys
                      (if password is present) into the wallet by
                      default. However, it **does not import the owner
                      key** for security reasons. Do NOT expect to be
                      able to recover it from the wallet if you lose
                      your password!

            :param str account_name: (**required**) new account name
            :param str registrar: which account should pay the registration fee
                                (defaults to ``default_account``)
            :param str owner_key: Main owner key
            :param str active_key: Main active key
            :param str memo_key: Main memo_key
            :param str password: Alternatively to providing keys, one
                                 can provide a password from which the
                                 keys will be derived
            :param array additional_owner_keys:  Additional owner public keys
            :param array additional_active_keys: Additional active public keys
            :param array additional_owner_accounts: Additional owner account
                names
            :param array additional_active_accounts: Additional acctive account
                names
            :param bool storekeys: Store new keys in the wallet (default:
                ``True``)
            :raises AccountExistsException: if the account already exists on
                the blockchain

        """
        if not registrar and config["default_account"]:
            registrar = config["default_account"]
        if not registrar:
            raise ValueError(
                "Not registrar account given. Define it with " +
                "registrar=x, or set the default_account using 'peerplays'")
        if password and (owner_key or active_key or memo_key):
            raise ValueError(
                "You cannot use 'password' AND provide keys!"
            )

        try:
            Account(account_name, blockchain_instance=self)
            raise AccountExistsException
        except:
            pass

        referrer = Account(referrer, blockchain_instance=self)
        registrar = Account(registrar, blockchain_instance=self)

        " Generate new keys from password"
        from peerplaysbase.account import PasswordKey, PublicKey
        if password:
            active_key = PasswordKey(account_name, password, role="active")
            owner_key = PasswordKey(account_name, password, role="owner")
            memo_key = PasswordKey(account_name, password, role="memo")
            active_pubkey = active_key.get_public_key()
            owner_pubkey = owner_key.get_public_key()
            memo_pubkey = memo_key.get_public_key()
            active_privkey = active_key.get_private_key()
            # owner_privkey   = owner_key.get_private_key()
            memo_privkey = memo_key.get_private_key()
            # store private keys
            if storekeys:
                # self.wallet.addPrivateKey(str(owner_privkey))
                self.wallet.addPrivateKey(str(active_privkey))
                self.wallet.addPrivateKey(str(memo_privkey))
        elif (owner_key and active_key and memo_key):
            active_pubkey = PublicKey(
                active_key, prefix=self.prefix)
            owner_pubkey = PublicKey(
                owner_key, prefix=self.prefix)
            memo_pubkey = PublicKey(
                memo_key, prefix=self.prefix)
        else:
            raise ValueError(
                "Call incomplete! Provide either a password or public keys!"
            )
        owner = format(owner_pubkey, self.prefix)
        active = format(active_pubkey, self.prefix)
        memo = format(memo_pubkey, self.prefix)

        owner_key_authority = [[owner, 1]]
        active_key_authority = [[active, 1]]
        owner_accounts_authority = []
        active_accounts_authority = []

        # additional authorities
        for k in additional_owner_keys:
            owner_key_authority.append([k, 1])
        for k in additional_active_keys:
            active_key_authority.append([k, 1])

        for k in additional_owner_accounts:
            addaccount = Account(k, blockchain_instance=self)
            owner_accounts_authority.append([addaccount["id"], 1])
        for k in additional_active_accounts:
            addaccount = Account(k, blockchain_instance=self)
            active_accounts_authority.append([addaccount["id"], 1])

        # voting account
        voting_account = Account(
            proxy_account or "proxy-to-self", blockchain_instance=self)

        op = {
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "registrar": registrar["id"],
            "referrer": referrer["id"],
            "referrer_percent": int(referrer_percent * 100),
            "name": account_name,
            'owner': {'account_auths': owner_accounts_authority,
                      'key_auths': owner_key_authority,
                      "address_auths": [],
                      'weight_threshold': 1},
            'active': {'account_auths': active_accounts_authority,
                       'key_auths': active_key_authority,
                       "address_auths": [],
                       'weight_threshold': 1},
            "options": {"memo_key": memo,
                        "voting_account": voting_account["id"],
                        "num_witness": 0,
                        "num_committee": 0,
                        "votes": [],
                        "extensions": []
                        },
            "extensions": {},
            "prefix": self.prefix
        }
        op = operations.Account_create(**op)
        return self.finalizeOp(op, registrar, "active", **kwargs)

    def upgrade_account(self, account=None, **kwargs):
        """ Upgrade an account to Lifetime membership

            :param str account: (optional) the account to allow access
                to (defaults to ``default_account``)
        """
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        account = Account(account, blockchain_instance=self)
        op = operations.Account_upgrade(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "account_to_upgrade": account["id"],
            "upgrade_to_lifetime_member": True,
            "prefix": self.prefix
        })
        return self.finalizeOp(op, account["name"], "active", **kwargs)

    def _test_weights_treshold(self, authority):
        """ This method raises an error if the threshold of an authority cannot
            be reached by the weights.

            :param dict authority: An authority of an account
            :raises ValueError: if the threshold is set too high
        """
        weights = 0
        for a in authority["account_auths"]:
            weights += int(a[1])
        for a in authority["key_auths"]:
            weights += int(a[1])
        if authority["weight_threshold"] > weights:
            raise ValueError("Threshold too restrictive!")
        if authority["weight_threshold"] == 0:
            raise ValueError("Cannot have threshold of 0")

    def allow(
        self, foreign, weight=None, permission="active",
        account=None, threshold=None, **kwargs
    ):
        """ Give additional access to an account by some other public
            key or account.

            :param str foreign: The foreign account that will obtain access
            :param int weight: (optional) The weight to use. If not
                define, the threshold will be used. If the weight is
                smaller than the threshold, additional signatures will
                be required. (defaults to threshold)
            :param str permission: (optional) The actual permission to
                modify (defaults to ``active``)
            :param str account: (optional) the account to allow access
                to (defaults to ``default_account``)
            :param int threshold: The threshold that needs to be reached
                by signatures to be able to interact
        """
        from copy import deepcopy
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        if permission not in ["owner", "active"]:
            raise ValueError(
                "Permission needs to be either 'owner', or 'active"
            )
        account = Account(account, blockchain_instance=self)

        if not weight:
            weight = account[permission]["weight_threshold"]

        authority = deepcopy(account[permission])
        try:
            pubkey = PublicKey(foreign, prefix=self.prefix)
            authority["key_auths"].append([
                str(pubkey),
                weight
            ])
        except:
            try:
                foreign_account = Account(foreign, blockchain_instance=self)
                authority["account_auths"].append([
                    foreign_account["id"],
                    weight
                ])
            except:
                raise ValueError(
                    "Unknown foreign account or invalid public key"
                )
        if threshold:
            authority["weight_threshold"] = threshold
            self._test_weights_treshold(authority)

        op = operations.Account_update(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "account": account["id"],
            permission: authority,
            "extensions": {},
            "prefix": self.prefix
        })
        if permission == "owner":
            return self.finalizeOp(op, account["name"], "owner", **kwargs)
        else:
            return self.finalizeOp(op, account["name"], "active", **kwargs)

    def disallow(
        self, foreign, permission="active",
        account=None, threshold=None, **kwargs
    ):
        """ Remove additional access to an account by some other public
            key or account.

            :param str foreign: The foreign account that will obtain access
            :param str permission: (optional) The actual permission to
                modify (defaults to ``active``)
            :param str account: (optional) the account to allow access
                to (defaults to ``default_account``)
            :param int threshold: The threshold that needs to be reached
                by signatures to be able to interact
        """
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        if permission not in ["owner", "active"]:
            raise ValueError(
                "Permission needs to be either 'owner', or 'active"
            )
        account = Account(account, blockchain_instance=self)
        authority = account[permission]

        try:
            pubkey = PublicKey(foreign, prefix=self.prefix)
            affected_items = list(
                filter(lambda x: x[0] == str(pubkey),
                       authority["key_auths"]))
            authority["key_auths"] = list(filter(
                lambda x: x[0] != str(pubkey),
                authority["key_auths"]
            ))
        except:
            try:
                foreign_account = Account(foreign, blockchain_instance=self)
                affected_items = list(
                    filter(lambda x: x[0] == foreign_account["id"],
                           authority["account_auths"]))
                authority["account_auths"] = list(filter(
                    lambda x: x[0] != foreign_account["id"],
                    authority["account_auths"]
                ))
            except:
                raise ValueError(
                    "Unknown foreign account or unvalid public key"
                )

        if not affected_items:
            raise ValueError("Changes nothing!")
        removed_weight = affected_items[0][1]

        # Define threshold
        if threshold:
            authority["weight_threshold"] = threshold

        # Correct threshold (at most by the amount removed from the
        # authority)
        try:
            self._test_weights_treshold(authority)
        except:
            log.critical(
                "The account's threshold will be reduced by %d"
                % (removed_weight)
            )
            authority["weight_threshold"] -= removed_weight
            self._test_weights_treshold(authority)

        op = operations.Account_update(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "account": account["id"],
            permission: authority,
            "extensions": {}
        })
        if permission == "owner":
            return self.finalizeOp(op, account["name"], "owner", **kwargs)
        else:
            return self.finalizeOp(op, account["name"], "active", **kwargs)

    def update_memo_key(self, key, account=None, **kwargs):
        """ Update an account's memo public key

            This method does **not** add any private keys to your
            wallet but merely changes the memo public key.

            :param str key: New memo public key
            :param str account: (optional) the account to allow access
                to (defaults to ``default_account``)
        """
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        PublicKey(key, prefix=self.prefix)

        account = Account(account, blockchain_instance=self)
        account["options"]["memo_key"] = key
        op = operations.Account_update(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "account": account["id"],
            "new_options": account["options"],
            "extensions": {}
        })
        return self.finalizeOp(op, account["name"], "active", **kwargs)

    # -------------------------------------------------------------------------
    #  Approval and Disapproval of witnesses, workers, committee, and proposals
    # -------------------------------------------------------------------------
    def approvewitness(self, witnesses, account=None, **kwargs):
        """ Approve a witness

            :param list witnesses: list of Witness name or id
            :param str account: (optional) the account to allow access
                to (defaults to ``default_account``)
        """
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        account = Account(account, blockchain_instance=self)
        options = account["options"]

        if not isinstance(witnesses, (list, set, tuple)):
            witnesses = {witnesses}

        for witness in witnesses:
            witness = Witness(witness, blockchain_instance=self)
            options["votes"].append(witness["vote_id"])

        options["votes"] = list(set(options["votes"]))
        options["num_witness"] = len(list(filter(
            lambda x: float(x.split(":")[0]) == 1,
            options["votes"]
        )))

        op = operations.Account_update(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "account": account["id"],
            "new_options": options,
            "extensions": {},
            "prefix": self.prefix
        })
        return self.finalizeOp(op, account["name"], "active", **kwargs)

    def disapprovewitness(self, witnesses, account=None, **kwargs):
        """ Disapprove a witness

            :param list witnesses: list of Witness name or id
            :param str account: (optional) the account to allow access
                to (defaults to ``default_account``)
        """
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        account = Account(account, blockchain_instance=self)
        options = account["options"]

        if not isinstance(witnesses, (list, set, tuple)):
            witnesses = {witnesses}

        for witness in witnesses:
            witness = Witness(witness, blockchain_instance=self)
            if witness["vote_id"] in options["votes"]:
                options["votes"].remove(witness["vote_id"])

        options["votes"] = list(set(options["votes"]))
        options["num_witness"] = len(list(filter(
            lambda x: float(x.split(":")[0]) == 1,
            options["votes"]
        )))

        op = operations.Account_update(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "account": account["id"],
            "new_options": options,
            "extensions": {},
            "prefix": self.prefix
        })
        return self.finalizeOp(op, account["name"], "active", **kwargs)

    def approvecommittee(self, committees, account=None, **kwargs):
        """ Approve a committee

            :param list committees: list of committee member name or id
            :param str account: (optional) the account to allow access
                to (defaults to ``default_account``)
        """
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        account = Account(account, blockchain_instance=self)
        options = account["options"]

        if not isinstance(committees, (list, set, tuple)):
            committees = {committees}

        for committee in committees:
            committee = Committee(committee, blockchain_instance=self)
            options["votes"].append(committee["vote_id"])

        options["votes"] = list(set(options["votes"]))
        options["num_committee"] = len(list(filter(
            lambda x: float(x.split(":")[0]) == 0,
            options["votes"]
        )))

        op = operations.Account_update(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "account": account["id"],
            "new_options": options,
            "extensions": {},
            "prefix": self.prefix
        })
        return self.finalizeOp(op, account["name"], "active", **kwargs)

    def disapprovecommittee(self, committees, account=None, **kwargs):
        """ Disapprove a committee

            :param list committees: list of committee name or id
            :param str account: (optional) the account to allow access
                to (defaults to ``default_account``)
        """
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        account = Account(account, blockchain_instance=self)
        options = account["options"]

        if not isinstance(committees, (list, set, tuple)):
            committees = {committees}

        for committee in committees:
            committee = Committee(committee, blockchain_instance=self)
            if committee["vote_id"] in options["votes"]:
                options["votes"].remove(committee["vote_id"])

        options["votes"] = list(set(options["votes"]))
        options["num_committee"] = len(list(filter(
            lambda x: float(x.split(":")[0]) == 0,
            options["votes"]
        )))

        op = operations.Account_update(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "account": account["id"],
            "new_options": options,
            "extensions": {},
            "prefix": self.prefix
        })
        return self.finalizeOp(op, account["name"], "active", **kwargs)

    def approveproposal(
        self, proposal_ids, account=None, approver=None, **kwargs
    ):
        """ Approve Proposal

            :param list proposal_id: Ids of the proposals
            :param str account: (optional) the account to allow access
                to (defaults to ``default_account``)
        """
        from .proposal import Proposal
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        account = Account(account, blockchain_instance=self)
        is_key = approver and approver[:3] == self.prefix
        if not approver and not is_key:
            approver = account
        elif approver and not is_key:
            approver = Account(approver, blockchain_instance=self)
        else:
            approver = PublicKey(approver)

        if not isinstance(proposal_ids, (list, set, tuple)):
            proposal_ids = {proposal_ids}

        op = []
        for proposal_id in proposal_ids:
            proposal = Proposal(proposal_id, blockchain_instance=self)
            update_dict = {
                "fee": {"amount": 0, "asset_id": "1.3.0"},
                'fee_paying_account': account["id"],
                'proposal': proposal["id"],
                'active_approvals_to_add': [approver["id"]],
                "prefix": self.prefix
            }
            if is_key:
                update_dict.update({
                    'key_approvals_to_add': [str(approver)],
                })
            else:
                update_dict.update({
                    'active_approvals_to_add': [approver["id"]],
                })
            op.append(operations.Proposal_update(**update_dict))
        if is_key:
            self.txbuffer.appendSigner(account["name"], "active")
        return self.finalizeOp(op, approver["name"], "active", **kwargs)

    def disapproveproposal(
        self, proposal_ids, account=None, approver=None, **kwargs
    ):
        """ Disapprove Proposal

            :param list proposal_ids: Ids of the proposals
            :param str account: (optional) the account to allow access
                to (defaults to ``default_account``)
        """
        from .proposal import Proposal
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        account = Account(account, blockchain_instance=self)
        if not approver:
            approver = account
        else:
            approver = Account(approver, blockchain_instance=self)

        if not isinstance(proposal_ids, (list, set, tuple)):
            proposal_ids = {proposal_ids}

        op = []
        for proposal_id in proposal_ids:
            proposal = Proposal(proposal_id, blockchain_instance=self)
            op.append(operations.Proposal_update(**{
                "fee": {"amount": 0, "asset_id": "1.3.0"},
                'fee_paying_account': account["id"],
                'proposal': proposal["id"],
                'active_approvals_to_remove': [approver["id"]],
                "prefix": self.prefix
            }))
        return self.finalizeOp(op, account["name"], "active", **kwargs)

    # -------------------------------------------------------------------------
    # Bookie related calls
    # -------------------------------------------------------------------------
    def sport_create(self, names, account=None, **kwargs):
        """ Create a sport. This needs to be **proposed**.

            :param list names: Internationalized names, e.g. ``[['de', 'Foo'],
                ['en', 'bar']]``
            :param str account: (optional) the account to allow access
                to (defaults to ``default_account``)
        """
        assert isinstance(names, list)
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        account = Account(account)
        op = operations.Sport_create(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "name": names,
            "prefix": self.prefix
        })
        return self.finalizeOp(op, account["name"], "active", **kwargs)

    def sport_update(self, sport_id, names=[], account=None, **kwargs):
        """ Update a sport. This needs to be **proposed**.

            :param str sport_id: The id of the sport to update
            :param list names: Internationalized names, e.g. ``[['de', 'Foo'],
                ['en', 'bar']]``
            :param str account: (optional) the account to allow access
                to (defaults to ``default_account``)
        """
        assert isinstance(names, list)
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        account = Account(account)
        sport = Sport(sport_id)
        op = operations.Sport_update(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "sport_id": sport["id"],
            "new_name": names,
            "prefix": self.prefix
        })
        return self.finalizeOp(op, account["name"], "active", **kwargs)

    def event_group_create(
        self, names, sport_id="0.0.0", account=None, **kwargs
    ):
        """ Create an event group. This needs to be **proposed**.

            :param list names: Internationalized names, e.g. ``[['de', 'Foo'],
                ['en', 'bar']]``
            :param str sport_id: Sport ID to create the event group for
                (defaults to *relative* id ``0.0.0``)
            :param str account: (optional) the account to allow access
                to (defaults to ``default_account``)
        """
        assert isinstance(names, list)
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        if sport_id[0] == "1":
            # Test if object exists
            Sport(sport_id)
        else:
            # Test if object is proposed
            test_proposal_in_buffer(
                kwargs.get("append_to", self.propbuffer),
                "sport_create",
                sport_id)
        account = Account(account)
        op = operations.Event_group_create(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "name": names,
            "sport_id": sport_id,
            "prefix": self.prefix
        })
        return self.finalizeOp(op, account["name"], "active", **kwargs)

    def event_group_update(
        self, event_group_id, names=[],
        sport_id="0.0.0", account=None, **kwargs
    ):
        """ Update an event group. This needs to be **proposed**.

            :param str event_id: Id of the event group to update
            :param list names: Internationalized names, e.g. ``[['de', 'Foo'],
                ['en', 'bar']]``
            :param str sport_id: Sport ID to create the event group for
                (defaults to *relative* id ``0.0.0``)
            :param str account: (optional) the account to allow access
                to (defaults to ``default_account``)
        """
        assert isinstance(names, list)
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        if sport_id[0] == "1":
            # Test if object exists
            Sport(sport_id)
        else:
            # Test if object is proposed
            test_proposal_in_buffer(
                kwargs.get("append_to", self.propbuffer),
                "sport_create",
                sport_id)
        account = Account(account)
        event_group = EventGroup(event_group_id)
        op = operations.Event_group_update(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "event_group_id": event_group["id"],
            "new_name": names,
            "new_sport_id": sport_id,
            "prefix": self.prefix
        })
        return self.finalizeOp(op, account["name"], "active", **kwargs)

    def event_create(
        self,
        name,
        season,
        start_time,
        event_group_id="0.0.0",
        account=None,
        **kwargs
    ):
        """ Create an event. This needs to be **proposed**.

            :param list name: Internationalized names, e.g. ``[['de', 'Foo'],
                ['en', 'bar']]``
            :param list season: Internationalized season, e.g. ``[['de',
                'Foo'], ['en', 'bar']]``
            :param str event_group_id: Event group ID to create the event for
                (defaults to *relative* id ``0.0.0``)
            :param datetime start_time: Time of the start of the event
            :param str account: (optional) the account to allow access
                to (defaults to ``default_account``)
        """
        assert isinstance(season, list)
        assert isinstance(start_time, datetime), \
            "start_time needs to be a `datetime.datetime`"
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        account = Account(account)
        if event_group_id[0] == "1":
            # Test if object exists
            EventGroup(event_group_id)
        else:
            # Test if object is proposed
            test_proposal_in_buffer(
                kwargs.get("append_to", self.propbuffer),
                "event_group_create",
                event_group_id)
        op = operations.Event_create(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "name": name,
            "season": season,
            "start_time": formatTime(start_time),
            "event_group_id": event_group_id,
            "prefix": self.prefix
        })
        return self.finalizeOp(op, account["name"], "active", **kwargs)

    def event_update(
        self,
        event_id,
        name=None,
        season=None,
        start_time=None,
        event_group_id=None,
        status=None,
        account=None,
        **kwargs
    ):
        """ Update an event. This needs to be **proposed**.

            :param str event_id: Id of the event to update
            :param list name: Internationalized names, e.g. ``[['de', 'Foo'],
                ['en', 'bar']]``
            :param list season: Internationalized season, e.g. ``[['de',
                'Foo'], ['en', 'bar']]``
            :param str event_group_id: Event group ID to create the event for
                (defaults to *relative* id ``0.0.0``)
            :param datetime start_time: Time of the start of the event
            :param str status: Event status (:doc:`event_status`)
            :param str account: (optional) the account to allow access
                to (defaults to ``default_account``)
        """
        assert isinstance(season, list)
        assert isinstance(start_time, datetime), \
            "start_time needs to be a `datetime.datetime`"
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        account = Account(account)
        event = Event(event_id)
        op_data = {
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "event_id": event["id"],
            "prefix": self.prefix
        }

        # Do not try to update status of it doesn't change it on the chain
        if event["status"] == status:
            status = None

        if event_group_id:
            if event_group_id[0] == "1":
                # Test if object exists
                EventGroup(event_group_id)
            else:
                # Test if object is proposed
                test_proposal_in_buffer(
                    kwargs.get("append_to", self.propbuffer),
                    "event_group_create",
                    event_group_id)
            op_data.update({"new_event_group_id": event_group_id})
        if name:
            op_data.update({"new_name": name})
        if season:
            op_data.update({"new_season": season})
        if start_time:
            op_data.update({"new_start_time": formatTime(start_time)})
        if status:
            op_data.update({"new_status": status})

        op = operations.Event_update(**op_data)
        return self.finalizeOp(op, account["name"], "active", **kwargs)

    def event_update_status(
        self,
        event_id,
        status,
        scores=[],
        account=None,
        **kwargs
    ):
        """ Update the status of an event. This needs to be **proposed**.

            :param str event_id: Id of the event to update
            :param str status: Event status (:doc:`event_status`)
            :param list scores: List of strings that represent the scores of a
                match (defaults to [])
            :param str account: (optional) the account to allow access
                to (defaults to ``default_account``)
        """
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        account = Account(account)
        event = Event(event_id)

        # Do not try to update status of it doesn't change it on the chain
        if event["status"] == status:
            status = None

        op = operations.Event_update_status(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "event_id": event["id"],
            "status": status,
            "scores": scores,
            "prefix": self.prefix,
        })
        return self.finalizeOp(op, account["name"], "active", **kwargs)

    def betting_market_rules_create(
        self, names, descriptions, account=None, **kwargs
    ):
        """ Create betting market rules

            :param list names: Internationalized names, e.g. ``[['de', 'Foo'],
                ['en', 'bar']]``
            :param list descriptions: Internationalized descriptions, e.g.
                ``[['de', 'Foo'], ['en', 'bar']]``
            :param str account: (optional) the account to allow access
                to (defaults to ``default_account``)

        """
        assert isinstance(names, list)
        assert isinstance(descriptions, list)
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        account = Account(account)
        op = operations.Betting_market_rules_create(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "name": names,
            "description": descriptions,
            "prefix": self.prefix
        })
        return self.finalizeOp(op, account["name"], "active", **kwargs)

    def betting_market_rules_update(
        self, rules_id, names, descriptions, account=None, **kwargs
    ):
        """ Update betting market rules

            :param str rules_id: Id of the betting market rules to update
            :param list names: Internationalized names, e.g. ``[['de', 'Foo'],
                ['en', 'bar']]``
            :param list descriptions: Internationalized descriptions, e.g.
                ``[['de', 'Foo'], ['en', 'bar']]``
            :param str account: (optional) the account to allow access
                to (defaults to ``default_account``)

        """
        assert isinstance(names, list)
        assert isinstance(descriptions, list)
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        account = Account(account)
        rule = Rule(rules_id)
        op = operations.Betting_market_rules_update(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "betting_market_rules_id": rule["id"],
            "new_name": names,
            "new_description": descriptions,
            "prefix": self.prefix
        })
        return self.finalizeOp(op, account["name"], "active", **kwargs)

    def betting_market_group_create(
        self,
        description,
        event_id="0.0.0",
        rules_id="0.0.0",
        asset=None,
        delay_before_settling=0,
        never_in_play=False,
        account=None,
        **kwargs
    ):
        """ Create an betting market. This needs to be **proposed**.

            :param list description: Internationalized list of descriptions
            :param str event_id: Event ID to create this for (defaults to
                *relative* id ``0.0.0``)
            :param str rule_id: Rule ID to create this with (defaults to
                *relative* id ``0.0.0``)
            :param peerplays.asset.Asset asset: Asset to be used for this
                market
            :param int delay_before_settling: Delay in seconds before settling
                (defaults to 0 seconds - immediatelly)
            :param bool never_in_play: Set this market group as *never in play*
                (defaults to *False*)
            :param str account: (optional) the account to allow access
                to (defaults to ``default_account``)
        """
        if not asset:
            asset = self.rpc.chain_params["core_symbol"]
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        account = Account(account, blockchain_instance=self)
        asset = Asset(asset, blockchain_instance=self)
        if event_id[0] == "1":
            # Test if object exists
            Event(event_id)
        else:
            # Test if object is proposed
            test_proposal_in_buffer(
                kwargs.get("append_to", self.propbuffer),
                "event_create",
                event_id)
        if rules_id[0] == "1":
            # Test if object exists
            Rule(rules_id)
        else:
            # Test if object is proposed
            test_proposal_in_buffer(
                kwargs.get("append_to", self.propbuffer),
                "betting_market_rules_create",
                rules_id)
        op = operations.Betting_market_group_create(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "description": description,
            "event_id": event_id,
            "rules_id": rules_id,
            "asset_id": asset["id"],
            "never_in_play": bool(never_in_play),
            "delay_before_settling": int(delay_before_settling),
            "prefix": self.prefix
        })
        return self.finalizeOp(op, account["name"], "active", **kwargs)

    def betting_market_group_update(
        self,
        betting_market_group_id,
        description=None,
        event_id=None,
        rules_id=None,
        status=None,
        account=None,
        **kwargs
    ):
        """ Update an betting market. This needs to be **proposed**.

            :param str betting_market_group_id: Id of the betting market group
                to update
            :param list description: Internationalized list of descriptions
            :param str event_id: Event ID to create this for
            :param str rule_id: Rule ID to create this with
            :param str status: New Status
            :param str account: (optional) the account to allow access
                to (defaults to ``default_account``)
        """
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        account = Account(account, blockchain_instance=self)
        bmg = BettingMarketGroup(betting_market_group_id)

        # Do not try to update status of it doesn't change it on the chain
        if bmg["status"] == status:
            status = None

        op_data = {
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "betting_market_group_id": bmg["id"],
            "prefix": self.prefix
        }
        if event_id:
            if event_id[0] == "1":
                # Test if object exists
                Event(event_id)
            else:
                # Test if object is proposed
                test_proposal_in_buffer(
                    kwargs.get("append_to", self.propbuffer),
                    "event_create",
                    event_id)
            op_data.update({"new_event_id": event_id})

        if rules_id:
            if rules_id[0] == "1":
                # Test if object exists
                Rule(rules_id)
            else:
                # Test if object is proposed
                test_proposal_in_buffer(
                    kwargs.get("append_to", self.propbuffer),
                    "betting_market_rules_create",
                    rules_id)
            op_data.update({"new_rules_id": rules_id})

        if description:
            op_data.update({"new_description": description})

        if status:
            op_data.update({"status": status})

        op = operations.Betting_market_group_update(**op_data)
        return self.finalizeOp(op, account["name"], "active", **kwargs)

    def betting_market_create(
        self,
        payout_condition,
        description,
        group_id="0.0.0",
        account=None,
        **kwargs
    ):
        """ Create an event group. This needs to be **proposed**.

            :param list payout_condition: Internationalized names, e.g.
                ``[['de', 'Foo'], ['en', 'bar']]``
            :param list description: Internationalized descriptions, e.g.
                ``[['de', 'Foo'], ['en', 'bar']]``
            :param str group_id: Group ID to create the market for (defaults to
                *relative* id ``0.0.0``)
            :param str account: (optional) the account to allow access
                to (defaults to ``default_account``)
        """
        assert isinstance(payout_condition, list)
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        account = Account(account)
        if group_id[0] == "1":
            # Test if object exists
            BettingMarketGroup(group_id)
        else:
            # Test if object is proposed
            test_proposal_in_buffer(
                kwargs.get("append_to", self.propbuffer),
                "betting_market_group_create",
                group_id)
        op = operations.Betting_market_create(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "group_id": group_id,
            "description": description,
            "payout_condition": payout_condition,
            "prefix": self.prefix
        })
        return self.finalizeOp(op, account["name"], "active", **kwargs)

    def betting_market_update(
        self,
        betting_market_id,
        payout_condition,
        description,
        group_id="0.0.0",
        account=None,
        **kwargs
    ):
        """ Update an event group. This needs to be **proposed**.

            :param str betting_market_id: Id of the betting market to update
            :param list payout_condition: Internationalized names, e.g.
                ``[['de', 'Foo'], ['en', 'bar']]``
            :param list description: Internationalized descriptions, e.g.
                ``[['de', 'Foo'], ['en', 'bar']]``
            :param str group_id: Group ID to create the market for (defaults to
                *relative* id ``0.0.0``)
            :param str account: (optional) the account to allow access
                to (defaults to ``default_account``)
        """
        assert isinstance(payout_condition, list)
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        account = Account(account)
        market = BettingMarket(betting_market_id)
        if group_id[0] == "1":
            # Test if object exists
            BettingMarketGroup(group_id)
        else:
            # Test if object is proposed
            test_proposal_in_buffer(
                kwargs.get("append_to", self.propbuffer),
                "betting_market_group_create",
                group_id)
        op = operations.Betting_market_update(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "betting_market_id": market["id"],
            "new_group_id": group_id,
            "new_description": description,
            "new_payout_condition": payout_condition,
            "prefix": self.prefix
        })
        return self.finalizeOp(op, account["name"], "active", **kwargs)

    def betting_market_resolve(
        self, betting_market_group_id, results, account=None, **kwargs
    ):
        """ Create an betting market. This needs to be **proposed**.

            :param str betting_market_group_id: Market Group ID to resolve
            :param list results: Array of Result of the market (``win``,
                ``not_win``, or ``cancel``)
            :param str account: (optional) the account to allow access
                to (defaults to ``default_account``)

            Results take the form:::

                [
                   ["1.21.257", "win"],
                   ["1.21.258", "not_win"],
                   ["1.21.259", "cancel"],
               ]

        """
        assert isinstance(results, (list, set, tuple))
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        account = Account(account)
        # Test if object exists
        BettingMarketGroup(betting_market_group_id)
        op = operations.Betting_market_group_resolve(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "betting_market_group_id": betting_market_group_id,
            "resolutions": results,
            "prefix": self.prefix
        })
        return self.finalizeOp(op, account["name"], "active", **kwargs)

    # -------------------------------------------------------------------------
    # The betting in bookie
    # -------------------------------------------------------------------------
    def bet_place(
        self,
        betting_market_id,
        amount_to_bet,
        backer_multiplier,
        back_or_lay,
        account=None,
        **kwargs
    ):
        """ Place a bet

            :param str betting_market_id: The identifier for the market to bet
                in
            :param peerplays.amount.Amount amount_to_bet: Amount to bet with
            :param int backer_multiplier: Multipler for backer
            :param str back_or_lay: "back" or "lay" the bet
            :param str account: (optional) the account to bet (defaults
                        to ``default_account``)
        """
        from . import GRAPHENE_BETTING_ODDS_PRECISION
        assert isinstance(amount_to_bet, Amount)
        assert back_or_lay in ["back", "lay"]
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        account = Account(account)
        bm = BettingMarket(betting_market_id)
        op = operations.Bet_place(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "bettor_id": account["id"],
            "betting_market_id": bm["id"],
            "amount_to_bet": amount_to_bet.json(),
            "backer_multiplier": (
                int(backer_multiplier * GRAPHENE_BETTING_ODDS_PRECISION)
            ),
            "back_or_lay": back_or_lay,
            "prefix": self.prefix
        })
        return self.finalizeOp(op, account["name"], "active", **kwargs)

    def bet_cancel(self, bet_to_cancel, account=None, **kwargs):
        """ Cancel a bet

            :param str bet_to_cancel: The identifier that identifies the bet to
                cancel
            :param str account: (optional) the account that owns the bet
                (defaults to ``default_account``)
        """
        if not account:
            if "default_account" in config:
                account = config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        account = Account(account)
        bet = Bet(bet_to_cancel)
        op = operations.Bet_cancel(**{
            "fee": {"amount": 0, "asset_id": "1.3.0"},
            "bettor_id": account["id"],
            "bet_to_cancel": bet["id"],
            "prefix": self.prefix
        })
        return self.finalizeOp(op, account["name"], "active", **kwargs)
