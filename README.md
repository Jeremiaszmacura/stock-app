<hr />

### Create python virutal enviroment

<hr />

Create and active virtual enviroment using venv library:

```sh
python3 -m venv .venv
source .venv/bin/activate (Linux)
.venv\Scripts\activate (Windows)
```

In some Windows cases before activating venv:

```sh
Set-ExecutionPolicy Unrestricted -Scope Process
```

<hr />

### Install dependecies

<hr />

```sh
python -m pip install -r requirements.txt
```

<hr />

### Start database

<hr />

```sh
docker-compose up
```

<hr />

### Run app

<hr />

```sh
uvicorn main:app --reload
```

<hr />

### Api docs

<hr />

Swagger UI

```text
http://127.0.0.1:8000/docs
```

ReDoc

```text
http://127.0.0.1:8000/redoc
```

<hr />

### OpenAPI schema

<hr />

```text
http://127.0.0.1:8000/openapi.json
```

<hr />

### Run linters

<hr />

Pylint

```sh
python -m pylint backend
```

Black check

```sh
python -m black --check backend
```

Black fix

```sh
python -m black backend
```

<hr />

Dockerfile backend

<hr />

Build backend app

```sh
docker build -t stock_backend -f backend.dockerfile .
```

Run backend app

```sh
docker run -d --name stock_backend -p 80:80 stock_backend
```

App is avaiable under URL:

```text
http://127.0.0.1/:80
```