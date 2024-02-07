FROM python:3.11

WORKDIR /src

COPY ./requirements*.txt install.sh ./

RUN ./install.sh

COPY . .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
