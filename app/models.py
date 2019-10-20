import datetime

from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)


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
