# pull basic flask Functionality
import os
from flask import Flask
# Basic sql imports
from flask.ext.sqlalchemy import SQLAlchemy
# login management
from flask.ext.login import LoginManager
# openid support
# Depricated:from flask.ext.openid import OpenID
#
from config import basedir

app = Flask(__name__)
# used for everything in config file, i.e. db management
app.config.from_object('config')
db = SQLAlchemy(app)
# login
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
#Depricated:oid = OpenID(app, os.path.join(basedir, 'tmp'))

from app import views, models
