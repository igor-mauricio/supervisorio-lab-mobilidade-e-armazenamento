from extensions import db 
from flask_login import UserMixin # type: ignore


class User(db.Model, UserMixin): # type: ignore
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(100))
	name = db.Column(db.String(100))
	password = db.Column(db.String(100))
	
	def __init__(self, username: str, name: str, password: str):
		self.username = username
		self.name = name
		self.password = password



	