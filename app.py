from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, g, request, url_for
from flask_session import Session
from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///maze.db")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

@app.route('/')
@login_required
def index():
    #create table in SQL to store the moves
    return render_template('index.html')

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if not request.form.get("username"):
            flash("Please provide your Username")
            return render_template("register.html")
        else:
            username = request.form.get("username")
            try:
                db.execute("INSERT INTO users (username) VALUES(?)", username)
            except:
                flash("Username already taken")
                return render_template("register.html")
            return redirect("/login")
    else:
        return render_template("register.html")    


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("Please provide your Username")
            return render_template("login.html")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 :
            flash("Invalid Username")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")    

#do a login like finance app but using flash instead of apology() - DONE

#do the base html page

#create the index page

#decide what sql database will be like

#index page to display moves and add moves, like birthday app.py

#add random event every 5 moves maybe using flash?