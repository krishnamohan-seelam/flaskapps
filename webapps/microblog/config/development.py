import os
basedir  = os.path.dirname(__file__)

DEBUG = True
SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, '..\\microblog.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'python'