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
        return render_template("user.html")
    else:
        return redirect(url_for("login"))

@app.route("/api/v1/get_bill", methods=["POST", "GET"])
def api_v1_get_picture():
    amount = request.form["amount"]
    username = session["username"]
    if amount > 10:
        return "Currently, papyrus only supports amounts under $10. Sorry for the inconvenience."
    # process payment

@app.route("/oauth/")
def oauth():
    error = request.args.get('error', '')
    auth_code = request.args.get('code', '')
    if error != '':
        return render_template("error.html",
                                error="Sorry. It seems like something went wrong while authenticating your account. Try again later.")
    else:
        session["auth_code"] = auth_code

    # get username, email, etc
    try:
        user_info = vapi.get_user_data(auth_code)
    except ValueError:
        return render_template("error.html", error="Unable to validate your account. Please try <a href='/logout'>logging out</a> and trying again.")


    session["username"] = user_info["user"]["username"]
    session["name"] = user_info["user"]["first_name"] + " " + user_info["user"]["last_name"]
    return redirect(url_for("user_dashboard"))

@app.route("/logout/")
def logout():
    session.pop("auth_code", '')
    session.pop("username", '')
    session.pop("name", '')
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
