import os
from flask import (
    Flask, render_template, redirect, flash, url_for, request, session)
if os.path.exists("env.py"):
    import env


app = Flask(__name__)
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

""" I copied the code to set up flask from line 1 to 15
& the last line from the 2020 task manager mini project videos """


@app.route("/")
def hello():
    return "Hello World"


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)

