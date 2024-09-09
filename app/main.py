from flask import Flask
from flask_socketio import SocketIO  # type: ignore
from AuthService import AuthService
from AlarmService import AlarmService
from BatteryService import BatteryService
from infra.IHMController.IHMController import FakeIHMController
from infra.SetupDatabase import setup_database
from infra.Mediator import Mediator
from extensions import configureDatabase, configureLoginManager, db, login_manager
from controllers import AppController, AuthController, BatteryController
from models import User

app = Flask(__name__)
app.secret_key = "secret key"
socketio = SocketIO(app, cors_allowed_origins="*",)
configureDatabase(app)

configureLoginManager(app)
@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()

ihmController = FakeIHMController()
mediator = Mediator()
batteryService = BatteryService(mediator)
authService = AuthService(mediator)
alarmService = AlarmService(mediator, ihmController)

AppController(app)
AuthController(app, authService)
BatteryController(app, batteryService)

alarmService.subscribeAlarms()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        setup_database()
        authService.registerDefaultUsers()
        socketio.run(app, debug=True, port=3000,
                     host='0.0.0.0', allow_unsafe_werkzeug=True)