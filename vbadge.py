import requests
from bs4 import BeautifulSoup

VLEAGUE_URL = 'https://v-league.pro/player/%s/profile'


def get_profile(fighter_id):
    resp = requests.get(VLEAGUE_URL % fighter_id.lower())
    resp.raise_for_status()
    soup = BeautifulSoup(resp.content, 'lxml')

    def split_counts(counts):
        return tuple(int(count) for count in counts.split('/'))

    fields = [
        ('updated_at', 'Profile Update'),
        ('rank', 'Rank', lambda x: x[:x.find('(')].strip()),
        ('lp', 'League Points'),
        ('league', 'League'),
        ('fav_char', 'Favorite Character'),
        ('account', 'Account'),
        ('country', 'Country'),
        ('ranked_counts', 'Ranked Match', split_counts),
        ('casual_counts', 'Casual Match', split_counts),
    ]

    return {key: _field_value(soup, *args) for key, *args in fields}


def _field_value(soup, field_name, transform=lambda x: x):
    value = soup.find('td', text=field_name).next_sibling.text.strip()
    return transform(value)
