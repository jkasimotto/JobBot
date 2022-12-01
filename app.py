from redis import Redis
from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session

app = Flask(__name__)

# app.secret_key = 'dev'

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = "/tmp"
app.config["SECRET_KEY"] = "dev"
Session(app, store=Redis(host="localhost", port=6379))

@app.route("/")
def hello_world():
    return render_template("index.html", title="Hello")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    # Check if the request method is "POST"
    if request.method == "POST":
        # Get the passcode from the user's input
        # The user entered four digits in separate input fields
        passcode = request.form.get("digit1") + request.form.get("digit2") + request.form.get("digit3") + request.form.get("digit4")

        # Check if the passcode is correct
        if passcode == "1234":
            # Set the logged_in session variable
            session["logged_in"] = True
            print(session["logged_in"])

            # Redirect the user to the work screen
            return redirect(url_for("work"))

        else:
            # The passcode was incorrect, so return an error message
            error = "Invalid passcode"

    # Render the login screen
    return render_template("login.html", error=error)

# Define the work route
@app.route("/work", methods=["GET", "POST"])
def work():
    # Check if the user is logged in
    print(session.get("logged_in"))
    if session.get("logged_in"):
        # The user is logged in, so render the work screen
        return render_template("work.html")

    else:
        # The user is not logged in, so redirect them to the login screen
        return redirect(url_for("login"))