from models import Battery
from extensions import db

def setup_database():
    batteries = Battery.query.all()
    if len(batteries) == 0:
        battery1 = Battery(model="B-box Pro 3.8", manufacturer="BYD", state="SHUTDOWN", health_percent="100%", mode="STANDBY", relay_status="CLOSED", capacity=270, min_out_voltage=43, max_in_voltage=56.5, charged_percent=0)
        db.session.add(battery1)
        db.session.commit()
