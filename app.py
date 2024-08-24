from fastapi import FastAPI, HTTPException, Query
from typing import List
import google.auth
from google.auth.transport.requests import AuthorizedSession
import config

app = FastAPI()

# Configuración de autenticación
credentials, _ = google.auth.load_credentials_from_file(
    config.SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/cloud-platform']
)
authed_session = AuthorizedSession(credentials)

def fetch_places(lat: str, lng: str, place_type: str, page_token: str = '') -> dict:
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    params = {
        'location': f'{lat},{lng}',
        'radius': 10000,  # Cambié el radio a 10km por defecto
        'type': place_type,
        'key': config.GOOGLE_PLACES_API_KEY,
        'pagetoken': page_token
    }
    print(f"Fetching places with params: {params}")  # Debugging line
    response = authed_session.get(url, params=params)
    if response.status_code == 200:
        print(f"Response JSON: {response.json()}")  # Debugging line
    else:
        print(f"Error fetching data: {response.status_code}, {response.text}")  # Debugging line
    return response.json()

@app.get("/places", response_model=List[dict])
async def get_places(
    latitude: str = Query(..., description="Latitude of the location"),
    longitude: str = Query(..., description="Longitude of the location"),
    place_type: str = Query(..., description="Type of place to search for")
):
    places_data = []
    page_token = ''
    while True:
        data = fetch_places(latitude, longitude, place_type, page_token)
        places_data.extend(data.get('results', []))
        page_token = data.get('next_page_token')
        if not page_token:
            break

    if not places_data:
        raise HTTPException(status_code=404, detail="No places found")

    return places_data

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
