import requests
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, HTTPException, Query
from models.weather import Weather
from datetime import datetime
from typing import List


router = APIRouter(
    prefix="/weather",
    tags=["weather"],
)


def hourly_forecast_formatter(coords: str):
    print(coords)
    try:
        result = requests.get(f"https://api.weather.gov/points/{coords}").json()
        hourly = requests.get(result["properties"]["forecastHourly"]).json()
        hourly_json = jsonable_encoder(hourly["properties"]["periods"])
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"An error occurred when getting the hourly forecast: {str(e)}",
        )

    try:
        # 39.668941,-84.106102
        new_hourly = []
        for hour in hourly_json:
            hourly_dict = dict(hour)
            new_hourly.append(
                Weather(
                    number=hourly_dict.get("number"),
                    start_time=datetime.fromisoformat(hourly_dict.get("startTime")),
                    end_time=datetime.fromisoformat(hourly_dict.get("endTime")),
                    temperature=hourly_dict.get("temperature"),
                    icon=hourly_dict.get("icon"),
                    wind_speed=hourly_dict.get("windSpeed"),
                    wind_direction=hourly_dict.get("windDirection"),
                    chance_of_rain=hourly_dict.get("probabilityOfPrecipitation").get(
                        "value", 0
                    ),
                    humidity=hourly_dict.get("relativeHumidity").get("value", 0),
                    dewpoint=int(hourly_dict.get("dewpoint").get("value", 0)),
                    short_forecast=hourly_dict.get("shortForecast"),
                )
            )
        return new_hourly
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"An error occurred when formatting the hourly forecast: {str(e)}",
        )


@router.get(
    path="/hourly",
    summary="Get hourly forecast",
    description="This endpoint returns the hourly forecast for the coordinates provided.",
    response_model=List[Weather],
    status_code=200,
)
async def get_hourly_forecast(coords: str = Query(
    example="40.7128,-74.006",
    description="The coordinates with no spaces and N first, followed by W. You might need to include - before the second point if west of the Prime Meridian!",

)):
    try:
        return hourly_forecast_formatter(coords.replace(" ", ""))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")
