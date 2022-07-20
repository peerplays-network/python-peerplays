#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from peerplaysbase import operations
from peerplays import PeerPlays

from .account import Account
from .amount import Amount
from .asset import Asset
from .instance import BlockchainInstance
from .price import FilledOrder, Order, Price
from .utils import assets_from_string, formatTime, formatTimeFromNow


@BlockchainInstance.inject
class Son():
    """
    This class allows to easily access SON on the blockchain.

    :param peerplays.peerplays.PeerPlays blockchain_instance: Peerplays instance
    :returns: Blockchain SON
    :rtype: dictionary with overloaded methods

    Instances of this class are dictionaries that come with additional
    methods (see below) that allow dealing with a SONs and it's
    corresponding functions.

    """

    def __init__(self, *args, **kwargs):

        dict.__init__(self)


    def get_son_network(self):
        network = self.blockchain.rpc.get_son_network() 
        return get_son_network

