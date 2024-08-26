from fastapi import FastAPI
from app.routes import places, guia

app = FastAPI()

app.include_router(places.router)
app.include_router(guia.router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
