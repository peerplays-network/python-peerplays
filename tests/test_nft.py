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
        # fixture_data()
        self.nameMetadata = get_random_string(5)
        self.nameNft = get_random_string(5)
        # self.nameMetaData = "testmeta56"
        # self.nameNft = "testnft56"

    def test_nft(self):
        print("============nft test begin=========")
        self.setUp()
        # peerplays.blocking = True
        self.res = peerplays.nft_metadata_create("1.2.7",
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

        peerplays.nft_metadata_update("1.2.7",
                                      self.metadataId,
                                      self.nameMetadata + "m",
                                      self.nameMetadata + "m",
                                      self.nameMetadata + "m",
                                      "1.2.9",
                                      400,
                                      True,
                                      True)
        print("nft_metadata_update Success!")

        self.res = peerplays.nft_mint("1.2.7",
                           self.metadataId,
                           "1.2.7",
                           "1.2.7",
                           "1.2.7",
                           self.nameNft)
        print("nft_mint Success!")

        self.tokenId = self.res["operation_results"][0][1]

        peerplays.nft_safe_transfer_from("1.2.7",
                                         "1.2.7",
                                         "1.2.9",
                                         self.tokenId,
                                         "whatever")
        print("nft_safe_transfer_from Success!")

        peerplays.nft_approve("1.2.9", "1.2.8", self.tokenId)
        print("nft_approve Success!")

        peerplays.nft_set_approval_for_all("1.2.7", "1.2.10", True)
        print("nft_set_approval_for_all Success!")

        print("All tests successful!")

if __name__ == "__main__":
    self = Testcases()
    s = self
