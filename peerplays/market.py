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

            {'bids': [0.003679 BTC/PPY (1.9103 BTC|519.29602 PPY),
            0.003676 BTC/PPY (299.9997 BTC|81606.16394 PPY),
            0.003665 BTC/PPY (288.4618 BTC|78706.21881 PPY),
            0.003665 BTC/PPY (3.5285 BTC|962.74409 PPY),
            0.003665 BTC/PPY (72.5474 BTC|19794.41299 PPY)],
            'asks': [0.003738 BTC/PPY (36.4715 BTC|9756.17339 PPY),
            0.003738 BTC/PPY (18.6915 BTC|5000.00000 PPY),
            0.003742 BTC/PPY (182.6881 BTC|48820.22081 PPY),
            0.003772 BTC/PPY (4.5200 BTC|1198.14798 PPY),
            0.003799 BTC/PPY (148.4975 BTC|39086.59741 PPY)]}


        .. note:: Each bid is an instance of
            class:`peerplays.price.Order` and thus carries the keys
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

    def buy(
        self,
        price,
        amount,
        expiration=None,
        killfill=False,
        account=None,
        returnOrderId=False,
        **kwargs
    ):
        """
        Places a buy order in a given market.

        :param float price: price denoted in ``base``/``quote``
        :param number amount: Amount of ``quote`` to buy
        :param number expiration: (optional) expiration time of the order in seconds (defaults to 7 days)
        :param bool killfill: flag that indicates if the order shall be killed if it is not filled (defaults to False)
        :param string account: Account name that executes that order
        :param string returnOrderId: If set to "head" or "irreversible" the call will wait for the tx to appear in
                                    the head/irreversible block and add the key "orderid" to the tx output

        Prices/Rates are denoted in 'base', i.e. the BTC_PPY market
        is priced in PPY per BTC.

        **Example:** in the BTC_PPY market, a price of 400 means
        a BTC is worth 400 PPY 

        .. note::

            All prices returned are in the **reversed** orientation as the
            market. I.e. in the BTC/PPY market, prices are PPY per BTC.
            That way you can multiply prices with `1.05` to get a +5%.

        .. warning::

            Since buy orders are placed as
            limit-sell orders for the base asset,
            you may end up obtaining more of the
            buy asset than you placed the order
            for. Example:

                * You place and order to buy 10 BTC for 100 PPY/BTC
                * This means that you actually place a sell order for 1000 PPY in order to obtain **at least** 10 PPY
                * If an order on the market exists that sells BTC for cheaper, you will end up with more than 10 BTC
        """
        if not expiration:
            expiration = (
                self.blockchain.config["order-expiration"] or 60 * 60 * 24 * 365
            )
        if not account:
            if "default_account" in self.blockchain.config:
                account = self.blockchain.config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")
        account = Account(account, blockchain_instance=self.blockchain)

        if isinstance(price, Price):
            price = price.as_base(self["base"]["symbol"])

        if isinstance(amount, Amount):
            amount = Amount(amount, blockchain_instance=self.blockchain)
            assert (
                amount["asset"]["symbol"] == self["quote"]["symbol"]
            ), "Price: {} does not match amount: {}".format(str(price), str(amount))
        else:
            amount = Amount(
                amount, self["quote"]["symbol"], blockchain_instance=self.blockchain
            )

        order = operations.Limit_order_create(
            **{
                "fee": {"amount": 0, "asset_id": "1.3.0"},
                "seller": account["id"],
                "amount_to_sell": {
                    "amount": int(
                        round(
                            float(amount)
                            * float(price)
                            * 10 ** self["base"]["precision"]
                        )
                    ),
                    "asset_id": self["base"]["id"],
                },
                "min_to_receive": {
                    "amount": int(
                        round(float(amount) * 10 ** self["quote"]["precision"])
                    ),
                    "asset_id": self["quote"]["id"],
                },
                "expiration": formatTimeFromNow(expiration),
                "fill_or_kill": killfill,
            }
        )

        if returnOrderId:
            # Make blocking broadcasts
            prevblocking = self.blockchain.blocking
            self.blockchain.blocking = returnOrderId

        tx = self.blockchain.finalizeOp(order, account["name"], "active", **kwargs)

        if returnOrderId and tx.get("operation_results"):
            tx["orderid"] = tx["operation_results"][0][1]
            self.blockchain.blocking = prevblocking

        return tx
