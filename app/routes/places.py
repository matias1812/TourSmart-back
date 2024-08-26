from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.controllers.places_controller import fetch_all_places
from app.models.models import Place
from app.database import SessionLocal
from pydantic import BaseModel
from typing import Optional

class PlaceResponse(BaseModel):
    id: str
    name: str
    address: str
    latitude: float
    longitude: float
    place_type: str
    rating: Optional[float]  # Cambiado a Optional[float]
    is_fetched: bool

    class Config:
        orm_mode = True


router = APIRouter()

@router.get("/places", response_model=List[PlaceResponse])
async def get_places(
    latitude: str = Query(..., description="Latitude of the location"),
    longitude: str = Query(..., description="Longitude of the location"),
    type: str = Query(..., description="Type of place to search for, separated by '|'")
):
    db = SessionLocal()
    try:
        place_types = type.split('|')  # Convert the string to a list
        fetch_all_places(latitude, longitude, place_types, db)
        places_data = db.query(Place).filter(Place.place_type.in_(place_types)).all()
        
        if not places_data:
            raise HTTPException(status_code=404, detail="No places found")
        
        return places_data
    finally:
        db.close()
