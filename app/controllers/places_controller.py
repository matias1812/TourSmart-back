from sqlalchemy.orm import Session
from app.models.places import Place
from app.config import config
from google.auth.transport.requests import AuthorizedSession
from google.auth import load_credentials_from_file

# Configuración del cliente de Google Places API
credentials, _ = load_credentials_from_file(
    config.SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/cloud-platform']
)
authed_session = AuthorizedSession(credentials)

def fetch_places(lat: str, lng: str, place_type: str, db: Session, page_token: str = '') -> dict:
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    params = {
        'location': f'{lat},{lng}',
        'radius': 400000,  # 10km radius
        'type': place_type,
        'key': config.GOOGLE_PLACES_API_KEY,
        'pagetoken': page_token
    }
    response = authed_session.get(url, params=params)
    data = response.json()

    # Guardar lugares en la base de datos
    save_places(data.get('results', []), db)

    return data

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
        db.merge(db_place)  # Use merge to avoid duplicates
    db.commit()
