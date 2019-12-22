import datetime
import json
import re
from itertools import zip_longest

import numpy as np
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
    print(date, len(games))
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
        series_win[d] = [m.start() + 2 for m in re.finditer(constants.SW[d], str_res)]
        series_los[d] = [m.start() + 2 for m in re.finditer(constants.SL[d], str_res)]

    series['W'] = series_win
    series['L'] = series_los
    return series, count_games


def get_diff_series(series):
    full_series = {}
    for pl, item in series.items():
        full_series[pl] = {}
        for i in range(6, constants.CNT_REGEX):
            tmp = []
            full_series[pl][str(i)] = {}
            for d, v in item.items():
                if int(d) >= i:
                    tmp.extend(v)
            sort_tmp = sorted(tmp)
            full_series[pl][str(i)] = sort_tmp
            if len(tmp) > 1:

                diff = [j - i for i, j in zip(sort_tmp[:-1], sort_tmp[1:])]
                avg = round(sum(diff) / len(diff))
                full_series[pl][str(i) + 'avg'] = avg
                if sort_tmp[0] == 1:
                    next_ser = sort_tmp[1] - avg
                else:
                    next_ser = sort_tmp[0] - avg
                if next_ser <= 0:
                    full_series[pl][str(i) + 'next'] = f'Примерно через {abs(next_ser)} игр'
                else:
                    full_series[pl][str(i) + 'next'] = f'Должна была быть {next_ser} игр назад'
    return full_series


def get_count_series(digit):
    series, cnt = get_digit_info(digit)
    step = (cnt + constants.XTICK) // constants.XTICK

    line_x = sorted([i for i in range(cnt, 0, -step)])
    line_x = [line_x[0] - step] + line_x
    full_series = {}
    for pl, item in series.items():
        full_series[pl] = {}
        for d, v in item.items():
            count, division = np.histogram(v, bins=line_x)
            full_series[pl][d] = count.tolist()
    dataset = prepare_dataset(full_series)
    dataset['lost_games'] = f'Осталось {abs(line_x[0])} игр в срезе по {step}'
    return dataset


def prepare_dataset(data):
    all_data = {}

    colors = ['#16f1f1', '#ffc107', '#ff60eb', '#28a745', '#dc3545', '#007bff', '#6f42c1', ]

    for pl, item in data.items():
        dataset = {}
        dataset['datasets'] = []
        tmp_avg = [0] * constants.XTICK
        for d, row in item.items():
            if 3 < int(d) < 11:
                dataset['datasets'].append({'data': row,
                                            'backgroundColor': colors[int(d) - 4],
                                            })
                tmp_avg = [sum(i) for i in zip_longest(tmp_avg, row, fillvalue=0)]

        all_data[pl] = dataset
        dataset['labels'] = tmp_avg
    return all_data


def calculate_bets(user):
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, poolclass=NullPool)

    result = engine.execute(constants.USERS_ID)
    users = result.fetchall()
    for (user,) in users:
        result = engine.execute(constants.PL_GAMES, (user,))
        pl_games = result.fetchall()
        for gid, dt, digit, win, bet, sum in pl_games:
            res = engine.execute(constants.PL_GAME_RES.format(de=digit), (dt,))
            data_res = res.fetchone()
            if data_res:
                if win == bool(data_res[0]):
                    sum = round(constants.KOEF * bet, 2)
                else:
                    sum = 0
                engine.execute(constants.UPDATE_SUM, (sum, gid))


def get_balance(user):
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, poolclass=NullPool)
    result = engine.execute(constants.WIN_SUM, (user,))
    win_sum = result.fetchone()[0]
    result = engine.execute(constants.BALANCE, (user,))
    balance = result.fetchone()[0]
    balance = balance + win_sum
    return balance
