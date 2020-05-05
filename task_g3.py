import datetime
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app import constants
from app.games import Loto
from app.work_with_games import get_all_data
from config import Config
from telega import send_msg


def prepare_msg(notices):
    user_messages = {}
    for user_id, rules in notices.items():
        msg = []
        for rule in rules:
            notice = json.loads(rule)
            digit = notice['game_digit']
            ser = notice['game_size']
            if notice['game_type'] == '3':
                gname = 'Топ 3'
            elif game_type == '2':
                gname = 'Дуэль'
            elif game_type == '4':
                gname = 'Рап1'
            elif game_type == '5':
                gname = 'Рап2'
            else:
                gname = '12x24'
            if notice['game_ser'] == '0':
                add = 'Выпадет'
                add2 = 'невыпадений'
            else:
                add = 'Не Выпадет'
                add2 = 'выпадений'

            msg.append(f'{gname}. Число: {digit} {add}. Серия {ser} {add2}')
        user_messages[user_id] = msg
    return user_messages


def get_full_notices(game_type: str):
    messages = {}
    loto = Loto(game_type=game_type)
    last_ser = loto.get_last_series()
    rules = loto.prepare_notices()
    for user_id, rule in rules.items():
        if user_id not in messages:
            notices = rule & last_ser
            if notices:
                messages[user_id] = notices
    return messages


def check_frame(f):
    DIG = 4
    s = sum([f[0].count('1'), f[1].count('1'), f[2].count('1')])
    one = f[0].count('1') > 0 and f[1].count('1') > 0 and f[2].count('1') > 0
    risk = all([f[0][2] == '0', f[1][2] == '0', f[2][2] == '0'])
    if not risk and one and s >= DIG:
        return s
    else:
        return 0


def quadro():
    msg = ''
    g = Loto(game_type=constants.G3)
    s0 = g.get_raw_data('0', limit=3)
    s1 = g.get_raw_data('1', limit=3)
    s2 = g.get_raw_data('2', limit=3)
    frame = (s0, s1, s2)

    res = check_frame(frame)
    if res > 0:
        msg = f'Квадрат размером: {res}\n{s0}\n{s1}\n{s2}'
    return msg


if __name__ == '__main__':
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, poolclass=NullPool)
    Session = sessionmaker(bind=engine)
    db = Session()
    message = {}
    for game_type in (constants.G3, constants.G4, constants.G5):
        game_model = constants.GAME_MAP[game_type]['model']
        games = get_all_data(game_type=game_type)
        histoty = db.query(game_model.date).all()
        for game in games:
            game_date = datetime.datetime.strptime(game[0], '%Y-%m-%d %H:%M:%S')
            if (game_date,) not in histoty:
                game = game_model(game)
                db.add(game)
        db.commit()
        notices = get_full_notices(game_type=game_type)
        if notices:
            print(notices)
            user_messages = prepare_msg(notices)
            for user_id, msg_list in user_messages.items():
                if user_id in message:
                    message[user_id].extend(msg_list)
                else:
                    message[user_id] = msg_list
    try:
        add_msg = quadro()
        if add_msg:
            if message and 1 in message:
                message[1].append(add_msg)
            else:
                message[1] = add_msg
    except Exception:
        pass

    if message:
        print(message)
        send_msg(message)
