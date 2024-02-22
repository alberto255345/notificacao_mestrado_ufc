# [START ndb_flask]
from flask import Flask
from flask import request  # Importe o objeto request
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import dotenv
import os
from secretmanager import get_json_secret

app = Flask(__name__)

if not os.path.exists(".env"):
    try:
        # carrega secret
        payload = get_json_secret(project_id, secret_name)
        # Converte a string JSON em um dicionário Python
        secret_dict = json.loads(payload)
        # Define cada chave do dicionário como uma variável de ambiente
        for key, value in secret_dict.items():
            os.environ[key] = value
    except Exception as e:
        # Carrega valores de exemplo se o .env não existe
        dotenv.load_dotenv(".env.example")
else:
    dotenv.load_dotenv(".env")

@app.route("/index", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # validação
        print('Entrou POST')
        return "POST request recebida com sucesso!"
    else:
        # validação
        print('Entrou GET')

        # definindo que usaremos o Firefox sem carregar a página graficamente
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')

        # carregando uma página da Internet via Firefox
        driver = webdriver.Firefox(options=options)
        driver.get('https://si3.ufc.br/sigaa/public/processo_seletivo/lista.jsf?aba=p-processo&nivel=S')

        # Obtém o título da página
        titulo_pagina = driver.title

        # Valida se o título esperado está presente
        if "SIGAA - Sistema Integrado de Gestão de Atividades Acadêmicas" in titulo_pagina:
            print("Página carregada com sucesso!")
        else:
            print("Erro ao carregar a página. Título incorreto.")

        colunas=['Agrupador', 'Titulo', 'Categoria', 'Vagas', 'Periodo']

        texto = driver.find_elements(By.CLASS_NAME, 'agrupador')

        # Lista para armazenar os dados
        dados = []

        # Iterar sobre os elementos "agrupador"
        for agrupador in texto:
            # Dados para salvar
            linha_dados = []

            # Adicione o texto do agrupador à lista de dados
            linha_dados.append(agrupador.text)

            # Encontre o próximo elemento "tr" (linha) após o agrupador e seleciona o td de cada
            dado_subsequente = agrupador.find_element(By.XPATH, './following::tr').find_elements(By.TAG_NAME, 'td')

            # Adicione o texto de cada coluna à lista de dados
            for coluna in dado_subsequente:
                if coluna.text != '' :
                    linha_dados.append(coluna.text)

            # Adicione a linha de dados à lista de dados
            dados.append(linha_dados)

        # Crie um DataFrame com os dados
        df = pd.DataFrame(dados, columns=colunas)

        # Dividir a coluna 'Período' em duas colunas: 'Início' e 'Fim'
        df[['Início', 'Fim']] = df['Periodo'].str.split('a', expand=True)

        # Remover espaços em branco extras
        df['Início'] = df['Início'].str.strip()
        df['Fim'] = df['Fim'].str.strip()

        # Converter DataFrame em JSON
        json_data = df.to_json(orient='records')

        # Configurações do servidor SMTP e credenciais de login que estão no env
        remetente = os.getenv('REMETENTE')
        remetente_nome = os.getenv('REMETENTE_NOME')
        senha = os.getenv('SENHA')
        destinatario = os.getenv('DESTINATARIO')
        servidor_smtp = os.getenv('SERVIDOR_SMTP')
        porta = os.getenv('PORTA')  # Porta para conexão TLS

        # Criar mensagem de e-mail
        msg = MIMEMultipart()
        msg['From'] = f'{remetente_nome} <{remetente}>'
        msg['To'] = destinatario
        msg['Subject'] = 'Novo mestrado encontrado'

        # Corpo do e-mail
        corpo = json_data
        msg.attach(MIMEText(corpo, 'plain'))

        # Iniciar conexão com o servidor SMTP
        server = smtplib.SMTP(servidor_smtp, porta)
        server.starttls()

        # Fazer login no servidor SMTP
        server.login(remetente, senha)

        # Enviar e-mail
        texto_email = msg.as_string()
        server.sendmail(remetente, destinatario, texto_email)

        # Fechar conexão com o servidor
        server.quit()

        print("E-mail enviado com sucesso!")
        return "Hello World!"

if __name__ == "__main__":
    app.run()

# [END ndb_flask]