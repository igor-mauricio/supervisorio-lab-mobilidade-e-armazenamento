from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user  # type: ignore
from app.battery_service import BatteryService
from app.infra.Mediator import Mediator
from extensions import configureDatabase, configureLoginManager, db, login_manager
from models import PROFESSOR_PERMISSION, Battery, User
app = Flask(__name__)
app.secret_key = "secret key"

configureDatabase(app)
configureLoginManager(app)

mediator = Mediator()
batteryService = BatteryService(mediator)

@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()

@app.get("/")
def index():
    return render_template("index.html")

@app.get("auth/login")
def login():
    return render_template("login.html")

@app.post("auth/login")
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
   

@app.get("auth/register")
def register():
    return render_template("register.html")

@app.post("auth/register")
def register_form():
    name = request.form["name"]
    username = request.form["username"]
    password = request.form["password"]
    password_confirm = request.form["password_confirm"]
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        flash("Nome de usuário já existe")
        return redirect(url_for("register"))
    if password != password_confirm:
        flash("Senha e confirmação de senha não conferem")
        return redirect(url_for("register"))
    if len(password) < 5:
        flash("Senha deve ter no mínimo 5 caracteres")
        return redirect(url_for("register"))
    if len(name) == 0:
        flash("Nome não pode ser vazio")
        return redirect(url_for("register"))
    
    user = User(username, name, password)
    db.session.add(user)
    db.session.commit()
    flash("Usuário registrado com sucesso")
    return redirect(url_for("login"))

@app.get("auth/logout")
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
    battery: Battery = Battery.query.all()[0] # type: ignore
    if battery is None:
        return "No battery found", 404
    
    return render_template("battery.html", battery = {
        "capacity": battery.capacity,
        "charged_percent": battery.charged_percent,
        "health_percent": battery.health_percent,
        "manufacturer": battery.manufacturer,
        "model": battery.model,
        "min_out_voltage": battery.min_out_voltage,
        "max_out_voltage": battery.max_out_voltage,
        "state": battery.state,
        "relay_status": battery.relay_status
    })

@login_required
@app.post("/equipments/battery/change_relay_state")
def change_battery_relay_state():
    if current_user.permission_level < PROFESSOR_PERMISSION:
        return "Permission denied", 403
    state = request.form["relay_state"]
    try:
        batteryService.change_battery_relay_state(state)
    except Exception as e:
        if str(e) == "Invalid state":
            return "Invalid state", 400
        if str(e) == "No battery found":
            return "No battery found", 404
    return "State changed", 200

@login_required
@app.post("/equipments/battery/change_battery_mode")
def change_battery_mode():
    if current_user.permission_level < PROFESSOR_PERMISSION:
        return "Permission denied", 403
    mode = request.form["mode"]
    try:
        batteryService.change_battery_mode(mode)
    except Exception as e:
        if str(e) == "Invalid mode":
            return "Invalid mode", 400
        if str(e) == "No battery found":
            return "No battery found", 404
    return "Mode changed", 200
    
@app.get("/equipments/generator")
def generator():
    return "Generator"

@app.get("/equipments/inversor/fronius")
def inversor_fronnius():
    return "Fronius"

@app.get("/equipments/inversor/quattro")
def inversor_quattro():
    return "Quattro"

@app.get("/equipments/charge_controller/smart_solar")
def charge_controller_smart_solar():
    return "Charge Controller Smart Solar"

@app.get("/equipments/energy_management_system/cerbo_gx")
def charge_controller_cerbo_gx():
    return "Energy Management System Cerbo GX"

@app.get("/equipments/power_measurer")
def power_measurement():
    return "Power Measurer"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=33000, host='0.0.0.0')