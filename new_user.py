from flask_app import db, Usuario

USERNAME = input("User: ")
EMAIL = input("Email: ")
ADMIN = input("Admin? (Apenas: True ou False): ").strip().lower() == "true"  # Converte para booleano
SENHA = input("Senha: ")  # Mantém a senha como string

admin = Usuario(username=USERNAME, email=EMAIL, is_admin=ADMIN)
admin.set_password(SENHA)  # Define a senha usando o método do modelo
db.session.add(admin)
db.session.commit()

print(f"Usuário '{USERNAME}' criado com sucesso!")