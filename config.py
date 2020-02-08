import os

from sqlalchemy.pool import QueuePool

basedir = os.path.abspath(os.path.dirname(__file__))
BOT_FATHER = os.environ.get('BOT_FATHER')
ALEX = os.environ.get('ALEX')
DOZ = os.environ.get('DOZ')
OLEG = os.environ.get('OLEG')


TOKEN = os.environ.get('TOKEN')


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'postgresql://postgres:postgress@localhost:5432/dev_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'not today'
    SQLALCHEMY_POOL_SIZE = 20
    # SQLALCHEMY_ENGINE_OPTIONS = {
    #     'pool': QueuePool,
    #     'pool_size': 20,
    #     'pool_recycle': 120,
    #     'pool_pre_ping': True
    # }
