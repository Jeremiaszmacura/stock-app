from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from routes import user

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


@app.get("/")
async def root():
    return {"message": "Hello World"}
