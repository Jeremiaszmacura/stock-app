# Stock Data Analysis

FastAPI application that fetches stock data from Alpha Vantage, calculates risk metrics, and generates charts.

## Features

- Stock price charts — linear and candlestick (intraday, daily, weekly, monthly)
- Value at Risk (VaR) — historical simulation, linear model, Monte Carlo
- Hurst exponent — market efficiency / autocorrelation analysis
- Portfolio VaR — multi-symbol risk aggregation
- Company search via Alpha Vantage symbol search
- JWT authentication with user management

## Tech stack

| Layer | Technology |
|---|---|
| API | FastAPI, Python 3.14 |
| Database | MongoDB 8.0, Motor (async driver) |
| Data | Pandas, NumPy, SciPy, statsmodels |
| Charts | Matplotlib |
| Market data | Alpha Vantage |
| Auth | python-jose (JWT), passlib (bcrypt) |
| Infra | Docker, Docker Compose |

## Requirements

- Python 3.13+
- Docker & Docker Compose
- Alpha Vantage API key (free tier available)

## Quick start

**1. Clone and configure**

```sh
git clone <repo-url>
cd stock-app
cp .env.example .env  # fill in your values
```

Required `.env` variables:

```env
DATABASE_URL=mongodb://root:password@localhost:27017
MONGO_INITDB_DATABASE=stock_db
MONGO_INITDB_ROOT_USERNAME=root
MONGO_INITDB_ROOT_PASSWORD=password
ME_CONFIG_MONGODB_ADMINUSERNAME=root
ME_CONFIG_MONGODB_ADMINPASSWORD=password
DATABASE_URL_FOR_EXPRESS=mongodb://root:password@mongodb:27017
SECRET_KEY=<random-secret>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CLIENT_ORIGIN=http://localhost:3000
ALPHA_VANTAGE_API_KEY=<your-key>
```

**2. Start the database**

```sh
docker compose up -d
```

**3. Create virtual environment and install dependencies**

```sh
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
```

**4. Run the API**

```sh
uvicorn main:app --reload --app-dir src/stock-app
```

## API docs

| URL | Description |
|---|---|
| http://127.0.0.1:8000/docs | Swagger UI |
| http://127.0.0.1:8000/redoc | ReDoc |
| http://127.0.0.1:8000/openapi.json | OpenAPI schema |
| http://localhost:8081 | Mongo Express (DB browser) |

## API overview

| Method | Path | Description |
|---|---|---|
| `POST` | `/auth/token` | Login → JWT token |
| `GET` | `/users` | List users |
| `POST` | `/users` | Register user |
| `PUT` | `/users/{id}` | Update user |
| `DELETE` | `/users/{id}` | Delete user |
| `POST` | `/stock-data` | Fetch stock data + calculate VaR/Hurst |
| `POST` | `/stock-data/portfolio-var` | Portfolio-level VaR |
| `GET` | `/stock-data/search` | Search companies by symbol |

## Running tests

```sh
pytest tests/ -v
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
