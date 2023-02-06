"""Module contains Fastapi app instance with applied configurations and routes."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes import user, auth

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


@app.get("/")
async def root():
    return {"message": "Hello World"}
