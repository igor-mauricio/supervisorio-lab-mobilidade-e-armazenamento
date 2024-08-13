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



class Battery(db.Model): # type: ignore
	id = db.Column(db.Integer, primary_key=True)
	model = db.Column(db.String(100))
	manufacturer = db.Column(db.String(100))
	state = db.Column(db.String(100))
	health_percent = db.Column(db.String(100))
	mode = db.Column(db.String(100))
	relay_status = db.Column(db.String(100))
	capacity = db.Column(db.Float)
	min_out_voltage = db.Column(db.Float)
	max_in_voltage = db.Column(db.Float)
	charged_percent = db.Column(db.Float)
	

class BatteryLog(db.Model): # type: ignore
	id = db.Column(db.Integer, primary_key=True)
	battery_id = db.Column(db.Integer, db.ForeignKey('battery.id'))
	current = db.Column(db.Float)
	voltage = db.Column(db.Float)
	power = db.Column(db.Float)
	temperature = db.Column(db.Float)
	timestamp = db.Column(db.DateTime)


class Alarm(db.Model): # type: ignore
	id = db.Column(db.Integer, primary_key=True)
	confirmable_by_operator = db.Column(db.Boolean, default=True)
	message = db.Column(db.String(100))
	description = db.Column(db.Text)
	level = db.Column(db.Integer)

class AlarmLog(db.Model): # type: ignore
	id = db.Column(db.Integer, primary_key=True)
	alarm_id = db.Column(db.Integer, db.ForeignKey('alarms.id'))
	confirmed = db.Column(db.Boolean, default=False)
	confirmed_by_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	timestamp = db.Column(db.DateTime)

class UserEvent(db.Model): # type: ignore
	id = db.Column(db.Integer, primary_key=True)
	event = db.Column(db.String(100))

class UserEventLog(db.Model): # type: ignore
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
	timestamp = db.Column(db.DateTime)