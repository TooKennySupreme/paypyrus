from . import config
from flask import Flask
from flask import url_for, render_template, redirect, session

app = Flask('pp')
app.secret_key = config.secret_key

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/login/")
def login():
    return render_template("login.html")

@app.route("/venmo_auth/")
def venmo_auth():
    pass

@app.route("/user/")
def user_dashboard():
    # User dashboard, must be logged in
    pass

@app.route("/oauth/")
def oauth():
    error = request.args.get('key', '')
    auth_code = request.args.get('key', '')
    if error not '':
        return render_template("error.html",
                                error="Sorry. It seems like something went wrong while authenticating your account. Try again later.")
    else:
        session["auth_code"] = auth_code



if __name__ == '__main__':
    app.run(debug=True, port=5000)
