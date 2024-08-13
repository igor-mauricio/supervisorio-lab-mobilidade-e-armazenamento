
from dataclasses import dataclass
from models import Battery
from app.infra.Mediator import Mediator
from extensions import db

@dataclass
class BatteryService:
  mediator: Mediator
  
  def change_battery_relay_state(self, state: str) -> None:
      if state not in ["OPEN", "CLOSED"]:
          raise Exception("Invalid state")
      battery: Battery = Battery.query.all()[0] # type: ignore
      if battery is None:
          raise Exception("No battery found")
      battery.state = state
      db.session.commit()
      self.mediator.notify("battery_relay_state_changed", state)

  def change_battery_mode(self, mode: str):
      if mode not in ["OPEN", "STANDBY"]:
          raise Exception("Invalid mode")
      battery: Battery = Battery.query.all()[0] # type: ignore
      if battery is None:
         raise Exception("No battery found")
      battery.mode = mode
      db.session.commit()
      self.mediator.notify("battery_mode_changed", mode)