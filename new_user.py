from flask_app import db, Usuario

USERNAME = input(".User: ")
EMAIL = input(".Email: ")
ADMIN = input(".Admin? (Apenas: True ou False):")
SENHA = int(input(".Senha: "))

admin = Usuario(username=USERNAME, email=EMAIL, is_admin=ADMIN)
admin.set_password(SENHA)
db.session.add(admin)
db.session.commit()