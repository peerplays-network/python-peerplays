#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

# urlWitness = "http://0.0.0.0:8092"
urlWitness = "http://10.11.12.101:8092"
brainKey = "CHOROGI EERIE RETUCK PRAECOX MUDDLER LITERAL ACRON CARBRO BABBY AGAZED UNBOLT ABASED HALA TEMBLOR EMANATE HEMIPIC"

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


class Son():
    """ 
    This class is http endpoint based implementation of Son operations

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

    def create_son(self, account_name, url, sidechainPublicKeyListOfList):
        method = "try_create_son"
        params = [account_name, url, sidechainPublicKeyListOfList, "true"]
        r = WalletCall(method, params)
        return r

    def update_son(self, account_name, url, sidechainPublicKeyListOfList):
        method = "try_create_son"
        params = [account_name, url, sidechainPublicKeyListOfList, "true"]
        r = WalletCall(method, params)
        return r

    def delete_sidechain_address(self, account_name, sidechain):
        method = "delete_sidechain_address"
        params = [account_name, sidechain, "true"]
        r = WalletCall(method, params)
        return r


    def request_son_maintenance(self, account_name):
        method = "request_son_maintenance"
        params = [account_name, "true"]
        r = WalletCall(method, params)
        return r

    def sidechain_withdrawal_transaction(self, son_name, block_num, sidechain, peerplays_uid, peerplays_transaction_id, peerplays_from, widthdraw_sidechain, widthdraw_address, widthdraw_currency, widthdraw_amount):
        method =  "sidechain_withdrawal_transaction"
        params = [son_name, block_num, sidechain, peerplays_uid, peerplays_transaction_id, peerplays_from, widthdraw_sidechain, widthdraw_address, widthdraw_currency, widthdraw_amount, "true"]
        r = WalletCall(method, params)
        return r

    def sidechain_deposit_transaction(self, sidechain, transaction_id, operation_index, sidechain_from, sidechain_to, sidechain_currency, siechain_amount, peerplays_from_name_or_id, peerplays_to_name_or_id):
        """
        params:
           const sidechain_type& sidechain,
           const string &transaction_id,
           uint32_t operation_index,
           const string &sidechain_from,
           const string &sidechain_to,
           const string &sidechain_currency,
           int64_t sidechain_amount,
           const string &peerplays_from_name_or_id,
           const string &peerplays_to_name_or_id
        """
        method =  "sidechain_deposit_transaction"
        params = [sidechain, transaction_id, operation_index, sidechain_from, sidechain_to, sidechain_currency, siechain_amount, peerplays_from_name_or_id, peerplays_to_name_or_id, "true"]
        r = WalletCall(method, params)
        return r

    def vote_for_witness(self, voting_account, witness, approve):
        """
        params:
            string voting_account,
            string witness,
            bool approve,
            bool broadcast
        """
        method =  "vote_for_witness"
        params = [voting_account, witness, approve, "true"]
        r = WalletCall(method, params)
        return r

    def vote_for_son(self, voting_account, son, sidechain, approve):
        """
        params:
            string voting_account,
            string son,
            string sidechain,
            bool approve,
            bool broadcast
        """
        method =  "vote_for_son"
        params = [voting_account, son, sidechain, approve, "true"]
        r = WalletCall(method, params)
        return r

    def update_son_votes(self, voting_account, sons_to_approve, sons_to_reject, sidechain, desired_number_of_sons):
        """
        params:
            string voting_account,
            sons_to_approve,
            sons_to_reject,
            sidechain,
            desired_number_of_sons
        """
        method =  "update_son_votes"
        params = [voting_account, sons_to_approve, sons_to_reject, sidechain, desired_number_of_sons, "true"]
        r = WalletCall(method, params)
        return r

    def report_down(self):
        pass

    def heartbeat(self):
        pass

    def update_witness_votes (self, voting_account, witnesses_to_approve, witnesses_to_reject, desired_number_of_witnesses):
        """
        params:
            voting_account,
            witnesses_to_approve,
            witnesses_to_reject,
            desired_number_of_witnesses,
        """
        method =  "update_witness_votes"
        params = [voting_account, witnesses_to_approve, witnesses_to_reject, desired_number_of_witnesses, "true"]
        r = WalletCall(method, params)
        return r

if __name__ == "__main__":
    son = Son(urlWitness = urlWitness)
    # r = son.set_password("peerplays**")
    # r = son.create_son("sonaccount01", "http://sonaddreess01.com", [["bitcoin", "03456772301e221026269d3095ab5cb623fc239835b583ae4632f99a15107ef275"], ["ethereum", "5fbbb31be52608d2f52247e8400b7fcaa9e0bc12"], ["hive", "sonaccount01"], ["peerplays", "TEST8TCQFzyYDp3DPgWZ24261fMPSCzXxVyoF3miWeTj6JTi2DZdrL"]]) 
    # r = son.update_son("sonaccount01", "http://sonaddreess01.com", [["bitcoin", "03456772301e221026269d3095ab5cb623fc239835b583ae4632f99a15107ef275"], ["ethereum", "5fbbb31be52608d2f52247e8400b7fcaa9e0bc12"], ["hive", "sonaccount01"], ["peerplays", "TEST8TCQFzyYDp3DPgWZ24261fMPSCzXxVyoF3miWeTj6JTi2DZdrL"]]) 
    r = son.delete_sidechain_address("sonaccount01", "hive")
    r = son.request_son_maintenance("sonaccount01")
    print(r)
