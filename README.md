## 💻 Projeto: Notificação de Mestrados na UFC com Web Scraping e Cloud Run

Este projeto demonstra como criar um sistema de web scraping para extrair informações sobre mestrados da UFC e enviá-las por e-mail, utilizando o Cloud Run do Google Cloud para implantação.

---

## 📁 Estrutura do Projeto

O projeto consiste nos seguintes arquivos:

* **main.py:** Arquivo principal com o código Python que realiza o web scraping, compara os dados obtidos com os dados salvos anteriormente, e envia um e-mail com as diferenças encontradas.
* **compara.py:** Arquivo com funções para comparar os dados extraídos com os dados armazenados em um banco de dados PostgreSQL.
* **Dockerfile:** Arquivo para construir a imagem Docker que será utilizada no Cloud Run.
* **secretmanager.py:** Arquivo com funções para acessar segredos do Secret Manager do Google Cloud.
* **cloudbuild.yaml:** Arquivo de configuração para o Cloud Build, que automatiza o processo de build, push e deploy da aplicação no Cloud Run.
* **requirements.txt:** Arquivo com as dependências do projeto.

---

## 🔨 Classes e Métodos

### main.py

* **Classe `Flask`:** Cria uma instância da aplicação Flask, que é utilizada para definir rotas e lidar com as requisições HTTP.
* **Método `index()`:** Este método é chamado quando uma requisição HTTP é feita para a rota `/`. Ele utiliza o Selenium para realizar o web scraping da página de mestrados da UFC, extraindo informações como título, categoria, vagas e período. Em seguida, compara os dados obtidos com os dados salvos anteriormente e envia um e-mail com as diferenças encontradas.
* **Método `page_not_found()`:** Método para lidar com erros 404 (página não encontrada).

### compara.py

* **Classe `JSONData`:** Define a estrutura da tabela no banco de dados para armazenar os dados extraídos em formato JSON.
* **Método `comparar_e_salvar_json()`:** Este método compara os dados extraídos com os dados armazenados no banco de dados e salva o novo JSON com os dados atualizados.

### secretmanager.py

* **Método `get_json_secret()`:** Este método recupera os segredos armazenados no Secret Manager do Google Cloud, como credenciais de banco de dados e informações de e-mail.

---

## ☁️ Cloud Run

O Cloud Run é um serviço do Google Cloud que permite implantar aplicações web em contêineres sem precisar gerenciar a infraestrutura subjacente. Neste projeto, o Cloud Build é utilizado para construir a imagem Docker, enviá-la para o Container Registry e implantá-la no Cloud Run.

---

## 📧 Notificação por E-mail

O projeto envia um e-mail com as diferenças encontradas entre os dados extraídos e os dados armazenados anteriormente. As informações de e-mail, como remetente, destinatário e senha, são armazenadas no Secret Manager do Google Cloud por questões de segurança.

---

## 🛠️ Tecnologias Utilizadas

* Python
* Flask
* Selenium
* pandas
* SQLAlchemy
* psycopg2-binary
* Docker
* Google Cloud Secret Manager
* Google Cloud Build
* Google Cloud Run

---

## 💡 Próximos Passos

* Implementar um agendamento para que o web scraping seja executado automaticamente em intervalos regulares.
* Adicionar mais funcionalidades, como a possibilidade de filtrar os mestrados por área de interesse.
* Melhorar a interface do usuário para permitir que os usuários configurem as notificações de e-mail.


---

**Observação:** Este projeto é apenas um exemplo de como criar um web scraping e implantá-lo no Cloud Run. Adapte o código e as configurações de acordo com suas necessidades.