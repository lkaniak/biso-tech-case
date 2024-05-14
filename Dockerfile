FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

WORKDIR /app/

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY pyproject.toml /app/

# instalar dev deps para os testes
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --only main ; fi"

RUN poetry self add poetry-dotenv-plugin

ENV PYTHONPATH=/app

COPY movie-app/scripts /app/scripts

COPY alembic.ini /app/

COPY movie-app/api /app/