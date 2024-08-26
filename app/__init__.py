from fastapi import FastAPI
from .routes import places
from .routes import guia
app = FastAPI()

app.include_router(places.router)
app.include_router(guia.router)

