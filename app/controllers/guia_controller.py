from sqlalchemy.orm import Session
from app.models.models import Place
from config import config
from openai import OpenAI

# Configura el cliente OpenAI
client = OpenAI(base_url=config.OPENAI_BASE_URL, api_key=config.OPENAI_API_KEY)

async def get_chat_response(
    messages: list,
    model: str = "lmstudio-community/Phi-3.1-mini-4k-instruct-GGUF",
    temperature: float = 0.7,
    stream: bool = True
) -> dict:
    try:
        system_message = {"role": "system", "content": "You are an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful."}
        messages.insert(0, system_message)
        
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            stream=stream
        )
        return completion.choices[0].message
    except Exception as e:
        return {"error": str(e)}

def generate_tour_route(user_request: str, user_lat: float, user_lng: float) -> list:
    # Crear una nueva sesión de base de datos
    db = Session()
    try:
        # Filtrar y ordenar los lugares basados en la solicitud del usuario
        query = db.query(Place).filter(Place.rating.isnot(None)).order_by(Place.rating.desc())
        
        # Implementar lógica para adaptar los lugares a la petición del usuario
        if "comida peruana" in user_request.lower():
            query = query.filter(Place.place_type == "restaurant")  # Filtrar solo restaurantes
        # Añadir más filtros según la solicitud del usuario
        
        top_places = query.limit(10).all()
        
        # Crear la ruta basada en los lugares seleccionados y la ubicación del usuario
        route = []
        for place in top_places:
            route.append({
                "name": place.name,
                "address": place.address,
                "rating": place.rating,
                "latitude": place.latitude,
                "longitude": place.longitude
            })
        
        # Aquí puedes incluir lógica adicional para ordenar los lugares en la ruta, 
        # como la distancia entre los puntos o la mejor ruta basada en la ubicación del usuario
        
        return route
    finally:
        db.close()
