from models import Alarm, Battery, Fronius
from extensions import db

def setup_database():
    batteries = Battery.query.all()
    if len(batteries) == 0:
        battery1 = Battery(model="B-box Pro 3.8", manufacturer="BYD", state="SHUTDOWN", health_percent="100%", mode="STANDBY", relay_status="CLOSED", capacity=270, min_out_voltage=43, max_in_voltage=56.5, charged_percent=0)
        fronius1 = Fronius(limitedePotencia=100)
        batteryHighVoltageAlarm = Alarm(message="High Voltage", description="The battery voltage is too high", level="HIGH", confirmable_by_operator=True)
        db.session.add(batteryHighVoltageAlarm)
        db.session.add(battery1)
        db.session.add(fronius1)
        db.session.commit()
