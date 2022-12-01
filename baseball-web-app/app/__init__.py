from flask import Flask
from flask_session import Session
from config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
Session(app)
# for key in app.config:
#   print(key, ' : ', app.config[key])

from app import routes, forms, orm