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