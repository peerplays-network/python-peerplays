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


    def test_rbac(self):
        peerplays.custom_permission_create(
            self.testperm,
            owner_account="1.2.7",
            weight_threshold=1,
            account_auths=[["1.2.8", 1]])
        print("custom_permission_create success")

        custom_permissions_existing = peerplays.rpc.get_custom_permissions("1.2.7")
        for permission in custom_permissions_existing:
            if permission["permission_name"] == self.testperm:
                permission_id = permission['id']
                peerplays.custom_permission_update(
                        permission_id,
                        weight_threshold=1,
                        account_auths=[["1.2.9", 2]],
                        owner_account="1.2.7"
                )
                break
        print("custom_permission_update success")

        custom_permissions_existing = peerplays.rpc.get_custom_permissions("1.2.7")
        for permission in custom_permissions_existing:
            if permission["permission_name"] == self.testperm:
                permission_id = permission['id']
                op = peerplays.custom_account_authority_create(
                        permission_id,
                        0,
                        "2020-07-27T00:00:00",
                        "2030-07-27T00:00:00",
                        owner_account="1.2.7") 
                print("custom_account_authority_create success")
                break
        
        authorities = peerplays.rpc.get_custom_account_authorities("1.2.7")
        authority = authorities[0]
        authority_id = authority["id"]
        op = peerplays.custom_account_authority_update(
                authority_id,
                "2020-07-27T00:00:00",
                "2040-07-27T00:00:00",
                owner_account="1.2.7")
        print("custom_account_authority_update success")

        authorities = peerplays.rpc.get_custom_account_authorities("1.2.7")
        authority = authorities[0]
        authority_id = authority["id"]
        op = peerplays.custom_account_authority_delete(
                authority_id,
                owner_account="1.2.7")
        print("custom_account_authority_deletete success")

        custom_permissions_existing = peerplays.rpc.get_custom_permissions("1.2.7")
        for permission in custom_permissions_existing:
            if permission["permission_name"] == self.testperm:
                permission_id = permission['id']
                peerplays.custom_permission_delete(
                        permission_id,
                        owner_account="1.2.7"
                )
                break
        print("custom_permission_delete success")


if __name__ == "__main__":
    unittest.main()
