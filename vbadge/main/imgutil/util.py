import os
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageFont, ImageDraw

VLEAGUE_URL = 'https://v-league.pro/player/%s/profile'

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CHAR_DIR = os.path.join(CURRENT_DIR, 'characters')
DEFAULT_BADGE_DIR = os.path.join(CURRENT_DIR, 'badges')
FONT_PATH = os.path.join(CURRENT_DIR, 'fonts/LeagueGothic-Regular.otf')

START_Y = 195
PADDING_X = 7
FID_FONT_SIZE = 40
BODY_TOP = 21
BODY_FONT_SIZE = 25


def create_badge(profile, badge_dir=DEFAULT_BADGE_DIR):

    if not os.path.isdir(badge_dir):
        os.mkdir(badge_dir)

    infile = os.path.join(CHAR_DIR, _character_filename(profile['fav_char']))
    image = Image.open(infile)

    # Write text on image

    draw = ImageDraw.Draw(image)
    fid_font = ImageFont.truetype(FONT_PATH, FID_FONT_SIZE)
    body_font = ImageFont.truetype(FONT_PATH, BODY_FONT_SIZE)

    draw.text((PADDING_X, START_Y), profile['fighter_id'], font=fid_font)

    _draw_body(draw, body_font, 'Country: ' + profile['country'], 0)
    _draw_body(draw, body_font, 'Rank: ' + profile['rank'], 1)
    _draw_body(draw, body_font, 'League: ' + profile['league'], 2)
    _draw_body(draw, body_font, 'League Points: ' + profile['lp'], 3)

    wins, total = profile['ranked_counts']
    _draw_body(draw,
               body_font,
               'Ranked Win Rate: %s%%' % str(wins / total * 100)[:4], 4)

    # Save badge
    outfile = os.path.join(badge_dir, profile['fighter_id'].lower() + '.png')
    image.save(outfile)

    return image


def _draw_body(draw, font, text, order):
    x = PADDING_X
    y = START_Y + BODY_TOP + FID_FONT_SIZE + BODY_FONT_SIZE * order
    draw.text((x, y), text, font=font)


def _character_filename(character_name):
    return character_name.lower().replace('.', '').replace('-', '') + '.jpg'


def get_profile(fighter_id):
    fighter_id = fighter_id.lower()
    resp = requests.get(VLEAGUE_URL % fighter_id)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.content, 'lxml')

    def split_counts(counts):
        return tuple(int(count) for count in counts.split('/'))

    def shorten_date(d):
        return d.split()[0]

    fields = [
        ('updated_at', 'Profile Update', shorten_date),
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
    profile_divs = soup.find('div', class_='profileBar').children
    for div in profile_divs:
        if (hasattr(div, 'text')):
            text = div.text.strip()
            if text.lower() == fighter_id:
                result['fighter_id'] = text
                break

    return result


def _field_value(soup, field_name, transform=lambda x: x):
    value = soup.find('td', text=field_name).next_sibling.text.strip()
    return transform(value)
