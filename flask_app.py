import os
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

"""
TODO:   Antes de subir a aplicação, dar drop table.
"""
app = Flask(__name__)
app.config["DEBUG"] = False

project_folder = os.path.expanduser('~/mysite')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))

USERNAME = os.getenv("DB_USERNAME")
PASSWORD = os.getenv("DB_PASSWORD")
HOSTNAME = os.getenv("DB_HOSTNAME")
DATABASE = os.getenv("DB_DATABASE")

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username=USERNAME,
    password=PASSWORD,
    hostname=HOSTNAME,
    databasename=DATABASE,
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Vaga(db.Model):
    __tablename__ = "vaga"
    id = db.Column(db.Integer, primary_key=True)
    info = db.Column(db.String(2000))
    titulo = db.Column(db.String(2000))
    salario = db.Column(db.String(1000))
    escala = db.Column(db.String(1000))
    local = db.Column(db.String(1500))
    contato1 = db.Column(db.String(1250))
    contato2 = db.Column(db.String(1250))

@app.route("/", methods=["GET"])
def index():
    vagas = Vaga.query.all()
    return render_template("main_page.html", vaga=vagas)

@app.route("/add_vaga", methods=["GET", "POST"])
def add_vaga():
    if request.method == "POST":
        # Processa os dados do formulário
        vaga = Vaga(
            info=request.form["info"],
            titulo=request.form["titulo"],
            salario=request.form["salario"],
            escala=request.form["escala"],
            local=request.form["local"],
            contato1=request.form["contato1"],
            contato2=request.form["contato2"],
        )
        db.session.add(vaga)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("add_vaga.html")

if __name__ == "__main__":
    app.run(debug=True)