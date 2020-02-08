import datetime
import json
import re
from itertools import zip_longest

import numpy as np
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from typing import Tuple, Dict

from app import constants
from app.games import Loto
from app.models import Game
from config import Config


def _convert_items(items):
    res = []
    rows = [item.strip().split(' ') for item in items]
    for item in rows:
        tmp = [int(i) for i in item]
        res.append(tmp)
    return res


def _get_draw(data, game_type):
    if game_type == '2':
        DIGITS = re.compile(
            r"""<span class="zone"><b class='right'>([\d]+) <b class='right'>([\d]+) </span><span class="zone"><b class='left'>([\d]+) <b class='left'>([\d]+) </span>""")
    else:
        DIGITS = re.compile(r'<span class="zone">([\d ]+)</span>')

    results = ()
    text = data.replace('\n', ''
                        ).replace('  ', ' '
                                  ).replace('\t', ''
                                            ).replace('&nbsp;', ' '
                                                      ).replace('<b>', ''
                                                                ).replace('</b>', ''
                                                                          )
    DDATA = re.compile(r'<div class="draw_date" title="([\d+.]+ [\d\:]+)">[\d+.]+ [\d\:]+</div>')
    date_items = DDATA.findall(text)
    str_dates = [f'{d[6:10]}-{d[3:5]}-{d[:2]} {d[-8:-3]}:00' for d in date_items]
    draw_items = DIGITS.findall(text)
    if game_type == '2' and draw_items:
        draw_items = [' '.join(list(item)) for item in draw_items]
    if len(date_items) == len(draw_items):
        draw_items = _convert_items(draw_items)
        results = [[a, *b] for a, b in list(zip(str_dates, draw_items))]
    return results


def get_all_data(date=datetime.datetime.now().strftime("%d.%m.%Y"), game_type='1'):
    yesterday = (datetime.datetime.strptime(date, "%d.%m.%Y") - datetime.timedelta(days=2)).strftime("%d.%m.%Y")
    base_link = constants.GAME_MAP[game_type]['base_link']
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
            parsed_data = _get_draw(res, game_type)
            games.extend(parsed_data)
    return games


def refresh_game_stat(date, game_type: str):
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, poolclass=NullPool)
    Session = sessionmaker(bind=engine)
    db = Session()
    game_model = constants.GAME_MAP[game_type]['model']
    games = get_all_data(date, game_type)
    histoty = db.query(game_model.date).all()
    print(date, len(games))
    for game in games:
        game_date = datetime.datetime.strptime(game[0], '%Y-%m-%d %H:%M:%S')
        if (game_date,) not in histoty:
            print(game_date)
            game = game_model(game)
            db.add(game)
    db.commit()


def get_max_games(game_type: str) -> int:
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, poolclass=NullPool)
    tbl_name = constants.GAME_MAP[game_type]['tbl']
    result = engine.execute(f'select count(*) from {tbl_name}')
    result = result.fetchone()[0]
    return result


def get_raw_data(digit: str, game_type: str, limit=0) -> str:
    """Строка 1/0 за все игры для числа и количество"""
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, poolclass=NullPool)
    tbl_name = constants.GAME_MAP[game_type]['tbl']
    limit_str = f'limit {limit}' if limit > 0 else ''
    result = engine.execute("""
            select array(select (case when de{d:} = TRUE then '1' else '0' end)
                 from {tbl:}
                 order by date desc {limit:})
            """.format(d=digit, tbl=tbl_name, limit=limit_str))
    result = result.fetchone()
    raw = ''.join(result[0])
    return raw


def get_last_series(game_type: str):
    """"Получить последние серии для всех чисел"""
    current_series = []
    for digit in constants.GAME_MAP[game_type]['range']:
        raw = get_raw_data(digit, game_type)
        tmp = raw[:constants.CNT_REGEX]
        cnt = 0
        s = tmp[0]
        for i in tmp:
            if i == s:
                cnt += 1
            else:
                current_series.append((digit, s, cnt))
                break
    if game_type == constants.G2:
        series = list(filter(
            lambda x: constants.MIN_TELE_S + constants.SHIFT_G2 <= x[2] <= constants.MAX_TELE_S + constants.SHIFT_G2,
            current_series))
    elif game_type == constants.G3:
        series = list(filter(
            lambda x: constants.MIN_TELE_S + constants.SHIFT_G3 <= x[2] <= constants.MAX_TELE_S + constants.SHIFT_G3,
            current_series))
    else:
        series = list(filter(lambda x: constants.MIN_TELE_S <= x[2] <= constants.MAX_TELE_S, current_series))
    return series


def get_dataset_series(digit, game_type):
    """Количество серий для каждого числа"""
    cnt = get_max_games(game_type)
    loto = Loto(game_type=game_type)
    series = loto.get_raw_series(digit)
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
    """Даннные для гистограммы """
    all_data = {}

    colors = ['#16f1f1', '#ffc107', '#ff60eb', '#28a745', '#dc3545', '#007bff', '#6f42c1', ]
    for pl, item in data.items():
        dataset = {}
        dataset['datasets'] = []
        tmp_avg = [0] * constants.XTICK
        for d, row in item.items():
            if constants.MIN_SERIES <= int(d) < constants.MIN_SERIES + len(colors):
                dataset['datasets'].append({'data': row, 'backgroundColor': colors[int(d) - len(colors)]})
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
        for gid, dt, digit, win, bet, sum, game_type, game_koef in pl_games:
            tbl_name = constants.GAME_MAP[str(game_type) or constants.G1]['tbl']
            res = engine.execute(constants.PL_GAME_RES.format(de=digit, tbl=tbl_name), (dt,))
            data_res = res.fetchone()
            if data_res:
                if win == bool(data_res[0]):
                    if not game_koef:
                        game_koef = 1.92
                    sum = round(game_koef * bet, 2)
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


def get_all_balance():
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, poolclass=NullPool)
    result = engine.execute(constants.USERS_BAL).fetchall()
    return result


def get_groups(count: int, game_type: str) -> dict:
    groups = {'0': [], '1': []}
    mask0 = '0' * count + '1'
    mask1 = '1' * count + '0'
    for digit in constants.GAME_MAP[game_type]['range']:
        row = get_raw_data(digit, game_type, limit=count + 1)
        if row == mask0:
            groups['0'].append(digit)
        if row == mask1:
            groups['1'].append(digit)
    return groups

