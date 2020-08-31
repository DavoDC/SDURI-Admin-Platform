# init.py
# essentially this makes the 'app' folder a package that can be imported

from config import Config
from flask import Flask
from flask_admin import Admin
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import fnmatch
import getpass
import logging
import os
from subprocess import call

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

with app.app_context():
    if db.engine.url.drivername == 'sqlite':
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

# Import routes and models
from app import routes, models

# Handle autmatic testing log generation
# - Log folder
logfolder = 'testing/logs'

# - Check if an empty log exists
emptylog = None
for fpath in os.scandir(logfolder):
    if (fpath.is_file()):
        if(os.path.getsize(fpath) == 0):
            emptylog = str(fpath)
            
# - New log path
newlog = None

# - If no empty log was found
if emptylog is None:
    # > Generate new log file name
    # >>> Get user name
    name = getpass.getuser()
    # >>> Get number of log files
    num = len(fnmatch.filter(os.listdir(logfolder), '*.log'))
    # >>> Use above to generate name of log file
    newlog = str(logfolder + '/test' + name + str(num) + '.log')
else:
    # > Else if an empty was found
    # >>> Refine empty log path
    emptylog = emptylog.replace("<DirEntry '", "")
    emptylog = emptylog.replace("'>", "")
    emptylog = emptylog.strip()
    # >>> Put new log into existing empty log
    newlog = logfolder + '/' + emptylog
    
# - Log into new log file path
logging.basicConfig(filename=newlog, level=logging.INFO)

