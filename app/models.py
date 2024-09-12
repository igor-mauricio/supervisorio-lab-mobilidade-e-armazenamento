from extensions import db 
from flask_login import UserMixin # type: ignore

STUDENT_PERMISSION = 0
PROFESSOR_PERMISSION = 1
TECHNICIAN_PERMISSION = 2
ADMIN_PERMISSION = 3

class User(db.Model, UserMixin): # type: ignore
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(100))
	name = db.Column(db.String(100))
	password = db.Column(db.String(100))
	permission_level = db.Column(db.Integer, default=0)
	'''
	0 - Estudante
	1 - Professor
	2 - Técnico
	3 - Administrador
	'''
	
	def __init__(self, username: str, name: str, password: str, permission_level: int = 0):
		self.username = username
		self.name = name
		self.password = password
		self.permission_level = permission_level



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
	average_charge = db.Column(db.Float)
	average_discharge = db.Column(db.Float)
	energy = db.Column(db.Float)
	consumo = db.Column(db.Float)


class Fronius(db.Model): # type: ignore
	id = db.Column(db.Integer, primary_key=True)
	limitedePotencia = db.Column(db.Float)

class FroniusLog(db.Model): # type: ignore
	id = db.Column(db.Integer, primary_key=True)
	fronius_id = db.Column(db.Integer, db.ForeignKey('fronius.id'))
	timestamp = db.Column(db.DateTime)
	tensaoL1 = db.Column(db.Float)
	tensaoL2 = db.Column(db.Float)
	tensaoL3 = db.Column(db.Float)
	correnteL1 = db.Column(db.Float)
	correnteL2 = db.Column(db.Float)
	correnteL3 = db.Column(db.Float)
	potenciaL1 = db.Column(db.Float)
	potenciaL2 = db.Column(db.Float)
	potenciaL3 = db.Column(db.Float)
	frequency = db.Column(db.Float)
	potenciaMaxima = db.Column(db.Float)
	capacidadeMaximaPotencia = db.Column(db.Float)
	limitedePotencia = db.Column(db.Float)

class Alarm(db.Model): # type: ignore
	id = db.Column(db.Integer, primary_key=True)
	confirmable_by_operator = db.Column(db.Boolean, default=True)
	message = db.Column(db.String(100))
	description = db.Column(db.Text)
	level = db.Column(db.Integer)

class AlarmLog(db.Model): # type: ignore
	id = db.Column(db.Integer, primary_key=True)
	alarm_id = db.Column(db.Integer, db.ForeignKey('alarm.id'))
	confirmed = db.Column(db.Boolean, default=False)
	confirmed_by_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	timestamp = db.Column(db.DateTime)

class ControllerLog(db.Model): # type: ignore
	id = db.Column(db.Integer, primary_key=True)
	timestamp = db.Column(db.DateTime)
	chargerOnOff = db.Column(db.Boolean)
	chargerState = db.Column(db.String(100))
	MPPOperationMode = db.Column(db.String(100))
	PVVoltage = db.Column(db.Float)
	PVCurrent = db.Column(db.Float)
	PVPower = db.Column(db.Float)
	UserYield = db.Column(db.Float)
	yieldToday = db.Column(db.Float)
	maximumChargePowerToday = db.Column(db.Float)

class UserEvent(db.Model): # type: ignore
	id = db.Column(db.Integer, primary_key=True)
	event = db.Column(db.String(100))

class UserEventLog(db.Model): # type: ignore
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	event_id = db.Column(db.Integer, db.ForeignKey('user_event.id'))
	timestamp = db.Column(db.DateTime)