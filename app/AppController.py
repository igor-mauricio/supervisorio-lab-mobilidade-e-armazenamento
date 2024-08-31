from flask import Flask, request, flash, redirect, url_for, render_template
from models import User, PROFESSOR_PERMISSION
from AuthService import AuthService
from BatteryService import BatteryService
from flask_login import login_user, current_user

def AppController(app: Flask, authService: AuthService, batteryService: BatteryService):
    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/minecraft")
    def minecraft():
        return render_template("minecraft.html")

    @app.get("/auth/login")
    def login():
        return render_template("login.html")

    @app.post("/auth/login")
    def login_form(): 
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            flash("Login realizado com sucesso")
            return redirect(url_for("index"))
        flash("Dados inválidos")
        return redirect(url_for("login"))
    

    @app.get("/auth/register")
    def register():
        return render_template("register.html")

    @app.post("/auth/register")
    def register_form():
        name = request.form["name"]
        username = request.form["username"]
        password = request.form["password"]
        password_confirm = request.form["password_confirm"]
        try:
            authService.register(username, password, name, password_confirm)
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
        return redirect(url_for("login"))

    @app.get("/auth/logout")
    def logout():
        return "Logout"

    @app.get("/alarms")
    def alarms():
        return render_template("alarms.html")

    @app.get("/equipments")
    def equipments():
        return "Equipments"

    @app.get("/equipments/battery")
    def battery():
        try:
            battery = batteryService.get_battery()
        except Exception as e:
            error = str(e)
            if error == "No battery found":
                return "No battery found", 404
            return "Internal server error", 500
        
        return render_template("battery.html", battery = {
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

    @app.post("/equipments/battery/change_relay_state")
    def change_battery_relay_state():
        if not current_user.is_authenticated or current_user.permission_level < PROFESSOR_PERMISSION:
            return "Permission denied", 403
        state = request.form["relay_state"]
        try:
            batteryService.change_battery_relay_state(state)
        except Exception as e:
            error = str(e)
            if error == "Invalid state":
                return "Invalid state", 400
            if error == "No battery found":
                return "No battery found", 404
            return "Internal server error", 500
        return "State changed", 200

    @app.post("/equipments/battery/change_battery_mode")
    def change_battery_mode():
        if not current_user.is_authenticated or current_user.permission_level < PROFESSOR_PERMISSION:
            return "Permission denied", 403
        mode = request.form["mode"]
        try:
            batteryService.change_battery_mode(mode)
        except Exception as e:
            error = str(e)
            if error == "Invalid mode":
                return "Invalid mode", 400
            elif error == "No battery found":
                return "No battery found", 404
            return "Internal server error", 500
        return "Mode changed", 200

    @app.get("/equipments/battery/grafics")
    def grafics():
        return "Grafics"

    @app.get("/equipments/generator")
    def generator():
        return "Generator"

    @app.get("/equipments/inversor/fronius")
    def inversor_fronnius():
        return "Fronius"

    @app.get("/equipments/inversor/quattro")
    def inversor_quattro():
        return render_template("quattro.html")

    @app.get("/equipments/charge_controller/smart_solar")
    def charge_controller_smart_solar():
        return "Charge Controller Smart Solar"

    @app.get("/equipments/energy_management_system/cerbo_gx")
    def charge_controller_cerbo_gx():
        return "Energy Management System Cerbo GX"

    @app.get("/equipments/power_measurer")
    def power_measurement():
        return "Power Measurer"