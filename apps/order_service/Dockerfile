ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim AS builder

# prepare poetry env
RUN pip install poetry && \
    poetry config virtualenvs.create false

# install dependencies
WORKDIR /app
COPY ../../pyproject.toml ../../poetry.lock* /
RUN poetry install --no-root

# run app
WORKDIR /app
COPY apps/order_service/app /app

ENTRYPOINT ["gunicorn"]
CMD ["main:app", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0"]
