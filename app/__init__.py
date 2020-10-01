# init.py
# essentially this makes the 'app' folder a package that can be imported

from app import logging
from config import Config
from flask import Flask
from flask_admin import Admin
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Make app
app = Flask(__name__)

# Initialize config
app.config.from_object(Config)

# Initialize database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'

# Initialize admin
Bootstrap(app)
admin = Admin(app, name='Admin', template_mode='bootstrap3')

from app.auth import bp as auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth')

from app.myadmin import bp as myadmin_bp
app.register_blueprint(myadmin_bp, url_prefix='/myadmin')

with app.app_context():
    if db.engine.url.drivername == 'sqlite':
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

# Import routes and models
from app import routes
from app import models

# Start logging
logging.start_logging()

