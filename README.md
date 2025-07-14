# API Backend do Sistema NEPA – Faculdade Católica da Paraíba

Este repositório contém a API desenvolvida para o **NEPA (Núcleo de Extensão e Pesquisa Acadêmica)** da **Faculdade
Católica da Paraíba**.

A aplicação visa facilitar a gestão de projetos de extensão e pesquisa acadêmica, permitindo que
professores e alunos realizem todas as etapas de forma online — desde a visualização de editais e inscrições em
projetos, até o controle de frequência e envio de relatórios.

## Tecnologias e Dependências

A aplicação foi construída em **Python** utilizando o framework **Flask**, com as seguintes dependências e suas
integrações ao framework:

- [**Flask**](https://pypi.org/project/Flask/) – Framework principal
- [**Flask-JWT-Extended**](https://pypi.org/project/Flask-JWT-Extended/) – Autenticação com JWT
- [**Flask-SQLAlchemy**](https://pypi.org/project/Flask-SQLAlchemy/) – ORM para banco de dados relacional
- [**Flask-Migrate**](https://pypi.org/project/Flask-Migrate/) – Controle de versões do banco de dados
- [**Flask-CORS**](https://pypi.org/project/flask-cors/) – Suporte a CORS
- [**Flask-Smorest**](https://pypi.org/project/flask-smorest/) – Geração automática de documentação e rotas via API spec
- [**Flask-Argon2**](https://pypi.org/project/Flask-Argon2/) – Hash de senhas com segurança reforçada
- [**marshmallow**](https://pypi.org/project/marshmallow/) – Serialização e validação de dados
- [**gunicorn**](https://pypi.org/project/gunicorn/) – Servidor WSGI para produção
- [**pytest**](https://pypi.org/project/pytest/) – Testes automatizados
- [**psycopg3**](https://pypi.org/project/psycopg/) – Conector com PostgreSQL

## Ambientes de execução

A aplicação suporta três modos de execução, definidos pela variável de ambiente `FLASK_ENV`

### Development (`FLASK_ENV=development`)

- Modo com **debug ativo** e logs de SQL detalhados.
- Interface Swagger disponível para testes interativos da API.
- Permite **CORS aberto** (`CORS_ORIGINS=*`) para facilitar o desenvolvimento local.
- Conexão com banco de dados de desenvolvimento, definida por `DEVELOPMENT_DATABASE_URI`.

### Production (`FLASK_ENV=production`)

- Modo com **debug desativado** e propagação de exceções desligada.
- Interface Swagger **desativada** por padrão.
- **CORS restrito** via variável `CORS_ORIGINS`, que **deve ser configurada corretamente**.
- Conexão com banco de dados de produção, definida por `PRODUCTION_DATABASE_URI`.

### Testing (`FLASK_ENV=testing`)

- Modo usado para **testes automatizados**, com `TESTING=True`.
- Usa banco de dados isolado, definido por `TEST_DATABASE_URI`.
- CORS também liberado para testes (`CORS_ORIGINS=*`).

> [!WARNING]
> Todas as variáveis sensíveis devem ser definidas no arquivo `.env` localizado na raiz do projeto.
> A aplicação não inicia sem este arquivo.

## Incializando a API

> [!NOTE]
> Os passos a seguir assumem que você já possui um arquivo `.env` corretamente configurado

Siga os passos abaixo para configurar o ambiente de desenvolvimento local da aplicação:

1. Criação do ambiente virtual

    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows use: venv\Scripts\activate
    ```

2. Instalação das dependências

    ```bash
    pip install -r requirements.txt
    ```

3. Configuração do banco de dados

   Antes de iniciar o banco de dados, certifique-se de que `DEVELOPMENT_DATABASE_URI` e `FLASK_ENV` estão corretamente
   definidas. Em seguida, execute as migrações do banco:

    ```bash
    flask db upgrade
    ```

4. Rodar a API localmente

   Com o ambiente configurado e o banco atualizado, inicie a aplicação executando:

    ```bash
    flask run
    ```

   Por padrão, a documentação do Swagger estará disponível localmente em http://127.0.0.1:5000/swagger-ui
