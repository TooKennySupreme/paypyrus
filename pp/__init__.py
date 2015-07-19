from . import config
from utils.venmo_util import VenmoAPI
from flask import Flask
from flask import url_for, render_template, redirect, session, request

app = Flask('pp')
app.secret_key = config.secret_key
vapi = VenmoAPI()

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/login/")
def login():
    return render_template("login.html")

@app.route("/venmo_auth/")
def venmo_auth():
    return redirect(vapi.authorize())

@app.route("/user/")
def user_dashboard():
    # User dashboard, must be logged in
    if session["username"]:
        return "ur logged in"
    else:
        return redirect(url_for("login"))

@app.route("/oauth/")
def oauth():
    error = request.args.get('key', '')
    auth_code = request.args.get('key', '')
    if error != '':
        return render_template("error.html",
                                error="Sorry. It seems like something went wrong while authenticating your account. Try again later.")
    else:
        session["auth_code"] = auth_code

    # get username, email, etc
    user_info = vapi.get_user_data(auth_code)
    session["username"] = user_info["user"]["username"]
    session["name"] = user_info["user"]["first_name"] + " " + user_info["user"]["last_name"]
    return redirect(url_for("user_dashboard"))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
