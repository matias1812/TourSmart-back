from flask import Flask, jsonify, request
import google.auth
from google.auth.transport.requests import AuthorizedSession
import config

app = Flask(__name__)

# Configuración de autenticación
credentials, _ = google.auth.load_credentials_from_file(
    config.SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/cloud-platform']
)
authed_session = AuthorizedSession(credentials)

def fetch_places(lat, lng, place_type, page_token=''):
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    params = {
        'location': f'{lat},{lng}',
        'radius': 1000000,  # Cambié el radio a 10km por defecto
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

@app.route('/places', methods=['GET'])
def get_places():
    lat = request.args.get('latitude')
    lng = request.args.get('longitude')
    place_type = request.args.get('type')
    
    if not lat or not lng or not place_type:
        return jsonify({'error': 'Latitude, Longitude, and Type are required'}), 400

    places_data = []
    page_token = ''
    while True:
        data = fetch_places(lat, lng, place_type, page_token)
        places_data.extend(data.get('results', []))
        page_token = data.get('next_page_token')
        if not page_token:
            break

    return jsonify(places_data)

if __name__ == '__main__':
    app.run(debug=True)
