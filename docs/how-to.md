# Requerimentos

- [Docker](https://docs.docker.com/engine/install/) (virtualização)
- [Poetry](https://python-poetry.org/docs/#installation) (gerenciador de dependências)

# Ambiente dev

**OBS:** reiniciar o shell depois de instalar o Poetry!

1) instalar as deps do projeto, com o seguinte comando na pasta movie-app: ``poetry install``
2) Plugin para o poetry reconhecer e inserir o .env: ``poetry self add poetry-dotenv-plugin``
3) Ativar o shell do poetry: ``poetry shell``
4) Migrations: ``alembic upgrade head``
5)


# Testes

1) criar um database na imagem do postgresql com o nome concatenando a variável de ambiente ``POSTGRES_DB`` com ``_test``. ex: ``my_db_test``