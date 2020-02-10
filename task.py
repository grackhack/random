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


if __name__ == '__main__':
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, poolclass=NullPool)
    Session = sessionmaker(bind=engine)
    db = Session()
    message = {}
    for game_type in (constants.G1, constants.G2, constants.G3):
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
    if message:
        print(message)
        send_msg(message)
