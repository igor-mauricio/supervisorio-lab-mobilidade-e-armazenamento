from socket import SocketIO
from flask import Flask, request, flash, redirect, url_for, render_template
from infra import Mediator
from models import Alarm, AlarmLog, User, PROFESSOR_PERMISSION
from AuthService import AuthService
from BatteryService import BatteryService
from flask_login import login_required, login_user, current_user
from extensions import db

def AppController(app: Flask):
    
    @app.get("/")
    def welcome():
        return render_template("pages/welcome.html")

    @app.get("/minecraft")
    @login_required 
    def minecraft():
        return render_template("pages/minecraft.html", user=current_user.name, is_admin=current_user.permission_level == 3)

    @app.get("/alarms")
    @login_required
    def alarms():
        alarmLogsCalculated = []
        alarmLogs = AlarmLog.query.all()
        for alarmLog in alarmLogs:
            alarmLogsCalculated.append({
                "id": alarmLog.id,
                "message": Alarm.query.get(alarmLog.alarm_id).message,
                "description": Alarm.query.get(alarmLog.alarm_id).description,
                "confirmed": alarmLog.confirmed,
                "confirmed_by_user_id": User.query.get(alarmLog.confirmed_by_user_id).name if alarmLog.confirmed_by_user_id else None,
                "timestamp": alarmLog.timestamp.strftime("%H:%M:%S")
            })
        print(alarmLogsCalculated)
        return render_template("pages/alarms.html", alarmLogs=alarmLogsCalculated, user=current_user.name, is_admin=current_user.permission_level == 3)
    
    @app.get("/alarms/confirm/<int:alarm_id>")
    @login_required
    def confirm_alarm(alarm_id: int):
        alarm = AlarmLog.query.get(alarm_id)
        alarm.confirmed = True
        alarm.confirmed_by_user_id = current_user.id
        db.session.commit()
        return redirect(url_for("alarms"))

    @app.get("/equipments")
    @login_required
    def equipments():
        return "Equipments"

    @app.get("/equipments/battery/grafics")
    @login_required
    def grafics():
        return render_template("pages/grafics.html", user=current_user.name, is_admin=current_user.permission_level == 3)

    @app.get("/equipments/generator")
    @login_required
    def generator():
        return "Generator"

    @app.get("/equipments/inversor/fronius")
    @login_required
    def inversor_fronius():
        return render_template("pages/fronius.html", user=current_user.name, is_admin=current_user.permission_level == 3)

    @app.get("/equipments/conversor")
    @login_required
    def conversor():
        return render_template("pages/conversor.html", user=current_user.name, is_admin=current_user.permission_level == 3)
    
    @app.get("/equipments/controlador")
    @login_required
    def controlador():
        return render_template("pages/controlador.html", user=current_user.name, is_admin=current_user.permission_level == 3)

    @app.get("/equipments/inversor/quattro")
    @login_required
    def inversor_quattro():
        return render_template("pages/quattro.html", user=current_user.name, is_admin=current_user.permission_level == 3)

    @app.get("/equipments/charge_controller/smart_solar")
    @login_required
    def charge_controller_smart_solar():
        return "Charge Controller Smart Solar"

    @app.get("/equipments/energy_management_system/cerbo_gx")
    @login_required
    def charge_controller_cerbo_gx():
        return "Energy Management System Cerbo GX"

    @app.get("/equipments/power_measurer")
    @login_required
    def power_measurement():
        return "Power Measurer"
    
    @app.get("/lobby")
    @login_required
    def lobby():
        return render_template("pages/lobby.html", user=current_user.name, is_admin=current_user.permission_level == 3)


def AuthController(app: Flask, authService: AuthService):
    @app.get("/auth/login")
    def login():
        return render_template("pages/login.html")

    @app.post("/auth/login")
    def login_form():
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            flash("Login realizado com sucesso")
            return redirect(url_for("lobby"))
        flash("Dados inválidos")
        return redirect(url_for("login"))

    @app.get("/auth/register")
    @login_required
    def register():
        return render_template("pages/register.html")

    @app.post("/auth/register")
    @login_required
    def register_form():
        name = request.form["name"]
        username = request.form["username"]
        password = request.form["password"]
        password_confirm = request.form["password_confirm"]
        permission_level = int(request.form["permission_level"])
        try:
            authService.register(username, password, name, password_confirm, permission_level)
        except Exception as e:
            error = str(e)
            if error == "User already exists":
                flash("Usuário já existe")
                return redirect(url_for("register"))
            if error == "Password and confirmation do not match":
                flash("Senha e confirmação de senha não conferem")
                return redirect(url_for("register"))
            return "Internal server error", 500
        flash("Usuário registrado com sucesso")
        return redirect(url_for("lobby"))

    @app.get("/auth/logout")
    def logout():
        authService.logout()
        flash("Usuário deslogado com sucesso")
        return redirect(url_for("login"))


def BatteryController(app: Flask, batteryService: BatteryService, mediator: Mediator, socketio: SocketIO):
    mediator.subscribe("battery_charged", lambda charged_percent: socketio.emit('battery_update', {'charged_percent': charged_percent}))
    mediator.subscribe("battery_log_created", lambda battery_log: socketio.emit('battery_log_created', {
        "current": battery_log.current,
        "voltage": battery_log.voltage,
        "power": battery_log.power,
        "temperature": battery_log.temperature,
        "timestamp": battery_log.timestamp.strftime("%H:%M:%S"),
        "average_charge": battery_log.average_charge,
        "average_discharge": battery_log.average_discharge,
        "energy": battery_log.energy,
        "consumo": battery_log.consumo
    }))

    mediator.subscribe("fronius_log_created", lambda battery_log: socketio.emit('fronius_log_created', {
        "tensaoL1": battery_log.tensaoL1,
        "tensaoL2": battery_log.tensaoL2,
        "tensaoL3": battery_log.tensaoL3,
        "timestamp": battery_log.timestamp.strftime("%H:%M:%S"),
        "correnteL1": battery_log.correnteL1,
        "correnteL2": battery_log.correnteL2,
        "correnteL3": battery_log.correnteL3,
        "potenciaL1": battery_log.potenciaL1,
        "potenciaL2": battery_log.potenciaL2,
        "potenciaL3": battery_log.potenciaL3,
        "potenciaMaxima": battery_log.potenciaMaxima,
        "capacidadeMaximaPotencia": battery_log.capacidadeMaximaPotencia,
        "limitedePotencia": battery_log.limitedePotencia,
        "frequency": battery_log.frequency
    }))

    mediator.subscribe("controller_log_created", lambda state: socketio.emit('controller_log_created', {
        'timestamp': state.timestamp.strftime("%H:%M:%S"),
        'chargerOnOff': state.chargerOnOff,
        'chargerState': state.chargerState,
        'MPPOperationMode': state.MPPOperationMode,
        'PVVoltage': state.PVVoltage,
        'PVCurrent': state.PVCurrent,
        'PVPower': state.PVPower,
        'UserYield': state.UserYield,
        'yieldToday': state.yieldToday,
        'maximumChargePowerToday': state.maximumChargePowerToday
    }))






    @app.get("/equipments/battery")
    @login_required
    def battery():
        try:
            battery = batteryService.get_battery()
        except Exception as e:
            error = str(e)
            if error == "No battery found":
                return "No battery found", 404
            return "Internal server error", 500

        return render_template("pages/battery.html", user=current_user.name, is_admin=current_user.permission_level == 3, battery={
            "capacity": battery.capacity,
            "charged_percent": battery.charged_percent,
            "health_percent": battery.health_percent,
            "manufacturer": battery.manufacturer,
            "model": battery.model,
            "min_out_voltage": battery.min_out_voltage,
            "max_in_voltage": battery.max_in_voltage,
            "state": battery.state,
            "relay_status": battery.relay_status
        })
    
    # @socketio.on('toggle_battery_mode')
    # def toggle_battery_mode():
    #     print("asodjasiodjio")
    #     if not current_user.is_authenticated or current_user.permission_level < PROFESSOR_PERMISSION:
    #         return "Permission denied", 403
    #     # mode = request.form["mode"]
    #     try:
    #         batteryService.toggle_battery_mode()
    #     except Exception as e:
    #         error = str(e)
    #         print(e)
    #         print("asiduasidou")
    #         if error == "Invalid mode":
    #             return "Invalid mode", 400
    #         elif error == "No battery found":
    #             return "No battery found", 404
    #         return "Internal server error", 500
    #     return "ok", 200

    # @socketio.on('toggle_relay_state')
    # def toggle_relay_state():
    #     if not current_user.is_authenticated or current_user.permission_level < PROFESSOR_PERMISSION:
    #         return "Permission denied", 403
    #     try:
    #         batteryService.toggle_battery_relay_state()
    #     except Exception as e:
    #         error = str(e)
    #         print(e)
    #         if error == "Invalid state":
    #             return "Invalid state", 400
    #         if error == "No battery found":
    #             return "No battery found", 404
    #         return "Internal server error", 500
    #     return "ok", 200
        
    @app.post("/equipments/battery/change_relay_state")
    @login_required
    def toggle_battery_relay_state():
        if not current_user.is_authenticated or current_user.permission_level < PROFESSOR_PERMISSION:
            return "Permission denied", 403
        try:

            relay_state = batteryService.toggle_battery_relay_state()
            return {'relay_status': relay_state}, 200
        except Exception as e:
            error = str(e)
            print(e)
            if error == "Invalid state":
                return "Invalid state", 400
            if error == "No battery found":
                return "No battery found", 404
            return "Internal server error", 500

    @app.post("/equipments/battery/change_battery_mode")
    @login_required
    def toggle_battery_mode():
        print("asodjasiodjio")
        if not current_user.is_authenticated or current_user.permission_level < PROFESSOR_PERMISSION:
            return "Permission denied", 403
        # mode = request.form["mode"]
        try:
            mode = batteryService.toggle_battery_mode()
            return {'state': mode}, 200
        except Exception as e:
            error = str(e)
            print(e)
            print("asiduasidou")
            if error == "Invalid mode":
                return "Invalid mode", 400
            elif error == "No battery found":
                return "No battery found", 404
            return "Internal server error", 500