from flask import Flask, g
import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__, template_folder=config.TEMPLATE_FOLDER)
app.config.from_object('config')

engine = create_engine(config.SQLALCHEMY_DATABASE_URI, echo=True)

from app import views, models  # experim: remove "from app"
