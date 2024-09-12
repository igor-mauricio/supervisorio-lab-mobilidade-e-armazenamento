from datetime import datetime
import math
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
from models import Battery, BatteryLog, User
import threading
import time
import random
import math

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
BatteryController(app, batteryService, mediator, socketio)

alarmService.subscribeAlarms()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        setup_database()
        def change_battery_percent():
            with app.app_context():
                battery:Battery = batteryService.get_battery()
                while True:
                    # Generate a random battery charged percent
                    battery.charged_percent = float(f"{(math.sin(time.time()/10) + 1) * 50:.1f}")
                    current = 100 * math.sin(time.time()/5) + 100 + random.uniform(0, 10)
                    voltage = 100 * math.sin(time.time()/5) + 100 + random.uniform(0, 10)
                    power = current * voltage
                    harmonics_voltage = [100 * math.sin(time.time()/(5*h)) + 100 + random.uniform(0, 10) for h in [1,3,5]]
                    harmonics_current = [100 * math.sin(time.time()/(5*h)) + 100 + random.uniform(0, 10) for h in [2, 4]]

                    battery_log = BatteryLog(
                        battery_id=battery.id,
                        current=sum(harmonics_current),
                        voltage=sum(harmonics_voltage),
                        power=sum(harmonics_current) * sum(harmonics_voltage),
                        temperature=200 * math.sin(time.time()) + random.uniform(-10, 10),
                        timestamp=datetime.now()
                    )
                    db.session.add(battery_log)
                    mediator.notify("battery_log_created", battery_log)
                    db.session.commit()
                    mediator.notify("battery_charged", battery.charged_percent)



                    
                    time.sleep(0.2)  # Sleep for 5 seconds before updating again

        # Create and start the service in a separate thread
        battery_thread = threading.Thread(target=change_battery_percent)
        battery_thread.start()
        authService.registerDefaultUsers()
        socketio.run(app, debug=True, port=3000,
                     host='0.0.0.0', allow_unsafe_werkzeug=True)