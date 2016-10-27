import os
import unittest
from . import util
import requests_cache

requests_cache.install_cache('requests_cache')
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


class TestCreateBadge(unittest.TestCase):

    def test_read_badge(self):
        image = util.create_badge({
            'fighter_id': 'Rauden',
            'updated_at': '2016-10-25',
            'rank': '25459',
            'lp': '4525',
            'league': 'Gold',
            'fav_char': 'Chun-Li',
            'account': 'STEAM',
            'country': 'Viet Nam',
            'ranked_counts': (621, 1228),
            'casual_counts': (45, 83),
        })

        image.show()
        badge_path = os.path.join(CURRENT_DIR, 'badges', 'rauden.png')
        self.assertTrue(os.path.isfile(badge_path))


class TestGetProfile(unittest.TestCase):

    def test_get_rauden(self):
        profile = util.get_profile('rauden')
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
