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

    def __init__(self, *args, **kwargs):
        base = kwargs.get("base", None)
        quote = kwargs.get("quote", None)

        if len(args) == 1 and isinstance(args[0], str):
            quote_symbol, base_symbol = assets_from_string(args[0])
            quote = Asset(quote_symbol, blockchain_instance=self.blockchain)
            base = Asset(base_symbol, blockchain_instance=self.blockchain)
            dict.__init__(self, {"base": base, "quote": quote})
        elif len(args) == 0 and base and quote:
            dict.__init__(self, {"base": base, "quote": quote})
        elif len(args) == 2 and not base and not quote:
            dict.__init__(self, {"base": args[1], "quote": args[0]})
        else:
            raise ValueError("Unknown Market Format: %s" % str(args))

    def get_string(self, separator=":"):
        """
        Return a formated string that identifies the market, e.g. ``BTC:PPY``

        :param str separator: The separator of the assets (defaults to ``:``)
        """
        return "%s%s%s" % (self["quote"]["symbol"], separator, self["base"]["symbol"])

    def __eq__(self, other):
        if isinstance(other, str):
            quote_symbol, base_symbol = assets_from_string(other)
            return (
                self["quote"]["symbol"] == quote_symbol
                and self["base"]["symbol"] == base_symbol
            ) or (
                self["quote"]["symbol"] == base_symbol
                and self["base"]["symbol"] == quote_symbol
            )
        elif isinstance(other, Market):
            return (
                self["quote"]["symbol"] == other["quote"]["symbol"]
                and self["base"]["symbol"] == other["base"]["symbol"]
            )


    def orderbook(self, limit=25):
        """
        Returns the order book for a given market. You may also specify "all" to get the
        orderbooks of all markets.

        :param int limit: Limit the amount of orders (default: 25)

        Sample output:

        .. code-block:: js

            {'bids': [0.003679 USD/BTS (1.9103 USD|519.29602 BTS),
            0.003676 USD/BTS (299.9997 USD|81606.16394 BTS),
            0.003665 USD/BTS (288.4618 USD|78706.21881 BTS),
            0.003665 USD/BTS (3.5285 USD|962.74409 BTS),
            0.003665 USD/BTS (72.5474 USD|19794.41299 BTS)],
            'asks': [0.003738 USD/BTS (36.4715 USD|9756.17339 BTS),
            0.003738 USD/BTS (18.6915 USD|5000.00000 BTS),
            0.003742 USD/BTS (182.6881 USD|48820.22081 BTS),
            0.003772 USD/BTS (4.5200 USD|1198.14798 BTS),
            0.003799 USD/BTS (148.4975 USD|39086.59741 BTS)]}


        .. note:: Each bid is an instance of
            class:`bitshares.price.Order` and thus carries the keys
            ``base``, ``quote`` and ``price``. From those you can
            obtain the actual amounts for sale

        .. note:: This method does order consolidation and hides some
            details of individual orders!
        """
        orders = self.blockchain.rpc.get_order_book(
            self["base"]["id"], self["quote"]["id"], limit
        )
        asks = list(
            map(
                lambda x: Order(
                    float(x["price"]),
                    quote=Amount(
                        x["quote"], self["quote"], blockchain_instance=self.blockchain
                    ),
                    base=Amount(
                        x["base"], self["base"], blockchain_instance=self.blockchain
                    ),
                    blockchain_instance=self.blockchain,
                ),
                orders["asks"],
            )
        )
        bids = list(
            map(
                lambda x: Order(
                    float(x["price"]),
                    quote=Amount(
                        x["quote"], self["quote"], blockchain_instance=self.blockchain
                    ),
                    base=Amount(
                        x["base"], self["base"], blockchain_instance=self.blockchain
                    ),
                    blockchain_instance=self.blockchain,
                ),
                orders["bids"],
            )
        )
        data = {"asks": asks, "bids": bids}
        return data


