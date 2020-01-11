import os

basedir = os.path.abspath(os.path.dirname(__file__))
BOT_FATHER = os.environ.get('BOT_FATHER')
TOKEN = os.environ.get('TOKEN')


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'postgresql://postgres:postgress@localhost:5432/dev_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'not today'
    SQLALCHEMY_POOL_SIZE = 20
