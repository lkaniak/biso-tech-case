# Requerimentos

- [Docker](https://docs.docker.com/engine/install/) (virtualização)
- [Poetry](https://python-poetry.org/docs/#installation) (gerenciador de dependências)

# Ambiente dev

**OBS:** reiniciar o shell depois de instalar o Poetry!

1) instalar as deps do projeto, com o seguinte comando na pasta movie-app: ``poetry install``
  1.1) verificar no ``pyproject.toml`` a versão do tensorflow para instalar de acordo com o hardware no grupo ``[tool.poetry.group.tensorflow.dependencies]``
2) Plugin para o poetry reconhecer e inserir o .env: ``poetry self add poetry-dotenv-plugin``
3) Ativar o shell do poetry: ``poetry shell``
4) Migrations: ``alembic upgrade head``
5) Rodar a geração do modelo: ``movie-app/scripts/py/generate_model_f_eng.py``


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