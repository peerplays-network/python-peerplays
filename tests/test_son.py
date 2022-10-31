import unittest
import mock
from pprint import pprint
from peerplays import PeerPlays
from peerplays.account import Account
from peerplays.amount import Amount
from peerplays.asset import Asset
from peerplays.instance import set_shared_peerplays_instance
from peerplaysbase.operationids import getOperationNameForId
from .fixtures import fixture_data, peerplays
import string
import random

from peerplays.son import Son

# Initializing son objet
urlWitness = "http://10.11.12.101:8092"
son = Son(urlWitness = urlWitness)


class Testcases(unittest.TestCase):

    def setUp(self):
        # fixture_data()
        peerplays.nobroadcast = False
        peerplays.blocking = True
        pass

    def test_a(self):
        r = son.create_son("sonaccount01", "http://sonaddreess01.com", [["bitcoin", "03456772301e221026269d3095ab5cb623fc239835b583ae4632f99a15107ef275"], ["ethereum", "5fbbb31be52608d2f52247e8400b7fcaa9e0bc12"], ["hive", "sonaccount01"], ["peerplays", "TEST8TCQFzyYDp3DPgWZ24261fMPSCzXxVyoF3miWeTj6JTi2DZdrL"]]) 


    def test_account_creation(self):
        peerplays.blocking = True
        account_name = "".join(random.choices(string.ascii_lowercase, k=10))
        account_name = account_name + "".join(random.choices(string.digits, k=10))
        print("account_name:", account_name)
        peerplays.blocking = True
        print("peerplays blocking:", peerplays.blocking)

        op_res = peerplays.create_account(
            account_name,
            referrer="1.2.7",
            password=account_name,
            blocking=True
        )
        print("op_res_keys:", op_res.keys())
        print("op_res:", op_res)
        print("op_res_keys:", op_res.keys())
        self.assertTrue(op_res["operation_results"][0][0])
        account_id = op_res["operation_results"][0][1]
        account_name_from_chain = peerplays.rpc.get_object(account_id)["name"]
        self.assertEqual(account_name, account_name_from_chain)
        peerplays.transfer(account_name, 10000, "TEST", account="nathan")
        tx = peerplays.upgrade_account(account_name)
        account = Account(account_name)
        print("====================================", account, "============================")
        # tx = account.upgrade()
        ops = tx["operations"]
        op = ops[0][1]
        self.assertEqual(len(ops), 1)
        self.assertEqual(
            getOperationNameForId(ops[0][0]),
            "account_upgrade"
        )
        self.assertTrue(
            op["upgrade_to_lifetime_member"]
        )
        self.assertEqual(
            op["account_to_upgrade"],
            account["id"],
        )
        account_name = "test1234"
        r = son.create_son("sonaccount01", "http://sonaddreess01.com", [["bitcoin", "03456772301e221026269d3095ab5cb623fc239835b583ae4632f99a15107ef275"], ["ethereum", "5fbbb31be52608d2f52247e8400b7fcaa9e0bc12"], ["hive", "sonaccount01"], ["peerplays", "TEST8TCQFzyYDp3DPgWZ24261fMPSCzXxVyoF3miWeTj6JTi2DZdrL"]]) 
        print ("tested ========================")
        print(r)
