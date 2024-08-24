from pydantic import BaseSettings
import os

class Config(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str = 'mysql+pymysql://matiast:agustina1812@localhost/inventario_db'
    JWT_SECRET_KEY: str = 'f7c5e9d7d36b2e2d6c0e9b8e1c3d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9g0h1i2j'  # Cambia esto en producción
    UPLOAD_FOLDER: str = 'uploads'
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SERVICE_ACCOUNT_FILE: str = os.getenv('SERVICE_ACCOUNT_FILE', '/Users/matiast./Desktop/portafolio/TourSmart-back/tourtsmart-203cd67769dc.json')
    GOOGLE_PLACES_API_KEY: str = os.getenv('GOOGLE_PLACES_API_KEY', 'AIzaSyBTkA0w4OOz3tWOuaEYG6_0buHVq1QXf4Y')
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY', 'lm-studio')
    OPENAI_BASE_URL: str = os.getenv('OPENAI_BASE_URL', 'http://localhost:1234/v1')
config = Config()
