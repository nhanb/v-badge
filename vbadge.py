import os
import requests
from bs4 import BeautifulSoup
from PIL import Image

VLEAGUE_URL = 'https://v-league.pro/player/%s/profile'
CHAR_DIR = 'characters'
BADGE_DIR = 'badges'


if not os.path.isdir(BADGE_DIR):
    os.mkdir(BADGE_DIR)


def create_badge(profile):
    infile = '%s/%s.jpg' % (CHAR_DIR, _character_filename(profile['fav_char']))
    image = Image.open(infile)

    # Write text on image
    # TODO

    outfile = '%s/%s.png' % (BADGE_DIR, profile['fighter_id'].lower())
    image.save(outfile)
    image.show()


def _character_filename(character_name):
    return character_name.lower().replace('.', '')


def get_profile(fighter_id):
    fighter_id = fighter_id.lower()
    resp = requests.get(VLEAGUE_URL % fighter_id)
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

    result = {key: _field_value(soup, *args) for key, *args in fields}

    result['fighter_id'] = fighter_id
    # Look for fighter ID in proper case
    breadcrumbs = soup.find('ol', class_='breadcrumb').children
    for b in breadcrumbs:
        if (hasattr(b, 'text')):
            text = b.text.strip()
            if text.lower() == fighter_id:
                result['fighter_id'] = text
                break

    return result


def _field_value(soup, field_name, transform=lambda x: x):
    value = soup.find('td', text=field_name).next_sibling.text.strip()
    return transform(value)
