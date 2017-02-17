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
            'updated_at': '2017-02-17',
            'rank': '30347',
            'lp': '4967',
            'league': 'Gold',
            'fav_char': 'Ryu',
            'account': 'STEAM',
            'country': 'Viet Nam',
            'ranked_counts': (841, 1649),
            'casual_counts': (79, 136),
        })

        image.show()
        badge_path = os.path.join(CURRENT_DIR, 'badges', 'rauden.png')
        self.assertTrue(os.path.isfile(badge_path))


class TestGetProfile(unittest.TestCase):

    def test_get_rauden(self):
        profile = util.get_profile('rauden')
        self.assertDictEqual(profile, {
            'fighter_id': 'Rauden',
            'updated_at': '2017-02-17',
            'rank': '30347',
            'lp': '4967',
            'league': 'Gold',
            'fav_char': 'Ryu',
            'account': 'STEAM',
            'country': 'Viet Nam',
            'ranked_counts': (841, 1649),
            'casual_counts': (79, 136),
        })


if __name__ == '__main__':
    unittest.main()
