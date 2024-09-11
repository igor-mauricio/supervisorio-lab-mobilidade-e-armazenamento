
from dataclasses import dataclass
from models import Battery
from infra.Mediator import Mediator
from extensions import db

@dataclass
class BatteryService:
    mediator: Mediator

    def get_battery(self) -> Battery:
        battery: Battery = Battery.query.all()[0]
        if battery is None:
            raise Exception("No battery found")
        return battery
  
    def toggle_battery_relay_state(self, state: str ="") -> None:
        # if state not in ["OPEN", "CLOSED"]:
        #     raise Exception("Invalid state")

        battery: Battery = Battery.query.all()[0] # type: ignore
        if battery is None:
            raise Exception("No battery found")
        if battery.relay_status == "OPEN":
            battery.relay_status = "CLOSED"
        else:
            battery.relay_status = "OPEN"
        db.session.commit()
        self.mediator.notify("battery_relay_status_changed", battery.relay_status)

    def toggle_battery_mode(self, mode: str=""):
        # if mode not in ["OPEN", "STANDBY", "SHUTDOWN"]:
        #     raise Exception("Invalid mode")
        battery: Battery = Battery.query.all()[0] # type: ignore
        if battery is None:
            raise Exception("No battery found")
        if battery.state == "OPEN" or battery.state == "STANDBY":
            battery.state = "SHUTDOWN"
        else:
            battery.state = "STANDBY"
        db.session.commit()
        self.mediator.notify("battery_state_changed", battery.state)