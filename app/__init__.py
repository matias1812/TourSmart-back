from fastapi import FastAPI
from .config import config
from .routes import places

app = FastAPI()

app.include_router(places.router)

