from flask_app import db

def executar_query(query):
    """
    Executa uma query SQL específica no banco de dados.
    
    :param query: A query SQL a ser executada (string).
    """
    try:
        # Executa a query
        resultado = db.session.execute(query)
        db.session.commit()

        # Exibe os resultados, se houver
        if resultado.returns_rows:
            for row in resultado:
                print(row)
        else:
            print("Query executada com sucesso!")
    except Exception as e:
        print(f"Erro ao executar a query: {e}")
    finally:
        db.session.close()

if __name__ == "__main__":
    print("Bem-vindo ao executor de queries!")
    query = input("Digite a query SQL que deseja executar:\n")
    executar_query(query)