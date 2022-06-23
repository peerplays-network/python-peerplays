#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from peerplaysbase import operations

from .account import Account
from .amount import Amount
from .asset import Asset
from .instance import BlockchainInstance
from .price import FilledOrder, Order, Price
from .utils import assets_from_string, formatTime, formatTimeFromNow


@BlockchainInstance.inject
class Market(dict):
    """
    This class allows to easily access Markets on the blockchain for trading, etc.

    :param peerplays.peerplays.PeerPlays blockchain_instance: Peerplays instance
    :param peerplays.asset.Asset base: Base asset
    :param peerplays.asset.Asset quote: Quote asset
    :returns: Blockchain Market
    :rtype: dictionary with overloaded methods

    Instances of this class are dictionaries that come with additional
    methods (see below) that allow dealing with a market and it's
    corresponding functions.

    This class tries to identify **two** assets as provided in the
    parameters in one of the following forms:

    * ``base`` and ``quote`` are valid assets (according to :class:`peerplays.asset.Asset`)
    * ``base:quote`` separated with ``:``
    * ``base/quote`` separated with ``/``
    * ``base-quote`` separated with ``-``

    .. note:: Throughout this library, the ``quote`` symbol will be
              presented first (e.g. ``BTC:PPY`` with ``BTC`` being the
              quote), while the ``base`` only refers to a secondary asset
              for a trade. This means, if you call
              :func:`peerplays.market.Market.sell` or
              :func:`peerplays.market.Market.buy`, you will sell/buy **only
              quote** and obtain/pay **only base**.
    """

