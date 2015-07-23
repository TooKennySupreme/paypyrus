import time
from . import config
from datetime import datetime
from utils.venmo_util import VenmoAPI
from utils import qrcode, encryption
from flask import Flask
from flask import url_for, render_template, redirect, session, request, Response
from models import *
import string, random, mimetypes

mimetypes.add_type('image/svg+xml', '.svg')

app = Flask('pp')
app.secret_key = config.secret_key
vapi = VenmoAPI()

def must_be_logged_in():
    return render_template("error.html", error="You must be logged in to view this page.")

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

def create_bill_url(bill_token):
    return "{}/show_bill/{}".format(config.current_host, bill_token)

@app.route("/qr_svg/<token>/")
def get_qr_svg(token):
    try:
        bill_svg = QRCode.select().where(QRCode.qr_token == token).first()
        bill_svg_string = bill_svg.qr_code_string.decode("base64")
        return Response(bill_svg_string, mimetype='image/svg+xml')
    except:
        return "404", 404

@app.route("/show_bill/<token>/")
def show_bill(token):
    return render_template("show_bill.html", token=token)

@app.route("/stats/")
def stats():
    bills = Bill.select().where(Bill.creator == session["username"])
    return render_template("stats.html", full_name=session["name"], bills=bills)

@app.route("/backs/<num>/")
def backs(num):
    num = int(num)
    return render_template("backs.html", num=xrange(0, num))

@app.route("/settings/")
def settings():
    if session.get("username") != None:
        return render_template("settings.html")
    else:
        return must_be_logged_in()

@app.route("/delete_account/")
def delete_account():
    username = session.get("username")
    if username != None:
        Bill.delete().where(Bill.creator == username).execute()
        QRCode.delete().where(QRCode.creator == username).execute()
        User.delete().where(User.username == username).execute()
        logout_user()
        return render_template("generic.html", message="""
        Your account and all associated bills have been deleted. You may recreate
         your account by simply logging back in.
        """)
    else:
        return must_be_logged_in()

@app.route("/api/v1/delete_bill/", methods=["GET", "POST"])
def api_v1_delete_bill():
    username = session["username"]
    bill_token = request.form["bill_token"]
    bill = Bill.select().where(Bill.bill_token == bill_token).first()
    print bill
    if bill.creator != username:
        return "You cannot delete a bill you do not own!", 401
    else:
        Bill.delete().where(Bill.bill_token == bill_token).execute()
        QRCode.delete().where(QRCode.qr_token == bill_token).execute()
        return "OK"


@app.route("/api/v1/get_bill/", methods=["POST", "GET"])
def api_v1_get_picture():
    custom_amount = request.form.get("custom_amount")
    if custom_amount != None:
        try:
            custom_amount = float(custom_amount)
        except:
            return "Invalid custom amount. ", 400

    if custom_amount > 100:
        return "Sorry, but we do not currently allow denominations over $100.", 400

    if custom_amount:
        quantities = {
            custom_amount: 1
        }
    else:
        quantities = {
            0.01: request.form["quantity_1"] or 0,
            1: request.form["quantity_5"] or 0,
            2: request.form["quantity_10"] or 0
        }

        if sum([int(i) for i in quantities.values()]) > 50:
            return "You may not create more than 50 bills at once.", 400

    username = session["username"]

    current_time = int(time.time())
    bill_tokens = []
    toks = []

    for denomination in quantities:
        if denomination == 0:
            return False
        quantity = int(quantities[denomination])
        bill_tokens = create_bill(username, denomination, quantity, current_time)
        for bt in bill_tokens:
            toks.append(bt)

    for tok in toks:
        qrcode.qrfilegen(tok, session["username"])

    return ",".join(toks)

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
    reason = request.form.get("reason")
    isPhone = '@' not in phone_email

    bill = Bill.select().where(Bill.bill_token == token).first()
    user = bill.user
    amount = bill.amount

    auth_key = encryption.decrypt_aes(user.auth_key)

    if not bill.spent:
        try:
            current_time = int(time.time())
            if reason == "":
                reason = None

            vapi.make_transaction(isPhone, phone_email, auth_key, amount, reason)
            bill.spent = True
            bill.ip = request.remote_addr
            bill.redeemer_id = phone_email
            bill.time_redeemed = current_time
            bill.save()
            return "OK"
        except Exception as e:
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
    encrypted_auth_key = encryption.encrypt_aes(auth_key)

    create_user(username, encrypted_auth_key, email)

    session["username"] = username
    session["name"] = name

    return redirect(url_for("user_dashboard"))

def logout_user():
    session.pop("auth_code", '')
    session.pop("username", '')
    session.pop("name", '')

@app.route("/logout/")
def logout():
    logout_user()
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

if config.in_production == True:
    @app.errorhandler(Exception)
    def handle_exceptions(error):
        print error
        return render_template("error.html"), 500

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
