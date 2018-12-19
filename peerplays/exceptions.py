# -*- coding: utf-8 -*-
from graphenestorage.exceptions import WrongMasterPasswordException
from graphenecommon.exceptions import (
    AccountDoesNotExistsException,
    AssetDoesNotExistsException,
    BlockDoesNotExistsException,
    CommitteeMemberDoesNotExistsException,
    InvalidAssetException,
    InvalidMemoKeyException,
    InvalidMessageSignature,
    InvalidWifError,
    KeyAlreadyInStoreException,
    KeyNotFound,
    MissingKeyError,
    NoWalletException,
    OfflineHasNoRPCException,
    ProposalDoesNotExistException,
    VestingBalanceDoesNotExistsException,
    WalletExists,
    WalletLocked,
    WitnessDoesNotExistsException,
    WorkerDoesNotExistsException,
    WrongMemoKey,
    GenesisBalanceDoesNotExistsException,
)


class RPCConnectionRequired(Exception):
    """ An RPC connection is required
    """

    pass


class AccountExistsException(Exception):
    """ The requested account already exists
    """

    pass


class ObjectNotInProposalBuffer(Exception):
    """ Object was not found in proposal
    """

    pass


class RPCConnectionRequired(Exception):
    """ An RPC connection is required
    """

    pass


class AccountExistsException(Exception):
    """ The requested account already exists
    """

    pass


class InsufficientAuthorityError(Exception):
    """ The transaction requires signature of a higher authority
    """

    pass


class WrongMasterPasswordException(Exception):
    """ The password provided could not properly unlock the wallet
    """

    pass


class BetDoesNotExistException(Exception):
    """ This bet does not exist
    """

    pass


class BettingMarketDoesNotExistException(Exception):
    """ Betting market does not exist
    """

    pass


class BettingMarketGroupDoesNotExistException(Exception):
    """ Betting Market Group does not exist
    """

    pass


class EventDoesNotExistException(Exception):
    """ This event does not exist
    """

    pass


class EventGroupDoesNotExistException(Exception):
    """ This event group does not exist
    """

    pass


class SportDoesNotExistException(Exception):
    """ Sport does not exist
    """

    pass


class RuleDoesNotExistException(Exception):
    """ Rule does not exist
    """

    pass


class ObjectNotInProposalBuffer(Exception):
    """ Object was not found in proposal
    """

    pass


class GenesisBalanceDoesNotExistsException(Exception):
    """ The provided genesis balance id does not exist
    """

    pass
