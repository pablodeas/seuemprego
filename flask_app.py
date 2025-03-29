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
#app.secret_key = os.getenv("SECRET_KEY")
app.secret_key = "secret_key"

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
    email = db.Column(db.String(150), unique=True, nullable=False)
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

@app.route("/", methods=["GET"])
def index():
    vagas = Vaga.query.all()
    return render_template("main_page.html", vaga=vagas)

# Rota para login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Verificar se o usuário existe com o nome de usuário e email
        usuario = Usuario.query.filter_by(username=username, email=email).first()
        if usuario and usuario.check_password(password):
            session["logged_in"] = True
            session["user_id"] = usuario.id
            session["username"] = usuario.username
            flash("Olá, tudo bem? Todas as vagas são apagadas no primeiro domingo do mês, então fique de olho 😉.", "info")
            return redirect(url_for("index"))
        else:
            flash("Usuário, email ou senha inválidos.", "danger")
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

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Verificar se o usuário já existe
        if Usuario.query.filter_by(username=username).first():
            flash("Usuário já existe. Escolha outro nome.", "danger")
            return redirect(url_for("register"))

        # Criar novo usuário
        novo_usuario = Usuario(username=username, email=email)
        novo_usuario.set_password(password)
        db.session.add(novo_usuario)
        db.session.commit()
        flash("Conta criada com sucesso! Faça login.", "success")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/alterar_senha", methods=["GET", "POST"])
def alterar_senha():
    if not session.get("logged_in"):
        flash("Você precisa fazer login para acessar esta página.", "warning")
        return redirect(url_for("login"))
    if request.method == "POST":
        usuario_id = session.get("user_id")
        usuario = Usuario.query.get(usuario_id)
        senha_atual = request.form["senha_atual"]
        nova_senha = request.form["nova_senha"]

        if not usuario.check_password(senha_atual):
            flash("Senha atual incorreta.", "danger")
            return redirect(url_for("alterar_senha"))

        usuario.set_password(nova_senha)
        db.session.commit()
        flash("Senha alterada com sucesso!", "success")
        return redirect(url_for("privado"))
    return render_template("alterar_senha.html")

if __name__ == "__main__":
    app.run(debug=True)