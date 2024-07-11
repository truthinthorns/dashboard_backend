import requests
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, HTTPException


router = APIRouter(
    prefix="/weather",
    tags=["weather"],
)


def get_forecast_links(hourly: bool, coords: str):
    try:
        result = requests.get(f'https://api.weather.gov/points/{coords}').json()
        if hourly:
            return result["properties"]["forecastHourly"]
        else:
            return result["properties"]["forecast"]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")
    

@router.get('/hourly')
async def get_hourly_forecast(coords: str):
    try:
        link = get_forecast_links(True, coords)
        result = requests.get(link).json()
        new_result = jsonable_encoder(result['properties']['periods'])
        return new_result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")


@router.get('/weekly')
async def get_weekly_forecast(coords: str):
    try:
        link = get_forecast_links(False, coords)
        result = requests.get(link).json()
        new_result = jsonable_encoder(result['properties']['periods'])
        return new_result
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")