from sqlalchemy.orm import Session
from app.models.models import Place
from config import config
from google.auth.transport.requests import AuthorizedSession
from google.auth import load_credentials_from_file
from typing import List, Dict
import time  # Para manejar la espera entre solicitudes de página

# Configuración del cliente de Google Places API
credentials, _ = load_credentials_from_file(
    config.SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/cloud-platform']
)
authed_session = AuthorizedSession(credentials)

def fetch_places(lat: str, lng: str, place_types: List[str], page_token: str = '', existing_place_ids: set = set()) -> Dict:
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    params = {
        'location': f'{lat},{lng}',
        'radius': 400000,  # 40 km radius (ajustado para abarcar un área más manejable)
        'type': '|'.join(place_types),  # Join multiple types
        'key': config.GOOGLE_PLACES_API_KEY,
        'pagetoken': page_token,
        'keyword': 'restaurant|museum|park'  # Puedes ajustar los parámetros de búsqueda según sea necesario
    }
    
    response = authed_session.get(url, params=params)
    data = response.json()
    
    if response.status_code != 200:
        raise Exception(f"Google Places API error: {data.get('error_message', 'Unknown error')}")
    
    # Espera para permitir que el token de la siguiente página esté disponible
    if 'next_page_token' in data:
        time.sleep(2)  # Google recomienda esperar 2 segundos antes de usar el siguiente token

    # Filtrar lugares existentes en la base de datos
    filtered_results = [
        place for place in data.get('results', [])
        if place['place_id'] not in existing_place_ids
    ]
    
    return {
        'results': filtered_results,
        'next_page_token': data.get('next_page_token')
    }

def save_places(places_data, db: Session):
    for place in places_data:
        db_place = Place(
            id=place['place_id'],
            name=place.get('name'),
            address=place.get('vicinity'),
            latitude=place['geometry']['location']['lat'],
            longitude=place['geometry']['location']['lng'],
            place_type=place.get('types', [])[0] if place.get('types') else None,
            rating=place.get('rating'),
            is_fetched=False
        )
        db.add(db_place)
    db.commit()

def fetch_all_places(lat: str, lng: str, place_types: List[str], db: Session):
    page_token = ''
    
    # Fetch existing place IDs from the database
    existing_place_ids = {place.id for place in db.query(Place).all()}
    all_places = []
    
    while page_token is not None:
        data = fetch_places(lat, lng, place_types, page_token, existing_place_ids)
        new_places = data.get('results', [])
        all_places.extend(new_places)
        save_places(new_places, db)
        page_token = data.get('next_page_token')
    
    # Fetch all places from the database and merge with new ones
    existing_places = db.query(Place).all()
    return {
        'existing_places': existing_places,
        'new_places': all_places
    }
