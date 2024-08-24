from google.auth.transport.requests import AuthorizedSession
from google.auth import load_credentials_from_file
from app.config import config

credentials, _ = load_credentials_from_file(
    config.SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/cloud-platform']
)
authed_session = AuthorizedSession(credentials)

def fetch_places(lat: str, lng: str, place_type: str, page_token: str = '') -> dict:
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    params = {
        'location': f'{lat},{lng}',
        'radius': 400000,  # 10km radius
        'type': place_type,
        'key': config.GOOGLE_PLACES_API_KEY,
        'pagetoken': page_token
    }
    response = authed_session.get(url, params=params)
    return response.json()
