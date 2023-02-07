#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import random
import os
import time

class PeerPlays():
    """ 
    This class is http endpoint based implementation of peerplays operations
        : param str urlWalletServer: Remote wallet server

        .. code-block:: python

            from peerplays.peerplays2 import PeerPlays as PeerPlays2
            peerplays2 = PeerPlays2(urlWalletServer=urlWalletServer)


        where ``<urlWalletServer>`` starts with ``http://`` or ``https://``.

        The purpose of this class it to simplify interaction with
        a few of the new PeerPlays features and changes.
        
        The idea is to have a class that allows to do this


    """

    def __init__(self, urlWalletServer):
        """ Transfer an asset to another account.

            :param str urlWalletServer: Remote wallet server
            :param float amount: Amount to transfer
            :param str asset: Asset to transfer
            :param str memo: (optional) Memo, may begin with `#` for encrypted
                messaging
            :param str account: (optional) the source account for the transfer
                if not ``default_account``
        """
        self.urlWitness = urlWalletServer
        pass

    def wallet_server(self):
        self.urlWitnessR = urlWitness.split("://")[1]
        commandServer = ""
        commandServer = commandServer + './cli_wallet '
        commandServer = commandServer + '-r "' +  self.urlWitnessR + '" '
        commandString = './cli_wallet -s "ws://10.11.12.101:8090" --chain-id "7c1c72eb738b3ff1870350f85daca27e2d0f5dd25af27df7475fbd92815e421e" -r "0.0.0.0:8091" -d'
        os.system(commandString)

    def wallet_server_start(self):
        process = multiprocessing.Process(target=self.wallet_server)
        process.start()

    def WalletCall(self, method, params=[]):
        """ Genric method for making calls to peerplays node through remote wallet.
            :param str method: Name of the cli_wallet command to call
            :param str params: Parameters to the command
        """
        data = dict()
        data["jsonrpc"] = "2.0"
        data["id"] = 1

        data["method"] = method
        data["params"] = params
        dataJson = json.dumps(data)
        r = requests.get(self.urlWitness, data = dataJson)

        resultJson = r.text
        result = json.loads(resultJson)
        return result

    def info(self):
        """ Info command
        """
        method = "info"
        params = []
        r = self.WalletCall(method, params)
        return r

    def unlock(self, password):
        """ Method to unlock wallet
            :param str password: Remote wallet password
        """
        method = "unlock"
        params = [password]
        r = self.WalletCall(method, params)
        return r

    def set_password(self, password):
        """ Set remote wallet password
            param str password: New wallet password
        """
        method = "set_password"
        params = [password]
        r = self.WalletCall(method, params)
        return r

    def is_locked(self):
        """ Check if wallet is locked
        """
        method = "is_locked"
        r = self.WalletCall(method)
        return r

    def import_key(self, accountName, wif):
        """ Import keys to the wallet
        :param str accountName: AccoutName
        :param strr wif: WIF of the account
        """
        method = "import_key"
        params = [accountName, wif]
        r = self.WalletCall(method)

    def register_account (self, accountName, ownerKey, activeKey, registrarAccount, referrerAccount, referrerPercent):
        """ Create new account
            :param str accountName: New account name
            :param str ownerKey: Owner key
            :param str activeKey: Active key
            :param str registrAccount: Registrar
            :param str referreAccount: Referrer
            :param str referrerPercent: Referrer percent
        """
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
        """ Create new account. This method is more for back compatibility
            :param str accountName: New account name
            :param str ownerKey: Owner key
            :param str activeKey: Active key
            :param str registrAccount: Registrar
            :param str referreAccount: Referrer
            :param str referrerPercent: Referrer percent
        """
        r = self.register_account (account_name, owner_key, active_key, registrar, referrer, referrer_percent)
        return r

    def suggest_brain_key(self):
        method = "suggest_brain_key"
        params = []
        r = self.WalletCall(method, params)
        return r

if __name__ == "__main__":
    p2 = PeerPlays(urlWalletServer=urlWitness)
