# -*- coding: utf-8 -*-
from .amount import Amount
from .instance import BlockchainInstance
from graphenecommon.account import (
    Account as GrapheneAccount,
    AccountUpdate as GrapheneAccountUpdate,
)
from peerplaysbase import operations


@BlockchainInstance.inject
class Account(GrapheneAccount):
    """ This class allows to easily access Account data

        :param str account_name: Name of the account
        :param peerplays.peerplays.peerplays blockchain_instance: peerplays
               instance
        :param bool full: Obtain all account data including orders, positions, etc.
        :param bool lazy: Use lazy loading
        :param bool full: Obtain all account data including orders, positions,
               etc.
        :returns: Account data
        :rtype: dictionary
        :raises peerplays.exceptions.AccountDoesNotExistsException: if account
                does not exist

        Instances of this class are dictionaries that come with additional
        methods (see below) that allow dealing with an account and it's
        corresponding functions.

        .. code-block:: python

            from peerplays.account import Account
            account = Account("init0")
            print(account)

        .. note:: This class comes with its own caching function to reduce the
                  load on the API server. Instances of this class can be
                  refreshed with ``Account.refresh()``.

    """

    def define_classes(self):
        self.type_id = 2
        self.amount_class = Amount
        self.operations = operations


@BlockchainInstance.inject
class AccountUpdate(GrapheneAccountUpdate):
    """ This purpose of this class is to keep track of account updates
        as they are pushed through by :class:`peerplays.notify.Notify`.

        Instances of this class are dictionaries and take the following
        form:

        ... code-block: js

            {'id': '2.6.29',
             'lifetime_fees_paid': '44261516129',
             'most_recent_op': '2.9.0',
             'owner': '1.2.29',
             'pending_fees': 0,
             'pending_vested_fees': 16310,
             'total_core_in_orders': '6788845277634',
             'total_ops': 0}

    """

    account_class = Account
