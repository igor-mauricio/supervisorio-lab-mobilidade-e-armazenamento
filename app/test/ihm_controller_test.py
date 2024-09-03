from app.infra.IHMController.IHMController import OpenPipeIHMController


def test_shouldModifyVariableInIHMController():
    ihm_controller = OpenPipeIHMController()
    ihm_controller.writeTag("test_bool_tag", "1")
    ihm_controller.writeTag("test_int_tag", "42")
