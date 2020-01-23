import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app import constants
from app.work_with_games import get_last_series, get_all_data
from config import Config
from telega import send_msg


def prepare_msg(series, game_type):
    msg = []
    if game_type == '3':
        gname = 'Топ 3'
    elif game_type == '2':
        gname = 'Дуэль'
    else:
        gname = '12x24'
    for digit, win, ser in series:
        if win == '0':
            add = 'Выпадет'
            add2 = 'невыпадений'
        else:
            add = 'Не Выпадет'
            add2 = 'выпадений'

        msg.append(f'{gname}. Число: {digit} {add}. Серия {ser} {add2}')
    return msg


if __name__ == '__main__':
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, poolclass=NullPool)
    Session = sessionmaker(bind=engine)
    db = Session()
    message = []
    for game_type in (constants.G1, constants.G2, constants.G3):
        game_model = constants.GAME_MAP[game_type]['model']
        games = get_all_data(game_type=game_type)
        histoty = db.query(game_model.date).all()
        for game in games:
            game_date = datetime.datetime.strptime(game[0], '%Y-%m-%d %H:%M:%S')
            if (game_date,) not in histoty:
                game = game_model(game)
                print(game)
                db.add(game)
        db.commit()
        series = get_last_series(game_type=game_type)
        if series:
            print(series)
            msg = prepare_msg(series, game_type)
            message.extend(msg)
    if message:
        message = '\n'.join(message)
        print(message)
        send_msg(message)
