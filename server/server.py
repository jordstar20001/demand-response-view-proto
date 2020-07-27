from flask import Flask, request, session, redirect, send_from_directory

import json
from demandresponse import UserManager, PermissionManager
        
app = Flask(__name__, static_url_path="/static")

config = json.loads(open("data/cfg.json", "r").read())

app.config["SECRET_KEY"] = config["SECRET_KEY"]

USERMANAGER = UserManager(config["USERS_JSON_FN"])
PERMSMANAGER = PermissionManager(config["AUTH_JSON_FN"])
ACC_INDEX_PAGES = config["ACCTYPE_INDEXPAGES"]

del config

def Authed(auth_str, acc_type = None):
    if not PERMSMANAGER.is_anonymous_action(auth_str) and acc_type != None:
        if "USER" not in session: return False
        session_user = session["USER"]
        if session_user == None or not PERMSMANAGER.user_permitted(session_user, auth_str) or (session_user["acc_type"] != acc_type and acc_type != None):
            return False

    return True

@app.route("/")
def home():
    if "USER" in session: return redirect("/dashboard")
    return app.send_static_file("index.html")

@app.route("/login", methods=["POST"])
def login():
    loginData = request.form
    u, p = loginData["txtUsername"], loginData["txtPassword"]

    if USERMANAGER.valid_user(u, p):
        session["USER"] = USERMANAGER.get_user_by_username(u)
        return "Success!", 200
    
    else:
        return "Incorrect username or password", 403

@app.route("/logout", methods=["GET"])
def logout():
    if "USER" in session: del session["USER"]
    return redirect("/")

    

@app.route("/dashboard", defaults={'file': None})
@app.route("/dashboard/<path:file>", methods=["GET"])
def dashboard(file):
    if not Authed("/dashboard"): return redirect("/")
    if file == None:
        user = session["USER"]
        if user["acc_type"] not in ACC_INDEX_PAGES:
            return f"Index webpage not found for account type {user['acc_type']}", 404

        return send_from_directory("static/dashboard", ACC_INDEX_PAGES[user["acc_type"]])
    return send_from_directory("static/dashboard", file)


@app.route("/dashboard/api/<endpoint>", methods=["GET", "POST"])
def dashboard_api(endpoint):
    if Authed(endpoint): return 200
    return "", 200    

@app.route("/public/<path:path>", methods=["GET"])
def public(path):
    print(f"Path: {path}")
    return send_from_directory("static/public", path)

# Run the server
if __name__ == "__main__":
    app.run("0.0.0.0", 8080)