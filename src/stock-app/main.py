"""Module contains Fastapi app instance with applied configurations and routes."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from config import settings
from routes import user, auth, stock_data

app = FastAPI()

origins = [
    settings.CLIENT_ORIGIN,
]

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(user.router, tags=["Users"], prefix="/users")
app.include_router(auth.router, tags=["Auth"], prefix="/auth")
app.include_router(stock_data.router, tags=["StockData"], prefix="/stock-data")


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("../favicon.png")


@app.get("/")
async def root():
    return {"message": "Hello World"}
