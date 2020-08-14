# init.py
# essentially this makes the 'app' folder a package that can be imported

from flask import Flask

from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
#
#app = Flask(__name__)
## app.config.from_object(Config)
#db = SQLAlchemy(app)
#migrate = Migrate(app, db)
#login = LoginManager(app)
#login.login_view = 'login'
#
#from app import routes, models

from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app

from app import models
