from flask_mail import Mail, Message
from flask import Flask

app = Flask(__name__)

# Configuração do Flask-Mail
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "seuempregoconf@gmail.com"
app.config["MAIL_PASSWORD"] = "Maitou26561483"
app.config["MAIL_DEFAULT_SENDER"] = "seuempregoconf@gmail.com"

mail = Mail(app)

with app.app_context():
    try:
        msg = Message("Teste de Email", recipients=["destinatario@gmail.com"])
        msg.body = "Este é um email de teste."
        mail.send(msg)
        print("Email enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar email: {e}")