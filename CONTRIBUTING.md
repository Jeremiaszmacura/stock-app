# Development Guide

## Package structure

Follows the `src` layout convention — source lives in `src/stock-app/`, tests in `tests/`.

Reference: https://www.pyopensci.org/python-package-guide/package-structure-code/python-package-structure.html

## Create a virtual environment

From the project root:

Unix

```sh
python3 -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell)

```sh
python3 -m venv .venv
Set-ExecutionPolicy Unrestricted -Scope Process
.venv\Scripts\activate
```

## Install dev dependencies

```sh
pip install -r requirements-dev.txt
```

## Start the database

```sh
docker compose up -d
```

## Run the app

```sh
uvicorn main:app --reload --app-dir src/stock-app
```

## API docs

Swagger UI

```text
http://127.0.0.1:8000/docs
```

ReDoc

```text
http://127.0.0.1:8000/redoc
```

OpenAPI schema

```text
http://127.0.0.1:8000/openapi.json
```

Mongo Express (DB browser)

```text
http://localhost:8081
```

## Run tests

```sh
pytest tests/ -v
```

## Run pre-commit hooks

```sh
pre-commit run -a
```
