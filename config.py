from dotenv import load_dotenv
import os

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))
DATABASE_URL = ''
database_name = 'sduri.db'

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ChDaJiJuVu'
    SECURITY_PASSWORD_SALT = 'very_salty'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, database_name)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
        
    # mail settings
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # gmail authentication
    MAIL_USERNAME = "sduri.pro@gmail.com" # os.environ['APP_MAIL_USERNAME']
    MAIL_PASSWORD = "cits32**" # os.environ['APP_MAIL_PASSWORD']

    # mail accounts
    MAIL_DEFAULT_SENDER = 'from@example.com'
    
