import datetime
from app import login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    balance = db.Column(db.Float, default=10000.0)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True, unique=True)
    de1 = db.Column(db.Boolean)
    de2 = db.Column(db.Boolean)
    de3 = db.Column(db.Boolean)
    de4 = db.Column(db.Boolean)
    de5 = db.Column(db.Boolean)
    de6 = db.Column(db.Boolean)
    de7 = db.Column(db.Boolean)
    de8 = db.Column(db.Boolean)
    de9 = db.Column(db.Boolean)
    de10 = db.Column(db.Boolean)
    de11 = db.Column(db.Boolean)
    de12 = db.Column(db.Boolean)
    de13 = db.Column(db.Boolean)
    de14 = db.Column(db.Boolean)
    de15 = db.Column(db.Boolean)
    de16 = db.Column(db.Boolean)
    de17 = db.Column(db.Boolean)
    de18 = db.Column(db.Boolean)
    de19 = db.Column(db.Boolean)
    de20 = db.Column(db.Boolean)
    de21 = db.Column(db.Boolean)
    de22 = db.Column(db.Boolean)
    de23 = db.Column(db.Boolean)
    de24 = db.Column(db.Boolean)

    def __init__(self, game: list):
        self.date = datetime.datetime.strptime(game[0], '%Y-%m-%d %H:%M:%S')
        des = [i for i in dir(self) if not callable(i) if 'de' in i and '_' not in i]
        for de in game[1:]:
            if f'de{de}' in des:
                self.__setattr__(f'de{de}', True)

    def __repr__(self):
        des = [i for i in dir(self) if not callable(i) if 'de' in i and '_' not in i]
        digits = [de[2:] for de in des if getattr(self, de)]
        digits = ' '.join(digits)
        return f'{self.date}: {digits}'


class PlayGame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    game_id = db.Column(db.Integer, db.ForeignKey('play.id'))
    game_num = db.Column(db.BigInteger)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)


class Play(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_time = db.Column(db.DateTime)
    game_digit = db.Column(db.Integer)
    game_dig = db.Column(db.String(16))
    game_series = db.Column(db.Boolean)
    game_bet = db.Column(db.Integer)
    game_result = db.Column(db.Float)
    game_win = db.Column(db.Boolean)
    game_stat = db.Column(db.JSON)
    game_type = db.Column(db.Integer)
    game_koef = db.Column(db.Float)


class Game3(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True, unique=True)
    de0 = db.Column(db.Boolean)
    de1 = db.Column(db.Boolean)
    de2 = db.Column(db.Boolean)
    de3 = db.Column(db.Boolean)
    de4 = db.Column(db.Boolean)
    de5 = db.Column(db.Boolean)
    de6 = db.Column(db.Boolean)
    de7 = db.Column(db.Boolean)
    de8 = db.Column(db.Boolean)
    de9 = db.Column(db.Boolean)
    s1 = db.Column(db.Integer)
    s2 = db.Column(db.Integer)

    def __init__(self, game: list):
        self.date = datetime.datetime.strptime(game[0], '%Y-%m-%d %H:%M:%S')
        des = [i for i in dir(self) if not callable(i) if 'de' in i and '_' not in i]
        self.__setattr__('s1', sum(game[1:]))
        for de in game[1:]:
            if f'de{de}' in des:
                self.__setattr__(f'de{de}', True)

    def __repr__(self):
        des = [i for i in dir(self) if not callable(i) if 'de' in i and '_' not in i]
        digits = [de[2:] for de in des if getattr(self, de)]
        digits = ' '.join(digits)
        return f'{self.date}: {digits}'


class Game2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True, unique=True)
    de1 = db.Column(db.Boolean)
    de2 = db.Column(db.Boolean)
    de3 = db.Column(db.Boolean)
    de4 = db.Column(db.Boolean)
    de5 = db.Column(db.Boolean)
    de6 = db.Column(db.Boolean)
    de7 = db.Column(db.Boolean)
    de8 = db.Column(db.Boolean)
    de9 = db.Column(db.Boolean)
    de10 = db.Column(db.Boolean)
    de11 = db.Column(db.Boolean)
    de12 = db.Column(db.Boolean)
    de13 = db.Column(db.Boolean)
    de14 = db.Column(db.Boolean)
    de15 = db.Column(db.Boolean)
    de16 = db.Column(db.Boolean)
    de17 = db.Column(db.Boolean)
    de18 = db.Column(db.Boolean)
    de19 = db.Column(db.Boolean)
    de20 = db.Column(db.Boolean)
    de21 = db.Column(db.Boolean)
    de22 = db.Column(db.Boolean)
    de23 = db.Column(db.Boolean)
    de24 = db.Column(db.Boolean)
    de25 = db.Column(db.Boolean)
    de26 = db.Column(db.Boolean)

    def __init__(self, game: list):
        self.date = datetime.datetime.strptime(game[0], '%Y-%m-%d %H:%M:%S')
        des = [i for i in dir(self) if not callable(i) if 'de' in i and '_' not in i]
        for de in game[1:]:
            if f'de{de}' in des:
                self.__setattr__(f'de{de}', True)

    def __repr__(self):
        des = [i for i in dir(self) if not callable(i) if 'de' in i and '_' not in i]
        digits = [de[2:] for de in des if getattr(self, de)]
        digits = ' '.join(digits)
        return f'{self.date}: {digits}'


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    rules = db.Column(db.JSON)
    skip_time = db.Column(db.JSON)


class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    rules = db.Column(db.JSON)

class Game4(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True, unique=True)
    de1 = db.Column(db.Boolean)
    de2 = db.Column(db.Boolean)
    de3 = db.Column(db.Boolean)
    de4 = db.Column(db.Boolean)
    de5 = db.Column(db.Boolean)
    de6 = db.Column(db.Boolean)
    de7 = db.Column(db.Boolean)
    de8 = db.Column(db.Boolean)
    de9 = db.Column(db.Boolean)
    de10 = db.Column(db.Boolean)
    de11 = db.Column(db.Boolean)
    de12 = db.Column(db.Boolean)
    de13 = db.Column(db.Boolean)
    de14 = db.Column(db.Boolean)
    de15 = db.Column(db.Boolean)
    de16 = db.Column(db.Boolean)
    de17 = db.Column(db.Boolean)
    de18 = db.Column(db.Boolean)
    de19 = db.Column(db.Boolean)
    de20 = db.Column(db.Boolean)
    b1 = db.Column(db.Boolean)
    b2 = db.Column(db.Boolean)
    b3 = db.Column(db.Boolean)
    b4 = db.Column(db.Boolean)


    def __init__(self, game: list):
        self.date = datetime.datetime.strptime(game[0], '%Y-%m-%d %H:%M:%S')
        des = [i for i in dir(self) if not callable(i) if 'de' in i and '_' not in i]
        for de in game[1:10]:
            if f'de{de}' in des:
                self.__setattr__(f'de{de}', True)
        self.__setattr__(f'b{game[9]}', True)


    def __repr__(self):
        des = [i for i in dir(self) if not callable(i) if 'de' in i and '_' not in i]
        digits = [de[2:] for de in des if getattr(self, de)]
        digits = ' '.join(digits)
        return f'{self.date}: {digits}'


class Game5(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, index=True, unique=True)
    de1 = db.Column(db.Boolean)
    de2 = db.Column(db.Boolean)
    de3 = db.Column(db.Boolean)
    de4 = db.Column(db.Boolean)
    de5 = db.Column(db.Boolean)
    de6 = db.Column(db.Boolean)
    de7 = db.Column(db.Boolean)
    de8 = db.Column(db.Boolean)
    de9 = db.Column(db.Boolean)
    de10 = db.Column(db.Boolean)
    de11 = db.Column(db.Boolean)
    de12 = db.Column(db.Boolean)
    de13 = db.Column(db.Boolean)
    de14 = db.Column(db.Boolean)
    de15 = db.Column(db.Boolean)
    de16 = db.Column(db.Boolean)
    de17 = db.Column(db.Boolean)
    de18 = db.Column(db.Boolean)
    de19 = db.Column(db.Boolean)
    de20 = db.Column(db.Boolean)
    b1 = db.Column(db.Boolean)
    b2 = db.Column(db.Boolean)
    b3 = db.Column(db.Boolean)
    b4 = db.Column(db.Boolean)

    def __init__(self, game: list):
        self.date = datetime.datetime.strptime(game[0], '%Y-%m-%d %H:%M:%S')
        des = [i for i in dir(self) if not callable(i) if 'de' in i and '_' not in i]
        for de in game[1:10]:
            if f'de{de}' in des:
                self.__setattr__(f'de{de}', True)
        self.__setattr__(f'b{game[9]}', True)

    def __repr__(self):
        des = [i for i in dir(self) if not callable(i) if 'de' in i and '_' not in i]
        digits = [de[2:] for de in des if getattr(self, de)]
        digits = ' '.join(digits)
        return f'{self.date}: {digits}'