from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager # type: ignore

db = SQLAlchemy()
login_manager = LoginManager()

def configureDatabase(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
    app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
    db.init_app(app)

def configureLoginManager(app: Flask):
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = 'You need to be logged in to access this page'
    login_manager.login_message_category = 'info'
