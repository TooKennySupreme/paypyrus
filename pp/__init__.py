import time
from . import config
from datetime import datetime
from utils.venmo_util import VenmoAPI
from utils import qrcode
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

def create_redemption_url(bill_token):
    return "http://paypyrus.rcket.science/redeem/{}".format(bill_token)


@app.route("/stats/")
def stats():
    bills = Bill.select().where(Bill.creator == session["username"])
    return render_template("stats.html", full_name=session["name"], bills=bills)

@app.route("/backs/<num>/")
def backs(num):
    num = int(num)
    return render_template("backs.html", num=xrange(0, num))

@app.route("/api/v1/get_bill", methods=["POST", "GET"])
def api_v1_get_picture():
    quantities = {
        0.01: request.form["quantity_1"] or 0,
        1: request.form["quantity_5"] or 0,
        2: request.form["quantity_10"] or 0
    }
    username = session["username"]

    current_time = int(time.time())
    bill_tokens = []
    urls = []

    for denomination in quantities:
        if denomination == 0:
            return False
        quantity = int(quantities[denomination])
        bill_tokens = create_bill(username, denomination, quantity, current_time)
        for bt in bill_tokens:
            urls.append(create_redemption_url(bt))

    print urls
    qr_urls = [qrcode.svgfilename(url) for url in urls]
    return ",".join(qr_urls)

@app.route("/scan")
def scan():
    return render_template("qrscanner.html")

@app.route("/redeem/<token>")
def redeem(token):
    exists = Bill.select().where(Bill.bill_token == token).exists()
    if not exists:
        return render_template("error.html", error="The bill you scanned has an incorrect token.")

    return render_template("redeem.html", token=token)

@app.route("/api/v1/redeem/<token>/", methods=["GET", "POST"])
def api_v1_redeem(token):
    phone_email = request.form["phone_email"]
    isPhone = '@' not in phone_email

    bill = Bill.select().where(Bill.bill_token == token).first()
    user = bill.user
    amount = bill.amount

    auth_key = user.auth_key

    if not bill.spent:
        try:
            current_time = int(time.time())

            vapi.make_transaction(isPhone, phone_email, auth_key, amount)
            bill.spent = True
            bill.ip = request.remote_addr
            bill.redeemer_id = phone_email
            bill.time_redeemed = current_time
            bill.save()
            return "OK"
        except:
            return "Sorry. The phone number/email you entered is invalid."
    else:
        return "Sorry. The paypyrus you scanned has already been redeemed."

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

@app.route("/print/<bills_list>")
def csv_bills(bills_list):
    bills_array = bills_list.split(",")
    return render_template("bills.html", bills_array=bills_array)

@app.route("/api/v1/check_balance/<token>/", methods=["GET", "POST"])
def check_balance(token):
    bill = Bill.select().where(Bill.bill_token == token).first()
    amount = bill.amount
    if bill.spent == True:
        return "0.00"
    else:
        return str(amount)

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
    print denomination
    print quantity
    user = User.select().where(User.username == username)
    btokens = []
    for i in range(quantity):
        bill_token = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(75))
        btokens.append(bill_token)
        Bill.create(
            user = user,
            creator = username,
            amount = denomination,
            time = time,
            bill_token = bill_token
        )
    return btokens

@app.template_filter('ctime')
def timectime(s):
    return format(datetime.fromtimestamp(s), '%m/%d/%Y  %H:%M:%S')

#@app.errorhandler(Exception)
#def handle_exceptions(error):
#   return render_template("error.html"), 500

@app.template_filter('format_time')
def format_time(n):
    if n == 0:
        return "n/a"
    return n

@app.template_filter('format_monies')
def format_monies(s):
    return "$%.2f" % s

if __name__ == '__main__':
    app.run(debug=True, port=5000)
