from fastapi import APIRouter, HTTPException
from typing import List, Dict
from pydantic import BaseModel
from app.controllers.guia_controller import generate_tour_route

router = APIRouter()

class TourRouteRequest(BaseModel):
    user_request: str
    user_lat: float
    user_lng: float

@router.post("/tour-route", response_model=List[Dict[str, str]])
async def tour_route(request: TourRouteRequest):
    try:
        route = generate_tour_route(request.user_request, request.user_lat, request.user_lng)
        if not route:
            raise HTTPException(status_code=404, detail="No tour route found based on the request")
        return route
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
