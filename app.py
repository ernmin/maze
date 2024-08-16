from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///history.db")

@app.route('/')
def index():
    return render_template('index.html')

#do a login like finance app but using flash instead of apology()

#do the base html page

#create the index page

#decide what sql database will be like

#index page to display moves and add moves, like birthday app.py