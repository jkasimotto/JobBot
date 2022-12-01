import os
from redis import Redis
from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# app.secret_key = 'dev'

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "redis"
app.config["SECRET_KEY"] = "dev"
app.config.update(SESSION_COOKIE_SAMESITE="None", SESSION_COOKIE_SECURE=True)
Session(app)

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
            session["messages"] = ["Hey! How are you doing today? My name is K."]
            session.modified = True
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
    if session.get("logged_in"):
        # The user is logged in, so render the work screen
        return render_template("work.html", messages=session["messages"])

    else:
        # The user is not logged in, so redirect them to the login screen
        return redirect(url_for("login"))

@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():
    if request.method == "POST":
        # Get the response from the user's input
        message = request.form.get("message")
        session["messages"].append(message)
        prompt = construct_prompt(session["messages"])
        print(prompt)
        chatbot_message = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.9,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=["Client:"],
        )
        session["messages"].append(chatbot_message["choices"][0]["text"].replace("K:", ""))
        session.modified = True

        return render_template("work.html", messages=session.get("messages"))
    else:
        pass


def construct_prompt(messages):
    prompt = "K is an expert in recruitment and career advice. K understands many people are unaware of the multitude of jobs that exist out there. K asks deeply personal questions to best understand what job would suit his client. K knows that asking people what kind of job they're looking for is pointless; instead K asks questions about their personality and experiences. K also recognises that open ended questions can cause his client's to miss alot of information. The following is a converastion between K and a client."
    for i, message in enumerate(messages):
        if i % 2 == 0:
            prompt += f"K: {message}"
        else:
            prompt += f"Client: {message}"
    prompt += "K:"
    return prompt