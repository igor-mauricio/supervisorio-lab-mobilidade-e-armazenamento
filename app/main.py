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
from models import Alarm, AlarmLog, Battery, BatteryLog, ControllerLog, Fronius, FroniusLog, User
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
                fronius:Fronius = Fronius.query.first()
                batteryHighVoltageAlarm:Alarm = Alarm.query.first()
                while True:
                    # Generate a random battery charged percent
                    battery.charged_percent = float(f"{(math.sin(time.time()/10) + 1) * 50:.1f}")
                    current = 100 * math.sin(time.time()/5) + 100 + random.uniform(0, 10)
                    voltage = 100 * math.sin(time.time()/5) + 100 + random.uniform(0, 10)
                    power = current * voltage
                    harmonics_voltage = [100 * math.sin(time.time()/(5*h)) + 100 + random.uniform(0, 10) for h in [1,3,5]]
                    harmonics_current = [100 * math.sin(time.time()/(5*h)) + 100 + random.uniform(0, 10) for h in [2, 4]]

                    if(voltage > 56.5):
                        alarmLog = AlarmLog(
                            alarm_id = batteryHighVoltageAlarm.id,
                            timestamp = datetime.now(),
                        )
                        db.session.add(alarmLog)
                        db.session.commit()
                        mediator.notify("alarm_created", alarmLog)

                    battery_log = BatteryLog(
                        battery_id=battery.id,
                        current=sum(harmonics_current),
                        voltage=sum(harmonics_voltage),
                        power=sum(harmonics_current) * sum(harmonics_voltage),
                        temperature=200 * math.sin(time.time()) + random.uniform(-10, 10),
                        timestamp=datetime.now(),
                        average_charge= 100 * math.sin(time.time()) + 100 + random.uniform(0, 10),
                        average_discharge = 100 * math.sin(time.time()) + 100 + random.uniform(0, 10),
                        energy = 100 * math.sin(time.time() * 2) + 120 + random.uniform(0, 5),
                        consumo = 100 * math.sin(time.time() * 4) + 150 + random.uniform(0, 20),
                    )

                    tensaoL1 = 100 * math.sin(time.time()/(5*1)) + 100 + random.uniform(0, 10)
                    tensaoL2 = 100 * math.sin(time.time()/(5*3)) + 100 + random.uniform(0, 10)
                    tensaoL3 = 100 * math.sin(time.time()/(5*5)) + 100 + random.uniform(0, 10)
                    correnteL1 = 100 * math.sin(time.time()/(5*2)) + 100 + random.uniform(0, 10)
                    correnteL2 = 100 * math.sin(time.time()/(5*4)) + 100 + random.uniform(0, 10)
                    correnteL3 = 100 * math.sin(time.time()/(5*6)) + 100 + random.uniform(0, 10)
                    potenciaL1 = tensaoL1 * correnteL1
                    potenciaL2 = tensaoL2 * correnteL2
                    potenciaL3 = tensaoL3 * correnteL3

                    fronius_log = FroniusLog(
                        fronius_id=fronius.id,
                        timestamp=datetime.now(),
                        tensaoL1 = tensaoL1,
                        tensaoL2 = tensaoL2,
                        tensaoL3 = tensaoL3,
                        correnteL1 = correnteL1,
                        correnteL2 = correnteL2,
                        correnteL3 = correnteL3,
                        potenciaL1 = potenciaL1,
                        potenciaL2 = potenciaL2,
                        potenciaL3 = potenciaL3,
                        potenciaMaxima = 1000,
                        capacidadeMaximaPotencia = 2000,
                        limitedePotencia = 3000,
                        frequency = 60 + random.uniform(-1, 1)
                    )

                    PVVoltage = 100 * math.sin(time.time()/(5*1)) + 100 + random.uniform(0, 10)
                    PVCurrent = 100 * math.sin(time.time()/(5*2)) + 100 + random.uniform(0, 10)

                    controller_log = ControllerLog(
                        timestamp = datetime.now(),
                        chargerOnOff = True,
                        chargerState = "CHARGING",
                        MPPOperationMode = "MPPT",
                        PVVoltage = PVVoltage,
                        PVCurrent = PVCurrent,
                        PVPower = PVVoltage * PVCurrent,
                        UserYield =  100 * math.sin(time.time()/(5*1)) + 100 + random.uniform(0, 10),
                        yieldToday = 150 + random.uniform(0, 10),
                        maximumChargePowerToday =  120 + random.uniform(0, 10)
                    )



                    db.session.add(battery_log)
                    db.session.add(fronius_log)
                    db.session.add(controller_log)
                    mediator.notify("battery_log_created", battery_log)
                    mediator.notify("fronius_log_created", fronius_log)
                    mediator.notify("controller_log_created", controller_log)
                    db.session.commit()
                    mediator.notify("battery_charged", battery.charged_percent)



                    
                    time.sleep(0.2)  # Sleep for 5 seconds before updating again

        # Create and start the service in a separate thread
        battery_thread = threading.Thread(target=change_battery_percent)
        battery_thread.start()
        authService.registerDefaultUsers()
        socketio.run(app, debug=True, port=3000,
                     host='0.0.0.0', allow_unsafe_werkzeug=True)