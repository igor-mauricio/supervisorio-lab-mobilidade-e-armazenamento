from flask import Flask, request, flash, redirect, url_for, render_template
from models import User, PROFESSOR_PERMISSION
from AuthService import AuthService
from BatteryService import BatteryService
from flask_login import login_required, login_user, current_user


def AppController(app: Flask):
    @app.get("/")
    def welcome():
        return render_template("pages/welcome.html")



    @app.get("/minecraft")
    @login_required
    def minecraft():
        user:User = current_user
        return render_template("pages/minecraft.html", user=user.name)

    @app.get("/alarms")
    @login_required
    def alarms():
        user:User = current_user
        return render_template("pages/alarms.html", user=user.name)

    @app.get("/equipments")
    @login_required
    def equipments():
        user:User = current_user
        return "Equipments"

    @app.get("/equipments/battery/grafics")
    @login_required
    def grafics():
        user:User = current_user
        return "Grafics"

    @app.get("/equipments/generator")
    @login_required
    def generator():
        user:User = current_user
        return "Generator"

    @app.get("/equipments/inversor/fronius")
    @login_required
    def inversor_fronnius():
        user:User = current_user
        return render_template("pages/fronius.html", user=user.name)

    @app.get("/equipments/inversor/quattro")
    @login_required
    def inversor_quattro():
        user:User = current_user
        return render_template("pages/quattro.html", user=user.name)

    @app.get("/equipments/charge_controller/smart_solar")
    @login_required
    def charge_controller_smart_solar():
        user:User = current_user
        return "Charge Controller Smart Solar"

    @app.get("/equipments/energy_management_system/cerbo_gx")
    @login_required
    def charge_controller_cerbo_gx():
        user:User = current_user
        return "Energy Management System Cerbo GX"

    @app.get("/equipments/power_measurer")
    @login_required
    def power_measurement():
        user:User = current_user
        return "Power Measurer"
    
    @app.get("/lobby")
    @login_required
    def lobby():
        user:User = current_user
        return render_template("pages/index.html", user=user.name)


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
            return redirect(url_for("minecraft"))
        flash("Dados inválidos")
        return redirect(url_for("login"))

    @app.get("/auth/register")
    def register():
        return render_template("pages/register.html")

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
        authService.logout()
        flash("Usuário deslogado com sucesso")
        return redirect(url_for("login"))


def BatteryController(app: Flask, batteryService: BatteryService):
    @app.get("/equipments/battery")
    @login_required
    def battery():
        user:User = current_user
        try:
            battery = batteryService.get_battery()
        except Exception as e:
            error = str(e)
            if error == "No battery found":
                return "No battery found", 404
            return "Internal server error", 500

        return render_template("pages/battery.html", user=user.name, battery={
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
    @login_required
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
    @login_required
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
