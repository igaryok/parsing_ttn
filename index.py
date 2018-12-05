from flask import Flask, render_template, request, redirect, url_for
from funcs import check_auth, get_ttn_fromdb, parsing, get_settings, save_to_file

app = Flask(__name__)
authorized = False


@app.route("/", methods=["GET", "POST"])
def auth():
    global authorized
    if request.method == "GET":
        return render_template("auth.html")

    login = request.form.get("login")
    password = request.form.get("password")

    if not check_auth(login, password):
        return f"sorry you don't have permission"
    authorized = True
    return render_template("main.html", items=get_ttn_fromdb())


@app.route("/parsing", methods=["POST"])
def parser():
    global authorized
    if authorized:
        parsing()
        return render_template("main.html", items=get_ttn_fromdb())
    else:
        return "You haven't authorized!!"


@app.route("/settings", methods=["POST"])
def settings():
    global authorized
    if authorized:
        return render_template("settings.html", items=get_settings("settings"))


@app.route("/settings_edit", methods=["POST"])
def setting_edit():
    global authorized
    if authorized:
        return render_template("settings_edit.html", items=get_settings("settings"))


@app.route("/main", methods=["POST"])
def main():
    global authorized
    if authorized:
        return render_template("main.html", items=get_ttn_fromdb())


@app.route("/save_settings", methods=["POST"])
def save_settings():
    global authorized
    if authorized:
        save_to_file(request.form["alter"], "settings/alter.ini")
        save_to_file(request.form["code"], "settings/code.ini")
        return render_template("settings.html", items=get_settings("settings"))


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    file.save("settings/" + file.filename)
    return render_template("settings.html", items=get_settings("settings"))
