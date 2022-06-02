#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from xmlrpc.client import ServerProxy, Fault

from locust import User, task, HttpUser
# from fixtures import fixture_data, peerplays

# from locust import HttpUser, task, between
from peerplays import PeerPlays

p = PeerPlays()
print("p.info:", p.info())

class XmlRpcClient(ServerProxy):
# class XmlRpcClient(PeerPlays):
# class XmlRpcClient(HttpUser):
    # from fixtures import peerplays
    """
    XmlRpcClient is a wrapper around the standard library's ServerProxy.
    It proxies any function calls and fires the *request* event when they finish,
    so that the calls get recorded in Locust.
    """

    def __init__(self, host, request_event):
    # def __init__(self):
        super().__init__(host)
        self._request_event = request_event
        self.peerplays = PeerPlays()
        self.peerplays.unlock("gnulinux")

    def __getattr__(self, name):
        # func = peerplays.__getattr__(self, name)
        # func = peerplays.info()
        func = time.asctime()
        def wrapper(*args, **kwargs):
            start_perf_counter = time.perf_counter()
            # from tests.fixtures import fixture_data, peerplays
            request_meta = {
                "request_type": "ws",
                "name": name,
                "start_time": time.time(),
                "response_length": 0,  # calculating this for an xmlrpc.client response would be too hard
                "response": None,
                "context": {},  # see HttpUser if you actually want to implement contexts
                "exception": None,
            }
            try:
                # request_meta["response"] = func(*args, **kwargs)
                # request_meta["response"] = peerplays.info()
                # trash_resp_direct = self.peerplays.info()
                print("try begin ===============")
                to = "1.2.8"
                amount = 0.1
                asset = "TEST"
                account = "1.2.9"
                trash_resp_direct = self.peerplays.transfer(to, amount, asset, memo="", account=account)
                print("direct:", trash_resp_direct)
                # trash_resp_direct = time.asctime()
                request_meta["response"] = trash_resp_direct
                # request_meta["exception"] = trash_resp_direct
                # request_meta["exception"] = None
                # trash_resp_func = func()
                # print("func:", trash_resp_func)
                # request_meta["response"] = func()
                # print(a)
            # except Fault as e:
            except Exception as e:
                request_meta["exception"] = e
            request_meta["response_time"] = (time.perf_counter() - start_perf_counter) * 1000
            self._request_event.fire(**request_meta)  # This is what makes the request actually get logged in Locust
            return request_meta["response"]

        return wrapper


class XmlRpcUser(User):
    """
    A minimal Locust user class that provides an XmlRpcClient to its subclasses
    """

    abstract = True  # dont instantiate this as an actual user when running Locust

    def __init__(self, environment):
        super().__init__(environment)
        self.client = XmlRpcClient(self.host, request_event=environment.events.request)
        # self.client = XmlRpcClient()


# The real user class that will be instantiated and run by Locust
# This is the only thing that is actually specific to the service that we are testing.
class MyUser(XmlRpcUser):
    host = "http://127.0.0.1:8877/"
    # host = "wss://irona.peerplays.download/api"

    @task
    def get_time(self):
        result = self.client.info()
        time.sleep(0.1)
        # self.client.get_time()
        print("time:", time.asctime(), result)

#    @task
#    def get_random_number(self):
#        self.client.get_random_number(0, 100)
#        print("random:", time.asctime())
