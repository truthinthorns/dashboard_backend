from fastapi import APIRouter, HTTPException, Query
from backend.models.weather import Weather
from backend.util.util import hourly_forecast_formatter


router = APIRouter(
    prefix="/weather",
    tags=["Weather"],
)


@router.get(
    path="/hourly",
    summary="Get hourly forecast",
    description="This endpoint returns the hourly forecast for the coordinates provided.",
    response_model=list[Weather],
    status_code=200,
)
async def get_hourly_forecast(
    coords: str = Query(
        example="40.7128,-74.006",
        description="The coordinates with no spaces and N first, followed by W. You might need to include - before the second point if west of the Prime Meridian!",
    )
):
    try:
        return hourly_forecast_formatter(coords.replace(" ", ""))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")
