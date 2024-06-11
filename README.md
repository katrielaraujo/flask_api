## Flask Sales Application

Este projeto é uma API RESTful desenvolvida em Python com o framework Flask para gerenciar vendas. Ele oferece endpoints para autenticação de usuários, gerenciamento de vendas (CRUD) e geração de relatórios em PDF.

### Tecnologias Utilizadas

* **Flask:** Framework web para desenvolvimento da API.
* **Flask-SQLAlchemy:** ORM para interação com o banco de dados SQLite.
* **Flask-Migrate:** Ferramenta para gerenciar migrações do banco de dados.
* **Flask-JWT-Extended:** Biblioteca para autenticação baseada em JWT (JSON Web Tokens).
* **ReportLab:** Biblioteca para geração de relatórios em PDF.
* **SQLite:** Banco de dados leve e embutido para armazenar os dados.

### Configuração e Execução

1. **Clone o repositório:**

   ```bash
   git clone [https://github.com/seu-usuario/flask-sales-app.git](https://github.com/katrielaraujo/flask_api.git)
   ```

2. **Crie um ambiente virtual:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate    # Windows
   ```

3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente:**

   * Crie um arquivo `.env` na raiz do projeto e defina as seguintes variáveis:
     ```
     FLASK_APP=run.py
     FLASK_ENV=development  # Ou production
     SECRET_KEY=sua_chave_secreta
     JWT_SECRET_KEY=sua_jwt_secreta
     ```

5. **Execute as migrações:**

   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

6. **Execute a aplicação:**

   ```bash
   flask run
   ```

### Endpoints

#### Autenticação

* **`POST /auth/register`:** Registra um novo usuário.
    * Campos: `email`, `password`
* **`POST /auth/login`:** Autentica um usuário e retorna um token JWT.
    * Campos: `email`, `password`

#### Vendas

* **`GET /sales`:** Lista todas as vendas (requer autenticação).
* **`POST /sales`:** Cria uma nova venda (requer autenticação).
    * Campos: `nome_cliente`, `produto`, `valor`, `data_venda`
* **`GET /sales/<id>`:** Retorna os detalhes de uma venda específica (requer autenticação).
* **`PUT /sales/<id>`:** Atualiza os detalhes de uma venda existente (requer autenticação).
* **`DELETE /sales/<id>`:** Exclui uma venda (requer autenticação).
* **`GET /sales/report`:** Gera um relatório em PDF das vendas em um intervalo de datas (requer autenticação).
    * Parâmetros de consulta: `start_date`, `end_date` (formato: YYYY-MM-DD)

### Escolhas Tecnológicas e Arquitetura

* **Flask:** Escolhido por sua simplicidade, flexibilidade e facilidade de uso.
* **SQLAlchemy:** ORM que facilita a interação com o banco de dados, tornando o código mais limpo e legível.
* **JWT:** Padrão de autenticação seguro e amplamente utilizado.
* **SQLite:** Banco de dados leve e adequado para projetos de pequeno e médio porte.

A arquitetura do projeto é baseada em uma estrutura MVC (Model-View-Controller), onde os modelos representam os dados, as views são responsáveis pela apresentação e os controllers lidam com a lógica de negócio.

### Próximos Passos

* Implementar testes unitários e de integração.
* Adicionar mais funcionalidades, como filtros de pesquisa e paginação.
* Melhorar a segurança, como adicionar validação de entrada e proteção contra ataques CSRF.
* Implementar um frontend para interagir com a API.

---
