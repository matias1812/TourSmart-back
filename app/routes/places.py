from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.controllers.places_controller import fetch_places

router = APIRouter()

@router.get("/places", response_model=List[dict])
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
