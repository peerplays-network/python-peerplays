import unittest
from pprint import pprint
from peerplays import PeerPlays
from peerplaysbase.operationids import getOperationNameForId
from peerplays.instance import set_shared_peerplays_instance
from .fixtures import fixture_data, peerplays, core_unit


class Testcases(unittest.TestCase):

    def setUp(self):
        fixture_data()
        self.testperm = "testperm1"
        self.clean_previous_test()

    def clean_previous_test(self):
        custom_permissions_existing = peerplays.rpc.get_custom_permissions("1.2.7")
        for permission in custom_permissions_existing:
            if permission["permission_name"] == self.testperm:
                permission_id = permission['id']
                peerplays.custom_permission_delete(
                        permission_id,
                        owner_account="1.2.7")
                print(self.testperm, " deleted!")
        print("Cleaning done!")


    def test_custom_permission_create(self):
        peerplays.custom_permission_create(
            self.testperm,
            owner_account="1.2.7",
            weight_threshold=1,
            account_auths=[["1.2.8", 1]])
        self.assertEqual(1, 1)

if __name__ == "__main__":
    unittest.main()
