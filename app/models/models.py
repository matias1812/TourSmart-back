import uuid
from sqlalchemy import create_engine, Column, String, Float, Boolean, Text, ForeignKey, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from config import config

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = 'users'
    
    id = Column(String(36), primary_key=True, default=generate_uuid)  # UUID
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now)

class Route(Base):
    __tablename__ = 'routes'
    
    id = Column(String(36), primary_key=True, default=generate_uuid)  # UUID
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=func.now)
    polyline = Column(Text, nullable=False)  # Ruta de Google Maps en formato codificado

    user = relationship("User", back_populates="routes")

class RouteDay(Base):
    __tablename__ = 'route_days'
    
    id = Column(String(36), primary_key=True, default=generate_uuid)  # UUID
    route_id = Column(String(36), ForeignKey('routes.id'), nullable=False)
    day_number = Column(Integer, nullable=False)
    place_id = Column(String(36), ForeignKey('places.id'))
    description = Column(Text)
    polyline = Column(Text, nullable=False)  # Ruta de Google Maps para cada día

    route = relationship("Route", back_populates="route_days")
    place = relationship("Place")

class Place(Base):
    __tablename__ = 'places'
    
    id = Column(String(36), primary_key=True, default=generate_uuid)  # UUID
    name = Column(String(255), nullable=False)
    address = Column(Text)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    place_type = Column(String(50))  # Ejemplo: 'restaurant', 'museum', etc.
    rating = Column(Float)
    is_fetched = Column(Boolean, default=False)  # Para marcar si el lugar ya ha sido obtenido

class AssistantMessage(Base):
    __tablename__ = 'assistant_messages'
    
    id = Column(String(36), primary_key=True, default=generate_uuid)  # UUID
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now)

    user = relationship("User", back_populates="assistant_messages")

class UserPreference(Base):
    __tablename__ = 'user_preferences'
    
    id = Column(String(36), primary_key=True, default=generate_uuid)  # UUID
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    preference_type = Column(String(50), nullable=False)  # Ejemplo: 'restaurant', 'museum', etc.
    value = Column(String(50), nullable=False)

    user = relationship("User", back_populates="preferences")

# Relaciones inversas
User.routes = relationship("Route", order_by=Route.id, back_populates="user")
User.assistant_messages = relationship("AssistantMessage", order_by=AssistantMessage.id, back_populates="user")
User.preferences = relationship("UserPreference", order_by=UserPreference.id, back_populates="user")
Route.route_days = relationship("RouteDay", order_by=RouteDay.day_number, back_populates="route")

# Configuración de la base de datos
DATABASE_URL = config.SQLALCHEMY_DATABASE_URI  # Reemplaza con tu configuración real
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
