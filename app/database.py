from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import config

# Configuración de la base de datos
DATABASE_URL = config.SQLALCHEMY_DATABASE_URI
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
