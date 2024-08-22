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

def majority(P1, P2, P3, P4):
    votes = [P1, P2, P3, P4]
    votes_table = {}
    for vote in votes:
        if vote in votes_table:
            votes_table[vote] += 1
        else:
            votes_table[vote] = 1
    if len(votes_table) == 1:
        for key, value in votes_table.items():
            return key
    elif len(votes_table) == 4:
        return 'Draw'
    elif len(votes_table) == 3:
        for key, value in votes_table.items():
            if value == 2:
                return key
            else:
                continue
    else:
        for key, value in votes_table.items():
            if value == 3:
                return key
            elif value == 2:
                return 'Draw'
            else:
                continue


@app.route('/', methods=["GET", "POST"])
@login_required
def index():
    user_id = session["user_id"]
    if request.method == "POST":
        if request.form['btn'] == 'move':
            P1 = request.form.get("P1")
            P2 = request.form.get("P2")
            P3 = request.form.get("P3")
            P4 = request.form.get("P4")
            team = majority(P1,P2,P3,P4)
            #if no option is given site will crash, code below does not work
            if P1 == None or P2 == None or P3 == None or P4 == None:
                flash("Please fill in the moves")
                return redirect('/')
            else:
                db.execute("INSERT INTO moves (user_id, P1, P2, P3, P4, Team) VALUES(?, ?, ?, ?, ?, ?)", user_id, P1, P2, P3, P4, team)
                return redirect("/")
        
        elif request.form['btn'] == 'delete':
            db.execute("DELETE FROM moves ORDER BY time DESC LIMIT 1")
            return redirect("/")
    else:
        rows = db.execute("SELECT * FROM moves WHERE user_id = ?", user_id)
        return render_template('index.html', rows = rows, user_id = user_id)
#how to number the moves and delete the moves, only can delete the latest move and not the previous moves

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

#how to only display moves for your account?

#add random event every 5 moves maybe using flash?