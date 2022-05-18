import unittest
from pprint import pprint
from peerplays import PeerPlays
from peerplaysbase.operationids import getOperationNameForId
from peerplays.instance import set_shared_peerplays_instance
from .fixtures import fixture_data, peerplays, core_unit
import random
import string


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


class Testcases(unittest.TestCase):

    def setUp(self):
        fixture_data()
        self.nameMetadata = get_random_string(10)
        self.nameNft = get_random_string(10)

    def test_nft(self):

        self.setUp()

        self.res = peerplays.nft_metadata_create("1.2.9",
                                                 self.nameMetadata,
                                                 self.nameMetadata,
                                                 self.nameMetadata,
                                                 revenue_partner="1.2.8",
                                                 revenue_split=300,
                                                 is_sellable=False,
                                                 is_transferable=False)
        # peerplays.blocking = False
        print("nft_metadata_create Success!")

        self.metadataId = self.res["operation_results"][0][1]
        print("metadataId:", self.metadataId)

        peerplays.nft_metadata_update("1.2.9",
                                      self.metadataId,
                                      self.nameMetadata + "m",
                                      self.nameMetadata + "m",
                                      self.nameMetadata + "m",
                                      "1.2.9",
                                      400,
                                      True,
                                      True)
        print("nft_metadata_update Success!")

        self.res = peerplays.nft_mint("1.2.9",
                           self.metadataId,
                           "1.2.9",
                           "1.2.9",
                           "1.2.9",
                           self.nameNft)
        print("nft_mint Success!")

        self.tokenId = self.res["operation_results"][0][1]

        # offers = peerplays.rpc.get_offers_by_item("1.29.0", "1.31.5", 1) 
        offers = peerplays.rpc.get_offers_by_item("1.29.0", self.tokenId, 1) 
        if len(offers) >= 1:
            offer = offers[0]
            peerplays.cancel_offer("1.2.9", offer["id"]) 

        # peerplays.create_offer(["1.31.5"], "1.2.9", {"amount":5,"asset_id":"1.3.0"}, {"amount":15,"asset_id":"1.3.0"}, False, "2030-09-18T11:05:39", "") 
        peerplays.create_offer([self.tokenId], "1.2.9", {"amount":5,"asset_id":"1.3.0"}, {"amount":15,"asset_id":"1.3.0"}, False, "2030-09-18T11:05:39", "") 
        print("create_off Success!")

        # offers = peerplays.rpc.get_offers_by_item("1.29.0", "1.31.5", 1) 
        offers = peerplays.rpc.get_offers_by_item("1.29.0", self.tokenId, 1) 
        offer = offers[0]
        peerplays.create_bid("1.2.10", {"amount":8,"asset_id":"1.3.0"}, offer["id"]) 
        print("create_bid Success!")

        peerplays.cancel_offer("1.2.9", offer["id"]) 
        print("cancel_offer Success!")

        print("All tests successful!")
