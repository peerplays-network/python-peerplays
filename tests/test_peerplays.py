import unittest
from pprint import pprint
from peerplays import PeerPlays

wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"


class Testcases(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ppy = PeerPlays(
            nobroadcast=True,
            wif={
                "active": wif
            })

    def test_connect(self):
        self.ppy.connect()

    def test_info(self):
        info = self.ppy.info()
        for key in ['current_witness',
            'head_block_id',
            'head_block_number',
            'id',
            'last_irreversible_block_num',
            'next_maintenance_time',
            'random',
            'recently_missed_count',
            'time']:
            self.assertTrue(key in info)
#        self.assertEqual(1, 1)
