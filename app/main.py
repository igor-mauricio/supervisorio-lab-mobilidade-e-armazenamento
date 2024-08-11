from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import login_user # type: ignore
from extensions import configureDatabase, configureLoginManager, db, login_manager
from models import User
app = Flask(__name__)
app.secret_key = "secret key"

configureDatabase(app)
configureLoginManager(app)

@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/login")
def login():
    return render_template("login.html")

@app.post("/login")
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
   

@app.get("/register")
def register():
    return render_template("register.html")

@app.post("/register")
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
    if len(password) < 8:
        flash("Senha deve ter no mínimo 8 caracteres")
        return redirect(url_for("register"))
    user = User(username, name, password)
    db.session.add(user)
    db.session.commit()
    flash("Usuário registrado com sucesso")
    return redirect(url_for("login"))

@app.get("/logout")
def logout():
    return "Logout"

@app.get("/alarms")
def alarms():
    return "Alarms"

@app.get("/equipments")
def equipments():
    return "Equipments"

@app.get("/equipments/battery")
def battery():
    return "Battery"

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