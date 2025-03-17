import os
from load_dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

USERNAME = "pablodeas"
PASSWORD = os.getenv("PASSWORD")
HOSTNAME = os.getenv("HOSTNAME")
DATABASENAME = "pablodeas"

app = Flask(__name__)
app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username=USERNAME,
    password=PASSWORD,
    hostname=HOSTNAME,
    databasename=DATABASENAME,
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Comment(db.Model):

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(4096))


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("main_page.html", comments=Comment.query.all())

    comment = Comment(content=request.form["contents"])
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('index'))