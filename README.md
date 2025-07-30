# API Backend do Sistema NEPA – Faculdade Católica da Paraíba

Este repositório contém a API desenvolvida para o **NEPA (Núcleo de Extensão e Pesquisa Acadêmica)**
da **Faculdade Católica da Paraíba**.

A aplicação visa facilitar a gestão de projetos de extensão e pesquisa acadêmica,
permitindo que professores e alunos realizem todas as etapas de forma online
— desde a visualização de editais e inscrições em projetos, até o controle de frequência e envio de relatórios.

## Conteúdos

- [Tecnologias e Dependências](#tecnologias-e-dependências)
- [Ambientes de execução](#ambientes-de-execução)
    - [Desenvolvimento](#desenvolvimento-development)
    - [Produção](#produção-production)
    - [Testes](#testes-testing)
- [Incializando a API localmente](#incializando-a-api-localmente)
- [Deploy no Servidor](#deploy-no-servidor)
    - [Configuração do Gunicorn](#configuração-do-gunicorn)
    - [Arquivo de serviço](#arquivo-de-serviço-systemd)

## Tecnologias e Dependências

A aplicação foi construída com **Python3.12** utilizando o framework **Flask**, com as seguintes dependências e suas
integrações ao framework:

- [**Flask**](https://pypi.org/project/Flask/) – Framework principal
- [**Flask-JWT-Extended**](https://pypi.org/project/Flask-JWT-Extended/) – Autenticação com tokens JWT
- [**Flask-SQLAlchemy**](https://pypi.org/project/Flask-SQLAlchemy/) – ORM para integração com banco de dados relacional
- [**Flask-Migrate**](https://pypi.org/project/Flask-Migrate/) – Migrações e controle de versão do banco de dados
- [**Flask-CORS**](https://pypi.org/project/flask-cors/) – Suporte a CORS
- [**Flask-Smorest**](https://pypi.org/project/flask-smorest/) – Suporte a validação e documentação automática de rotas
- [**Flask-Argon2**](https://pypi.org/project/Flask-Argon2/) – Hashing de senhas com Argon2
- [**Marshmallow**](https://pypi.org/project/marshmallow/) – Serialização, desserialização e validação de dados
- [**Gunicorn**](https://pypi.org/project/gunicorn/) – Servidor WSGI usado em ambientes de produção
- [**Pytest**](https://pypi.org/project/pytest/) – Framework de testes automatizados
- [**Flask-Pytest**](https://pypi.org/project/pytest/) – Fornece fixtures úteis para testes
- [**psycopg3**](https://pypi.org/project/psycopg/) – Conector para bancos de dados PostgreSQL

## Ambientes de execução

A aplicação suporta três modos de execução, configuráveis via variável de ambiente FLASK_ENV ou diretamente pelo
parâmetro env em create_app() — neste caso, o valor passado como parâmetro tem precedência.

### Desenvolvimento (`development`)

- Modo com debug ativo e logs de SQL detalhados.
- Interface Swagger disponível para testes interativos da API.
- CORS aberto para facilitar o desenvolvimento local.
- Conexão com banco de dados de desenvolvimento, definida por `DEVELOPMENT_DATABASE_URI`.

### Produção (`production`)

- Ambiente padrão na criação do app em `wsgi.py`
- Modo com debug desativado e propagação de exceções desligada.
- Interface Swagger desativada por padrão.
- CORS restrito via variável `CORS_ORIGINS`, que **deve ser configurada corretamente**.
- Conexão com banco de dados local de produção, definida por `PRODUCTION_DATABASE_URI`.

### Testes (`testing`)

- Modo usado para testes automatizados.
- CORS também liberado para testes.
- Conexão com banco de dados isolado, definido por `TEST_DATABASE_URI`.

## Incializando a API localmente

> [!WARNING]
> Todas as variáveis sensíveis devem ser definidas no arquivo `.env` localizado na raiz do projeto.
> (exemplo [.env.template](.env.template) fornecido no repositório)

Siga os passos abaixo para configurar o ambiente de desenvolvimento local da aplicação:

1. Criar ambiente virtual

    ```bash
    python3 -m venv .venv # No Windows use: python -m venv .venv
    source .venv/bin/activate  # No Windows use: .venv\Scripts\activate
    ```

2. Instalação das dependências

    ```bash
    pip install -r requirements.txt
    ```

3. Configuração do banco de dados

   Antes de iniciar as migrações o banco de dados, certifique-se de que `DEVELOPMENT_DATABASE_URI` e `FLASK_ENV` estão
   corretamente definidas. Em seguida, execute as migrações do banco:

    ```bash
    flask db upgrade
    ```

4. Executar a API localmente

   Com o ambiente configurado e o banco atualizado, inicie a aplicação executando:

    ```bash
    flask run
    ```

   Por padrão, a documentação do Swagger estará disponível localmente em http://127.0.0.1:5000/swagger-ui
   no ambiente de desenvolvimento.

## Deploy no Servidor

Este passo-a-passo assume que você já possui o código da API no servidor Debian/Ubuntu em /home/nepa/NEPA-api
e que o usuário nepa existe.

1. Criar ambiente virtual e instalar dependências

    ```bash
    cd /home/nepa/NEPA-api
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

2. Configurar variáveis de ambiente

   Crie um arquivo .env na raiz do projeto com todas as variáveis necessárias
   (exemplo [.env.template](.env.template) fornecido no repositório).

   ```bash
   touch .env
   ```

3. Aplicar migrações do banco de dados

   ```bash
   flask db upgrade
   ```

4. Ativar e iniciar o serviço

   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start nepa-api
   ```

5. Verificar status e logs

   ```bash
   sudo systemctl status nepa-api
   sudo journalctl -u nepa-api -f
   ```

### Configuração do Gunicorn

A configuração do Gunicorn utilizada pelo serviço encontra-se no arquivo [`gunicorn.conf.py`](./gunicorn.conf.py),
localizado na raiz do projeto.
O gunicorn é iniciado automaticamente com essa configuração, desde que seja executado na
raiz do diretório onde o arquivo está localizado.

### Arquivo de serviço systemd

O serviço `nepa-api`, localizado em `/etc/systemd/system/nepa-api.service`, contém o seguinte:

```unit file (systemd)
[Unit]
Description=NEPA Flask API
After=network.target

[Service]
User=nepa
Group=www-data
WorkingDirectory=/home/nepa/NEPA-api
Environment="PATH=/home/nepa/NEPA-api/.venv/bin"
ExecStart=/home/nepa/NEPA-api/.venv/bin/gunicorn

ProtectSystem=full
Restart=always

StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```