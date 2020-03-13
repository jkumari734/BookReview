from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/index")
def homepage():
    return render_template("index.html")

@app.route("/register", methods=["POST","GET"])
def register():
    username = request.form.get("username")
    name = request.form.get("name")
    pwd = request.form.get("password")
    return render_template("register.html", name=name, username=username, password=pwd)

@app.route("/login", methods=["POST","GET"])
def login():
    username = request.form.get("username")
    # name = request.form.get("name")
    pwd = request.form.get("password")
    return render_template("login.html", username=username, password=pwd)

@app.route("/results", methods=["POST","GET"])
def results():
    true=False
    return render_template("searchresults.html", true=False)
