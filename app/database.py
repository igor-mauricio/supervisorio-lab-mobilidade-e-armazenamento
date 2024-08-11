from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def configureDatabase(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
    app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False
    db.init_app(app)