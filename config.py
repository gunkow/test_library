import os

basedir = os.path.abspath(os.path.dirname(__file__))

TEMPLATE_FOLDER = basedir + '/templates'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + basedir + '/library.db'

CSRF_ENABLED = True
SECRET_KEY = 'u-shall-not-pass'