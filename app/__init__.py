# init.py
# essentially this makes the 'app' folder a package that can be imported

from flask import Flask

from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from flask_admin import Admin
from flask_bootstrap import Bootstrap

app = Flask(__name__)
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

