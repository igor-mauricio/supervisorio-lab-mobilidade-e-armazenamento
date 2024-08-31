from dataclasses import dataclass
from infra.IHMController.IHMController import OpenPipeIHMController
from infra.Mediator import Mediator
@dataclass
class AlarmService:
    mediator: Mediator
    ihmController: OpenPipeIHMController

    def subscribeAlarms(self):
        def handle_alarm(tag_name, event_name):
            self.ihmController.subscribeToTag(
                tag_name, lambda value: self.mediator.notify(event_name, value))

        handle_alarm("Low temperature alarm", "low_temperature_alarm")
        handle_alarm("High temperature alarm", "high_temperature_alarm")
        handle_alarm("High internal-temperature alarm",
                    "high_internal_temperature_alarm")
        handle_alarm("Low Voltage alarm", "low_voltage_alarm")
        handle_alarm("Mid Voltage alarm", "mid_voltage_alarm")
        handle_alarm("High Voltage alarm", "high_voltage_alarm")
        handle_alarm("Low State-of-charge alarm", "low_state_of_charge_alarm")
        handle_alarm("Low Starter-voltage alarm", "low_starter_voltage_alarm")
        handle_alarm("High Starter-voltage alarm", "high_starter_voltage_alarm")
        handle_alarm("Low fused-voltage alarm", "low_fused_voltage_alarm")
        handle_alarm("High fused-voltage alarm", "high_fused_voltage_alarm")
        handle_alarm("Fuse blown alarm", "fuse_blown_alarm")