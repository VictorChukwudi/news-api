from fastapi import FastAPI
from .core.config import settings
from .db.database import Base, engine
from .routers import auth
from .models import user_model

app = FastAPI()

# Base.metadata.create_all(bind=engine)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)

@app.get("/")
async def read_root():
    return "News API is running!"


@app.get("/config")
async def get_config():
    return {
        "database_url": settings.database_url,
        "message": "Configuration loaded successfully!"
    }
