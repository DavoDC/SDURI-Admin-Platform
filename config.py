from dotenv import load_dotenv
import os

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))
DATABASE_URL = ''
database_name = 'sduri.db'

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ChDaJiJuVu'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, database_name)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
