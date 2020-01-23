from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates'
            )
app.config.from_object(Config)

from . import filters
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)
login = LoginManager(app)
login.login_view = 'login'



from app import routes, models


