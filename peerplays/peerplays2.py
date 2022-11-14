#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import random

# urlWitness = "http://0.0.0.0:8092"
urlWitness = "http://10.11.12.101:8092"

def WalletCall(method, params=[]):
    data = dict()
    data["jsonrpc"] = "2.0"
    data["id"] = 1

    # data["method"] = "info"
    data["method"] = method
    # data["params"] = []
    data["params"] = params
    dataJson = json.dumps(data)
    r = requests.get(urlWitness, data = dataJson)
    # return r

    resultJson = r.text
    result = json.loads(resultJson)
    return result
    result = result["result"]
    return result


class PeerPlays():
    """ 
    This class is http endpoint based implementation of peerplays operations

    """

    def __init__(self, urlWitness):
        self.urlwitness = urlWitness
        pass

    def unlock(self, password):
        method = "unlock"
        params = [password]
        WalletCall(method, params)
        pass

    def set_password(self, password):
        method = "set_password"
        params = [password]
        r = WalletCall(method, params)
        return r

    def is_locked(self):
        method = "is_locked"
        r = WalletCall(method)
        return r

    def register_account (self, accountName, ownerKey, activeKey, registrarAccount, referrerAccount, referrerPercent):
        method = "register_account"
        params = [accountName, ownerKey, activeKey, registrarAccount, referrerAccount, referrerPercent, "true"]
        r = WalletCall(method, params)
        return r

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
                        ):
        r = self.register_account (account_name, owner_key, active_key, registrar, referrer, referrer_percent)
        return r

if __name__ == "__main__":
    peerplays = PeerPlays(urlWitness = urlWitness)

    name = "trash" + str(random.randint(1,10000))
    publicKey = "TEST6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV"
    r = peerplays.register_account(name, publicKey, publicKey, "nathan", "nathan", 10)
    print(r)
