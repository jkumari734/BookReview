import os
import requests
from flask import Flask, render_template, request

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgres://ogunfriattpack:6084243ceb1f939e574a96f953366c04e509075f182edd0089fdef631acd65a5@ec2-18-235-97-230.compute-1.amazonaws.com:5432/d2gkkmcmdcahl4")
db = scoped_session(sessionmaker(bind=engine)) 

app = Flask(__name__)


@app.route("/")
def index():
    books = db.execute("SELECT author, title FROM books where year > 2016").fetchall()
    return render_template("index.html", books=books)

@app.route("/index")
def homepage():
    return render_template("index.html")


@app.route("/registration", methods=["POST","GET"])
def registration():
    return render_template("register.html")

@app.route("/register", methods=["POST","GET"])
def register():
    username = request.form.get("username")
    name = request.form.get("name")
    pwd = request.form.get("password")
    db.execute("INSERT INTO users (username, name, password) VALUES (:username, :name, :password)", {"username":username, "name":name,"password":pwd})
    db.commit()
    return render_template("login.html")


@app.route("/loginpage", methods=["POST","GET"])
def loginPage():
    return render_template("login.html")

@app.route("/login", methods=["POST","GET"])
def login():
    username = request.form.get("username")
    pwd = request.form.get("password")
    name = db.execute("SELECT name FROM users where username = :username AND password = :password", {"username":username, "password":pwd}).fetchall()
    if len(name) == 1:
        return render_template("user.html", name=name[0][0])
    else:
        return render_template("error.html")

@app.route("/searchpage", methods=["POST","GET"])
def search():
    bookid = request.form.get("bookname")
    # print("enter this method search", bookid)
    temp = db.execute("SELECT title, isbn FROM books where year = :bookid", {"bookid":bookid}).fetchall()
    # print(temp,"result")
    if len(temp) > 0:
        return bookDetails(temp)
        # return render_template("success.html")
    else:
        return render_template("error.html", message="book not found")

@app.route("/bookdetails", methods=["GET", "POST"])
def bookDetails(title):
    # print("****************detail****************", title)
    display = []
    global booklist 
    booklist = []
    for i in title:
        url = "https://www.goodreads.com/book/review_counts.json?key={uaE76ht3BP8fSW3tl6RoQ}&isbns="
        temp = db.execute("SELECT isbn, username, rating, textreview FROM bookreviews WHERE isbn = :isbn", {"isbn":i[1]}).fetchall()
        u = requests.get(url+i[1])
        # print(u,"status")
        if u.status_code == 200:
            x = u.json()
            count = x['books'][0]['ratings_count']
            avgRating = float(x['books'][0]['average_rating'])
        else:
            count = 0
            avgRating = 0
        if len(temp) > 0:
            booklist.append(temp)
            display.append([i[0], count, avgRating, temp[0][0], temp[0][1], temp[0][2], i[1]])
        else:
            display.append([i[0], count, avgRating, None, None, None, i[1]])
        
    return render_template("bookdetails.html", title=display)

@app.route("/reviewsubmit/<string:i>", methods=["GET","POST"])
def reviewSubmit(i):
    x = db.execute("SELECT isbn, title, author, year FROM books WHERE isbn = :isbn",{"isbn":i}).fetchall()
    reviews = db.execute("SELECT username, rating, textreview FROM bookreviews WHERE isbn = :isbn", {"isbn":i}).fetchall()    
    # print(x,"gfjkgf")   
    return render_template("submitreview.html", x=x, reviews=reviews, username=x[0][0], rating=x[0][1], textreview=x[0][2], i=i)

@app.route("/review/<string:i>", methods=["POST","GET"])
def submit(i):
    username = request.form.get("username")
    rating = request.form.get("rating")
    textreview = request.form.get("textreview")
    db.execute("INSERT INTO bookreviews (isbn, username, rating, textreview) VALUES (:isbn, :username, :rating, :textreview)", {"isbn":i, "username":username, "rating":rating, "textreview":textreview})
    db.commit()
    return render_template("success.html", message="Thanks for the review!")



