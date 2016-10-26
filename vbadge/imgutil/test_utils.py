import os
import unittest
from . import utils
import requests_cache

requests_cache.install_cache('requests_cache')


class TestCreateBadge(unittest.TestCase):

    def test_read_badge(self):
        image = utils.create_badge({
            'fighter_id': 'Rauden',
            'updated_at': '2016-10-25',
            'rank': '25459',
            'lp': '4525',
            'league': 'Gold',
            'fav_char': 'Ryu',
            'account': 'STEAM',
            'country': 'Viet Nam',
            'ranked_counts': (621, 1228),
            'casual_counts': (45, 83),
        })

        image.show()
        img = os.path.dirname(os.path.abspath(__file__)) + '/badges/rauden.png'
        self.assertTrue(os.path.isfile(img))


class TestGetProfile(unittest.TestCase):

    def test_get_rauden(self):
        profile = utils.get_profile('rauden')
        self.assertEqual(profile, {
            'fighter_id': 'Rauden',
            'updated_at': '2016-10-25',
            'rank': '25459',
            'lp': '4525',
            'league': 'Gold',
            'fav_char': 'Ryu',
            'account': 'STEAM',
            'country': 'Viet Nam',
            'ranked_counts': (621, 1228),
            'casual_counts': (45, 83),
        })


if __name__ == '__main__':
    unittest.main()
