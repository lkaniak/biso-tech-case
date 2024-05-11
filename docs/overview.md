# Estrutura de arquivos

```
├── Dockerfile                            # imagem do backend
├── alembic.ini
├── docker-compose.yaml                   # contem definicoes das imagens do backend e do postgreSQL
├── docs                                  # contem descrições sobre o projeto
│   ├── how-to.md
│   ├── overview.md
│   └── proposta.md
├── movie-app                             # pasta do app
│   ├── alembic                           # migrations
│   ├── lib                               # códigos reusáveis pelos 3 módulos (recommendation, src, test)
│   ├── recommendation                    # sistema de recomendação
│   ├── src                               # src da api
│   │   ├── core                          # domínio principal do app
│   │   │   └── v1                        # versionamento da api
│   │   │       ├── routes.py             # agregador das rotas do app
│   │   │       ├── auth    [...]         # subdomínio relacionado a auth
│   │   │       ├── movies  [...]         # subdomínio relacionado aos filmes
│   │   │       ├── ratings [...]         # subdomínio relacionado as avaliações
│   │   │       └── users                 # subdomínio relacionado aos usuarios
│   │   │           ├── deps.py           # dependencias do router (validações)
│   │   │           ├── exceptions.py     # exceções especificas do modulo
│   │   │           ├── models.py         # models do database
│   │   │           ├── router.py         # contém as rotas do modulo
│   │   │           ├── schemas.py        # models do pydantic
│   │   │           └── service.py        # business logic do model
│   │   ├── infrastructure                # configs do app (db, security, fastAPI, etc)
│   │   ├── lib                           # códigos reusáveis pelos módulos da api
│   │   └── main.py                       # arquivo de entrada do FastAPI
│   └── test                              # unit tests
├── pyproject.toml                        # definicao do env para o [Poetry](https://python-poetry.org/docs/pyproject/)
└── scripts                               # pasta auxiliar para scripts (parecido com a sessão scripts do package.json)
    ├── format.sh
    ├── lint.sh
    ├── prestart.sh
    ├── test.sh
    └── tests-start.sh
```
