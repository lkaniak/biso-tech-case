# Requisitos

- [Docker](https://docs.docker.com/engine/install/) (virtualização)
- [Poetry](https://python-poetry.org/docs/#installation) (gerenciador de dependências)

# Ambiente dev

## máquina local

**OBS:** reiniciar o shell depois de instalar o Poetry!

1) instalar as deps do projeto, com o seguinte comando na pasta movie-app: ``poetry install``
  1.1) verificar no ``pyproject.toml`` a versão do tensorflow para instalar de acordo com o hardware no grupo ``[tool.poetry.group.tensorflow.dependencies]``
2) rodar o postgres no docker ou local, configurando no `.env` as variáveis
3) Plugin para o poetry reconhecer e inserir o .env: ``poetry self add poetry-dotenv-plugin``
4) Ativar o shell do poetry: ``poetry shell``
5) Migrations (rodar na pasta raiz do projeto): ``alembic upgrade head``
6) rodar a geração dos dados ``initial_data.py`` (pode rodar ele múltiplas veses para gerar mais ratings)
7) Rodar a geração do modelo: ``movie-app/scripts/py/generate_model_f_eng.py``
8) Rodar a api na pasta ``movie-app/api``: ``uvicorn --reload main:app --port $PORT``
9) Docs disponíveis em ``localhost:$PORT/docs ou localhost:$PORT/redoc``
10) primeiro user de teste (criado no passo 6) nas variáveis ``EMAIL_FIRST_SUPERUSER`` e ``FIRST_SUPERUSER_PASSWORD``


## Testes

**OBS:** é possível (mas não obrigatório) configurar os parâmetros do user de teste setando as variáveis:

```
EMAIL_TEST_USER
FIRST_SUPERUSER
FIRST_SUPERUSER_PASSWORD
```

1) seguir as etapas para setar a shell do poetry
2) criar um database na imagem do postgresql com o nome concatenando a variável de ambiente ``POSTGRES_DB``
com ``_test``. ex: ``my_db_test``
3) setar a variável ``ENVIRONMENT`` para ``staging``
4) rodar na pasta movie-app ``coverage run --source src -m pytest``