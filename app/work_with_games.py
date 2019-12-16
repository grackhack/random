import datetime
import json
import re

import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app import constants
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
    results = ()
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


def get_all_data(date=datetime.datetime.now().strftime("%d.%m.%Y")):
    yesterday = (datetime.datetime.strptime(date, "%d.%m.%Y") - datetime.timedelta(days=2)).strftime("%d.%m.%Y")
    base_link = 'https://www.stoloto.ru/draw-results/12x24/load'
    data = {
        'mode': 'date',
        'super': 'false',
        'from': yesterday,
        'to': date,
    }
    games = []
    for page in range(1, 3):
        data['page'] = str(page),
        r = requests.post(base_link, data=data)
        if r.status_code == 200:
            res = json.loads(r.text)
            res = res['data']
            games.extend(_get_draw(res))
    return games


def refresh_game_stat(date):
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, poolclass=NullPool)
    Session = sessionmaker(bind=engine)
    db = Session()
    games = get_all_data(date)
    histoty = db.query(Game.date).all()

    for game in games:
        game_date = datetime.datetime.strptime(game[0], '%Y-%m-%d %H:%M:%S')
        if (game_date,) not in histoty:
            print(game_date)
            game = Game(game)
            db.add(game)
    db.commit()


def get_digit_info(digit):
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, poolclass=NullPool)
    result = engine.execute("""
        select array(select (case when de{} = TRUE then '1' else '0' end)
             from game
             order by date desc)
        """.format(digit))
    result = result.fetchone()
    str_res = ''.join(result[0])
    count_games = len(str_res)
    series = {}
    series_win = {}
    series_los = {}
    for d in constants.SW:
        series_win[d] = [m.start() + 1 for m in re.finditer(constants.SW[d], str_res)]
        series_los[d] = [m.start() + 1 for m in re.finditer(constants.SL[d], str_res)]

    series['W'] = series_win
    series['L'] = series_los
    return series, count_games
