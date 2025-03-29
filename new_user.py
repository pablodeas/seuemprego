from flask_app import db, Usuario

# Criar um novo usuário
novo_usuario = Usuario(username="admin")
novo_usuario.set_password("1234")
db.session.add(novo_usuario)
db.session.commit()