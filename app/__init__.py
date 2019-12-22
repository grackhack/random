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


# Welcome to the Flask-Bootstrap sample application. This will give you a
# guided tour around creating an application using Flask-Bootstrap.
#
# To run this application yourself, please install its requirements first:
#
#   $ pip install -r sample_app/requirements.txt
#
# Then, you can actually run the application.
#
#   $ flask --app=sample_app dev
#
# Afterwards, point your browser to http://localhost:5000, then check out the
# source.

# from flask import Flask
# from flask_appconfig import AppConfig
# from flask_bootstrap import Bootstrap

# from .frontend import frontend
# from .nav import nav
#
#
# def create_app(configfile=None):
#     # We are using the "Application Factory"-pattern here, which is described
#     # in detail inside the Flask docs:
#     # http://flask.pocoo.org/docs/patterns/appfactories/
#
#     app = Flask(__name__,
#     static_url_path='',
#             static_folder='app/static',
#             template_folder='app/templates')
#
#     # We use Flask-Appconfig here, but this is not a requirement
#     AppConfig(app)
#
#     # Install our Bootstrap extension
#     Bootstrap(app)
#
#     # Our application uses blueprints as well; these go well with the
#     # application factory. We already imported the blueprint, now we just need
#     # to register it:
#     app.register_blueprint(frontend)
#
#     # Because we're security-conscious developers, we also hard-code disabling
#     # the CDN support (this might become a default in later versions):
#     app.config['BOOTSTRAP_SERVE_LOCAL'] = True
#
#     # We initialize the navigation as well
#     nav.init_app(app)
#
#     return app