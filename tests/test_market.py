# -*- coding: utf-8 -*-
import pytest
import logging
import asyncio
import unittest

import time

from peerplays.asset import Asset
from peerplays.amount import Amount
from peerplays.account import Account
from peerplays.price import Price, Order
from peerplays.market import Market
from .fixtures import fixture_data, peerplays, core_unit

log = logging.getLogger("grapheneapi")
log.setLevel(logging.DEBUG)

def do_trade(market, default_account):
    # Small sleep is needed to prevent trx dups when running multiple tests
    # await asyncio.sleep(1.1)
    # market = self.market
    res = market.buy(100, 100, account=default_account)
    print("Result Buy:", res)
    time.sleep(0.1)
    # res = market.sell(0.99, 1, account=default_account)
    # print("Result Sell:", res)

def cancel_all_orders(market, account_id):
    account = Account(account_id)
    orders = [order["id"] for order in market.accountopenorders(account_id) if "id" in order]
    print("Length Orders Before Cancel:", len(orders))
    market.cancel(orders, account=account)
    time.sleep(3.1)
    orders = [order["id"] for order in market.accountopenorders(account_id) if "id" in order]
    print("Length Orders After Cancel:", len(orders))

def place_order(market, default_account):
    # time.sleep(0.1)
    market.buy(1, 1, account=default_account)
    # market.sell(10, 1, account=default_account)
#    yield
#    await cancel_all_orders(default_account)

class Testcases(unittest.TestCase):

    def setUp(self):
        # fixture_data()
        peerplays.nobroadcast = False
        peerplays.blocking = True
        pass

    def a_test_market(self):
        market = Market("BTC:TEST", blockchain_instance=peerplays)
        print("market:", market)
        self.market = market

    def a_test_do_trade(self):
        market = Market("HIVE:TEST", blockchain_instance=peerplays)
        default_account = "1.2.7"
        do_trade(market, default_account)

    def a_test_cancel_all_orders(self):
        market = Market("HIVE:TEST", blockchain_instance=peerplays)
        default_account = "1.2.7"
        cancel_all_orders(market, default_account)

    def a_test_palce_order(self):
        market = Market("HIVE:TEST", blockchain_instance=peerplays)
        default_account = "1.2.7"
        place_order(market, default_account)

    def a_test_market_init(self):
        market = Market("HIVE:TEST", blockchain_instance=peerplays)
        assert market.get("base")
        assert market.get("quote")

    def a_test_market_ticker(self):
        market = Market("HIVE:TEST", blockchain_instance=peerplays)
        t = market.ticker()
        assert "lowestAsk" in t
        assert "highestBid" in t

    def a_test_volume24h(self):
        market = Market("HIVE:TEST", blockchain_instance=peerplays)
        #await asyncio.sleep(5)
        volume = market.volume24h()
        market["base"]["symbol"] in volume
        assert market["quote"]["symbol"] in volume
        assert volume[market["base"]["symbol"]] >= 0
        assert volume[market["quote"]["symbol"]] >= 0

    def a_test_orderbook(self):
        market = Market("HIVE:TEST", blockchain_instance=peerplays)
        orderbook = market.orderbook()
        assert "bids" in orderbook
        assert "asks" in orderbook
        assert len(orderbook["bids"]) >= 0

    def a_test_get_limit_orders(self):
        market = Market("HIVE:TEST", blockchain_instance=peerplays)
        orderbook = market.get_limit_orders()
        assert len(orderbook) >= 0
        assert isinstance(orderbook[0], Order)

    def test_trades(self):
        market = Market("HIVE:TEST", blockchain_instance=peerplays)
        trades = [trade for trade in market.trades()]
        assert len(trades) >= 0

    def test_accounttrades(self):
        market = Market("HIVE:TEST", blockchain_instance=peerplays)
        default_account = "1.2.7"
        trades = market.accounttrades(account=default_account)
        # print("trades:", trades)
        assert len(trades) >= 0

    def test_accountopenorders(self):
        market = Market("HIVE:TEST", blockchain_instance=peerplays)
        default_account = "1.2.7"
        orders = market.accountopenorders(account=default_account)
        # print("orders:", orders)
        assert type(orders) == list

    def test_buy(self):
        market = Market("HIVE:TEST", blockchain_instance=peerplays)
        default_account = "1.2.7"
        time.sleep(1.1)
        market.buy(1, 1, account=default_account)
        cancel_all_orders(market, default_account)

    def test_sell(self):
        market = Market("HIVE:TEST", blockchain_instance=peerplays)
        default_account = "1.2.7"
        # asyncio.sleep(1.1)
        # market.sell(1, 1, account=default_account)
        cancel_all_orders(market, default_account)

    def test_cancel(self):
        market = Market("HIVE:TEST", blockchain_instance=peerplays)
        default_account = "1.2.7"
        orders = market.accountopenorders(account=default_account)
        num_orders_before = len(orders)
        time.sleep(1.1)
        tx = market.buy(1, 1, account=default_account, returnOrderId="head")
        market.cancel(tx["orderid"], account=default_account)
        orders = market.accountopenorders(account=default_account)
        num_orders_after = len(orders)
        assert num_orders_before == num_orders_after
