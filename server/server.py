from flask import Flask, request, session, redirect, send_from_directory

import json
from demandresponse import UserManager, PermissionManager
        
app = Flask(__name__, static_url_path="/static")

config = json.loads(open("data/cfg.json", "r").read())

app.config["SECRET_KEY"] = config["SECRET_KEY"]

USERMANAGER = UserManager(config["USERS_JSON_FN"])
PERMSMANAGER = PermissionManager(config["AUTH_JSON_FN"])

del config

def Authed(auth_str):
    if not PERMSMANAGER.is_anonymous_action(auth_str):
        if "USER" not in session: return False
        session_user = session["USER"]
        if session_user == None or not PERMSMANAGER.user_permitted(session_user, auth_str):
            return False

    return True

@app.route("/")
def home():
    if "USER" in session: return redirect("/dashboard")
    return app.send_static_file("index.html")

@app.route("/login", methods=["POST"])
def login():
    loginData = request.form
    u,p = loginData["txtUsername"], loginData["txtPassword"]
    print(f"User: {u} | Pass: {p}")

    if USERMANAGER.valid_user(u, p):
        session["USER"] = USERMANAGER.get_user_by_username(u)
        return "Success!", 200
    
    else:
        return "Incorrect username or password", 403

@app.route("/logout", methods=["GET"])
def logout():
    if "USER" in session: del session["USER"]
    return redirect("/")

    

@app.route("/dashboard", defaults={'file': "index.html"})
@app.route("/dashboard/<path:file>", methods=["GET"])
def dashboard(file):
    if not Authed("/dashboard"): return redirect("/")
    return send_from_directory("static/dashboard", file)


@app.route("/dashboard/api/<endpoint>", methods=["GET"])
def dashboard_api(endpoint):
    print(f"SUCCESS: {endpoint}")
    return "", 200    

@app.route("/public/<path:path>", methods=["GET"])
def public(path):
    print(f"Path: {path}")
    return send_from_directory("static/public", path)

# Run the server
app.run("0.0.0.0", 8080)