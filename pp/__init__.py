import time
from . import config
from utils.venmo_util import VenmoAPI
from flask import Flask
from flask import url_for, render_template, redirect, session, request
from models import *
import string, random

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
        return render_template("user.html", full_name=session["name"])
    else:
        return redirect(url_for("login"))

@app.route("/api/v1/get_bill", methods=["POST", "GET"])
def api_v1_get_picture():
    quantities = {
        0.01: request.form["quantity_1"] or 0,
        5: request.form["quantity_5"] or 0,
        10: request.form["quantity_10"] or 0
    }
    username = session["username"]

    current_time = int(time.time())
    for denomination in quantities:
        # try:
        quantity = int(quantities[denomination])
        create_bill(username, denomination, quantity, current_time)
        # except:
        #     return "Invalid quantities"
    return "OK"

@app.route("/api/v1/redeem/<token>")
def api_v1_redeem(token):
    phone_email = request.form["phone_email"]
    isPhone = '@' not in phone_email

    bill = Bill.select().where(Bill.bill_token == token)
    user = bill.user
    amount = bill.amount
    auth_key = user.auth_key

    vapi.make_transaction(isPhone, phone_email, auth_key, amount)

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

    username = user_info["user"]["username"]
    name = user_info["user"]["first_name"] + " " + user_info["user"]["last_name"]
    email = user_info["user"]["email"]
    auth_key = user_info["access_token"]
    create_user(username, auth_key, email)

    session["username"] = username
    session["name"] = name

    return redirect(url_for("user_dashboard"))

@app.route("/logout/")
def logout():
    session.pop("auth_code", '')
    session.pop("username", '')
    session.pop("name", '')
    return redirect(url_for("index"))

def create_user(username, auth_key, email):
    sq = User.select().where(User.username == username)
    if not sq.exists():
        user = User.create(
            username = username,
            auth_key = auth_key,
            email = email
        )
        print "User created"
    print "User already exists"

def create_bill(username, denomination, quantity, time):
    user = User.select().where(User.username == username)
    for i in range(quantity):
        bill_token = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(100))
        Bill.create(
            user = user,
            creator = username,
            amount = denomination,
            time = time,
            bill_token = bill_token
        )

# @app.errorhandler(Exception)
# def handle_exceptions(error):
#    return render_template("error.html"), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
