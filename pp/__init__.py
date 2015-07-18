from . import config
from flask import Flask
from flask import url_for, render_template, redirect

app = Flask('pp')
app.secret_key = config.secret_key

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/login/")
def login():
    return render_template("login.html")


if __name__ == '__main__':
    app.run(debug=True, port=5000)
