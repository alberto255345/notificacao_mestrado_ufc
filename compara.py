import json
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class JSONData(Base):
    __tablename__ = 'json_email_notificacao'

    id = Column(Integer, primary_key=True)
    json_data = Column(JSON)

def comparar_e_salvar_json(df, host, user, password, database):
    
    engine = create_engine(f'postgresql://{user}:{password}@{host}/{database}')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Ler o último JSON salvo
    json_antigo = session.query(JSONData).order_by(JSONData.id.desc()).first()

    # carrega no json
    valor_jason = json.loads(json_antigo.json_data)

    df1 = pd.DataFrame(valor_jason)

    # Use o método merge para encontrar as diferenças entre os DataFrames
    diferencas = pd.merge(df, df1, how='outer', indicator=True).loc[lambda x : x['_merge'] != 'both']

    left_only = diferencas[diferencas['_merge'] == 'left_only']

    # Se houver diferenças apenas no DataFrame à esquerda
    if not left_only.empty:
        # Gerar a tabela HTML
        html_table = left_only.to_html(index=False)

        # Exibir a tabela HTML
        print("diferença encontrada")
    else:
        # Se não houver diferenças apenas no DataFrame à esquerda, exibir uma mensagem
        print("Não há novidades presentes apenas no DataFrame à esquerda.")

    # Salvar o novo JSON e atualizar o banco de dados
    json_novo = df.to_json(orient='records')
    novo_dado = JSONData(json_data=json_novo)
    session.add(novo_dado)
    session.commit()

    return html_table

