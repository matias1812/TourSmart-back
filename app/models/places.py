from sqlalchemy import create_engine, Column, String, Float, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import config

# Configuración de la base de datos
Base = declarative_base()

class Place(Base):
    __tablename__ = 'places'
    
    id = Column(String(36), primary_key=True)  # Usar UUID para el ID
    name = Column(String(255), nullable=False)
    address = Column(Text)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    place_type = Column(String(50))
    rating = Column(Float)
    is_fetched = Column(Boolean, default=False)  # Para marcar si el lugar ya ha sido obtenido

# Configuración de la base de datos
DATABASE_URL = config.SQLALCHEMY_DATABASE_URI
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
