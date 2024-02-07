# Development Guide

## Package

Package structure follows convetion introduced in following doc:
https://www.pyopensci.org/python-package-guide/package-structure-code/python-package-structure.html

## Create python virutal enviroment

```sh
cd backend
```

Unix

```sh
python -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell)

```sh
python -m venv .venv
Set-ExecutionPolicy Unrestricted -Scope Process
.venv\Scripts\activate
```

## Install DEV dependecies

```sh
python -m pip install -r requirements-dev.txt
```

## Start database

```sh
docker-compose up
```

## Run backend app

```sh
uvicorn main:app --reload
```

## Api docs

Swagger UI

```text
http://127.0.0.1:8000/docs
```

ReDoc

```text
http://127.0.0.1:8000/redoc
```

## OpenAPI schema

```text
http://127.0.0.1:8000/openapi.json
```

## Mongo-express

```text
localhost:8081
```

## Run pre-commit

```sh
pre-commit run -a
```

App is avaiable under URL:

```text
http://127.0.0.1/:80
```
