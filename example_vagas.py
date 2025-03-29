from flask_app import db, Vaga

# Vagas de exemplo
vagas = [
    {   
        "id": 1,
        "info": "Desenvolvimento de aplicações web utilizando Python e Flask.",
        "titulo": "Desenvolvedor Python",
        "salario": "R$ 6.000,00",
        "escala": "Segunda a Sexta",
        "local": "Remoto",
        "contato1": "contato@empresa.com",
        "contato2": "1234-5678"
    },
    {   
        "id": 1,
        "info": "Gerenciamento de projetos ágeis e liderança de equipes.",
        "titulo": "Gerente de Projetos",
        "salario": "R$ 8.500,00",
        "escala": "Segunda a Sexta",
        "local": "São Paulo - SP",
        "contato1": "rh@empresa.com",
        "contato2": "9876-5432"
    },
    {
        "id": 1,
        "info": "Atendimento ao cliente e suporte técnico.",
        "titulo": "Analista de Suporte",
        "salario": "R$ 3.200,00",
        "escala": "Escala 6x1",
        "local": "Rio de Janeiro - RJ",
        "contato1": "suporte@empresa.com",
        "contato2": "4567-8901"
    }
]

# Adicionar vagas ao banco de dados
for vaga_data in vagas:
    vaga = Vaga(**vaga_data, usuario_id=None)  # usuario_id pode ser None ou um ID válido
    db.session.add(vaga)

db.session.commit()

print("Vagas de exemplo criadas com sucesso!")