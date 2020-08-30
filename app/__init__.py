# init.py
# essentially this makes the 'app' folder a package that can be imported

from config import Config
from flask import Flask
from flask_admin import Admin
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Make app
app = Flask(__name__)

# Configure logging
# Get user name
import getpass
name = getpass.getuser()
# Get number of log files
import fnmatch
import os
num = len(fnmatch.filter(os.listdir('testing/logs'), '*.log'))
# Use above to generate name of log file
new = 'testing/logs/test' + name + str(num) + '.log'
# Log into log file
import logging
logging.basicConfig(filename=new, level=logging.INFO)

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

Bootstrap(app)
admin = Admin(app, name='Admin', template_mode='bootstrap3')

from app.auth import bp as auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth')



with app.app_context():
    if db.engine.url.drivername == 'sqlite':
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

from app import routes, models

