import datetime
import json
import re

import requests
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Game
from config import Config


def _convert_items(items):
    res = []
    rows = [item.strip().split(' ') for item in items]
    for item in rows:
        tmp = [int(i) for i in item]
        res.append(tmp)
    return res


def _get_draw(data):
    results = None
    text = data.replace('\n', ''
                        ).replace('  ', ' '
                                  ).replace('\t', ''
                                            ).replace('&nbsp;', ' '
                                                      ).replace('<b>', ''
                                                                ).replace('</b>', ''
                                                                          )
    DDATA = re.compile(r'<div class="draw_date" title="([\d+.]+ [\d\:]+)">[\d+.]+ [\d\:]+</div>')
    DIGITS = re.compile(r'<span class="zone">([\d ]+)</span>')
    date_items = DDATA.findall(text)
    str_dates = [f'{d[6:10]}-{d[3:5]}-{d[:2]} {d[-8:-3]}:00' for d in date_items]
    draw_items = DIGITS.findall(text)
    if len(date_items) == len(draw_items):
        draw_items = _convert_items(draw_items)
        results = [[a, *b] for a, b in list(zip(str_dates, draw_items))]
    return results


def get_all_data():
    date = datetime.datetime.now().strftime("%d.%m.%Y")
    yesterday = (datetime.date.today() - datetime.timedelta(days=2)).strftime("%d.%m.%Y")
    base_link = 'https://www.stoloto.ru/draw-results/12x24/load'
    data = {
        'mode': 'date',
        'super': 'false',
        'from': yesterday,
        'to': date,
    }
    games = []
    for page in range(1, 2):
        data['page'] = str(page),
        r = requests.post(base_link, data=data)
        if r.status_code == 200:
            res = json.loads(r.text)
            res = res['data']
            games.extend(_get_draw(res))
    return games


if __name__ == '__main__':
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine, pool_size=20, max_overflow=0)
    db = Session()
    games = get_all_data()
    histoty = db.query(Game.date).all()

    for game in games:
        game_date = datetime.datetime.strptime(game[0], '%Y-%m-%d %H:%M:%S')
        if (game_date,) not in histoty:
            game = Game(game)
            print(game)
            db.add(game)
    db.commit()
