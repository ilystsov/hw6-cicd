FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /opt/app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./
COPY server/ ./server/
COPY tests/ ./tests/

RUN poetry config virtualenvs.create false \
    && poetry install   

EXPOSE 8000

CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
