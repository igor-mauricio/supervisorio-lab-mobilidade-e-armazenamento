from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = "secret key"

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/login")
def login():
    return "Login"

@app.route("/register")
def register():
    return "Register"

@app.route("/logout")
def logout():
    return "Logout"

@app.route("/alarms")
def alarms():
    return "Alarms"

@app.route("/equipments")
def equipments():
    return "Equipments"

@app.route("/equipments/battery")
def battery():
    return "Battery"

@app.route("/equipments/generator")
def generator():
    return "Generator"

@app.route("/equipments/inversor/fronius")
def inversor_fronnius():
    return "Fronius"

@app.route("/equipments/inversor/quattro")
def inversor_quattro():
    return "Quattro"

@app.route("/equipments/charge_controller/smart_solar")
def charge_controller_smart_solar():
    return "Charge Controller Smart Solar"

@app.route("/equipments/energy_management_system/cerbo_gx")
def charge_controller_cerbo_gx():
    return "Energy Management System Cerbo GX"

@app.route("/equipments/power_measurer")
def power_measurement():
    return "Power Measurer"

if __name__ == "__main__":
    app.run(debug=True, port=33000, host='0.0.0.0')