#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import random
import os
# import multiprocessing
import time
# import subprocess

# urlWitness = "http://0.0.0.0:8091"
# urlWitness = "http://10.11.12.101:8091"
# witnessNode = "ws://10.11.12.101:8090"
# chainId = "7c1c72eb738b3ff1870350f85daca27e2d0f5dd25af27df7475fbd92815e421e"

class PeerPlays():
    """ 
    This class is http endpoint based implementation of peerplays operations

    """

    def __init__(self, urlWalletServer):
        # self.witnessNode = witnessNode
        self.urlWitness = urlWalletServer
        # self.chainId = chainId
        # self.wallet_server_start()
        # time.sleep(5)
        # self.set_password("password")
        # self.unlock("password)")
        pass

    def wallet_server(self):
        self.urlWitnessR = urlWitness.split("://")[1]
        commandServer = ""
        commandServer = commandServer + './cli_wallet '
        # commandServer = commandServer + '-s "' + self.witnessNode + '" '
        # commandServer = commandServer + "--chain-id " +  chainId + " "
        commandServer = commandServer + '-r "' +  self.urlWitnessR + '" '
        commandString = './cli_wallet -s "ws://10.11.12.101:8090" --chain-id "7c1c72eb738b3ff1870350f85daca27e2d0f5dd25af27df7475fbd92815e421e" -r "0.0.0.0:8091" -d'
        # os.system(commandServer)
        os.system(commandString)
        # subprocess.run(commandString)

    def wallet_server_start(self):
        # print("process to begin")
        process = multiprocessing.Process(target=self.wallet_server)
        # process = subprocess.call(self.wallet_server)
        process.start()
        # process.join()
        # print("process started:" , process)


    def WalletCall(self, method, params=[]):
        data = dict()
        data["jsonrpc"] = "2.0"
        data["id"] = 1

        # data["method"] = "info"
        data["method"] = method
        # data["params"] = []
        data["params"] = params
        dataJson = json.dumps(data)
        r = requests.get(self.urlWitness, data = dataJson)
        # return r

        resultJson = r.text
        result = json.loads(resultJson)
        return result
        # result = result["result"]
        # return result

    def info(self):
        method = "info"
        params = []
        r = self.WalletCall(method, params)
        return r
        # pass

    def unlock(self, password):
        method = "unlock"
        params = [password]
        r = self.WalletCall(method, params)
        return r
        pass

    def set_password(self, password):
        method = "set_password"
        params = [password]
        r = self.WalletCall(method, params)
        return r

    def is_locked(self):
        method = "is_locked"
        r = self.WalletCall(method)
        return r

    def import_key(self, accountName, wif):
        method = "import_key"
        params = [accountName, wif]
        r = self.WalletCall(method)

    def register_account (self, accountName, ownerKey, activeKey, registrarAccount, referrerAccount, referrerPercent):
        method = "register_account"
        params = [accountName, ownerKey, activeKey, registrarAccount, referrerAccount, referrerPercent, "true"]
        r = self.WalletCall(method, params)
        return r

    def create_account( 
                        self,
                        account_name,
                        registrar="None",
                        referrer="1.2.0",
                        referrer_percent=50,
                        owner_key=None,
                        active_key=None,
                        memo_key=None,
                        ):
        r = self.register_account (account_name, owner_key, active_key, registrar, referrer, referrer_percent)
        return r

    def suggest_brain_key(self):
        method = "suggest_brain_key"
        params = []
        r = self.WalletCall(method, params)
        return r

if __name__ == "__main__":
    p2 = PeerPlays(urlWalletServer=urlWitness)
    # p2.wallet_server_start()
    # print("----server --- started ----")

    # name = "trash" + str(random.randint(1,10000))
    # publicKey = "TEST6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV"
    # r = peerplays.register_account(name, publicKey, publicKey, "nathan", "nathan", 10)
    # print(r)
