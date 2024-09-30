FROM python:3.12-slim

ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app/

# Copiar os arquivos de dependência primeiro para aproveitar o cache de build
COPY pyproject.toml poetry.lock ./

RUN pip install poetry
RUN poetry config installer.max-workers 10 
RUN poetry install --no-interaction --no-ansi --no-dev

# Copiar o restante do código
COPY . .

RUN apt-get update && apt-get install -y postgresql-client

ENTRYPOINT ["/app/entrypoint.sh"]

EXPOSE 7000

# Comando para rodar a aplicação FastAPI
CMD ["uvicorn", "fast_zero.app:app", "--host", "0.0.0.0", "--port", "7000"]