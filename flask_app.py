import os
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

"""
TODO:   Antes de subir a aplicação, dar drop table.
"""
app = Flask(__name__)
app.config["DEBUG"] = False
app.secret_key = "sua_chave_secreta"  # Substitua por uma chave secreta segura

project_folder = os.path.expanduser('~/mysite')  # Ajustar dependendo do ambiente
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

class Usuario(db.Model):
    __tablename__ = "usuario"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    vagas = db.relationship("Vaga", backref="criador", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)

# Usuário e senha para autenticação (pode ser armazenado em um banco de dados)
USUARIO = "admin"
SENHA = "1234"

@app.route("/", methods=["GET"])
def index():
    vagas = Vaga.query.all()
    return render_template("main_page.html", vaga=vagas)

# Rota para login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        usuario = Usuario.query.filter_by(username=username).first()
        if usuario and usuario.check_password(password):
            session["logged_in"] = True
            session["user_id"] = usuario.id
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("index"))
        else:
            flash("Usuário ou senha inválidos.", "danger")
    return render_template("login.html")

# Rota para logout
@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("Você saiu da conta.", "info")
    return redirect(url_for("login"))

# Proteção da rota de adicionar vaga
@app.route("/add_vaga", methods=["GET", "POST"])
def add_vaga():
    if not session.get("logged_in"):
        flash("Você precisa fazer login para acessar esta página.", "warning")
        return redirect(url_for("login"))
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
            usuario_id=session.get("user_id")  # Assuming user_id is stored in session
        )
        db.session.add(vaga)
        db.session.commit()
        flash("Vaga adicionada com sucesso!", "success")
        return redirect(url_for("index"))
    return render_template("add_vaga.html")

@app.route("/privado", methods=["GET", "POST"])
def privado():
    if not session.get("logged_in"):
        flash("Você precisa fazer login para acessar esta página.", "warning")
        return redirect(url_for("login"))
    usuario_id = session.get("user_id")
    vagas = Vaga.query.filter_by(usuario_id=usuario_id).all()
    return render_template("privado.html", vagas=vagas)

@app.route("/delete_vaga/<int:vaga_id>", methods=["POST"])
def delete_vaga(vaga_id):
    if not session.get("logged_in"):
        flash("Você precisa fazer login para acessar esta página.", "warning")
        return redirect(url_for("login"))
    vaga = Vaga.query.get_or_404(vaga_id)
    if vaga.usuario_id != session.get("user_id"):
        flash("Você não tem permissão para deletar esta vaga.", "danger")
        return redirect(url_for("privado"))
    db.session.delete(vaga)
    db.session.commit()
    flash("Vaga deletada com sucesso!", "success")
    return redirect(url_for("privado"))

if __name__ == "__main__":
    app.run(debug=True)