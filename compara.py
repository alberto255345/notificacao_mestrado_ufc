import json
from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class JSONData(Base):
    __tablename__ = 'json_email_notificacao'

    id = Column(Integer, primary_key=True)
    json_data = Column(JSON)

def comparar_e_salvar_json(json_novo, host, user, password, database):
    # Converta a string JSON em um objeto JSON
    json_novo_obj = json.loads(json_novo)
    
    engine = create_engine(f'postgresql://{user}:{password}@{host}/{database}')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Ler o último JSON salvo
    json_antigo = session.query(JSONData).order_by(JSONData.id.desc()).first()

    # Comparar e encontrar a diferença entre os JSONs
    diferenca = {}
    if json_antigo:
        for chave, valor in json_novo_obj.items():
            if chave not in json_antigo.json_data or json_antigo.json_data[chave] != valor:
                diferenca[chave] = valor
        print("Diferença encontrada:", diferenca)
    else:
        print("Não há JSON anterior no banco de dados.")

    # Salvar o novo JSON e atualizar o banco de dados
    novo_dado = JSONData(json_data=json_novo)
    session.add(novo_dado)
    session.commit()

    return diferenca

