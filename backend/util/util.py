import requests
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
from backend.models.weather import Weather
from backend.models.user import MongoUser as User
from backend.models.todo import Todo
from datetime import datetime
from beanie import PydanticObjectId


def hourly_forecast_formatter(coords: str):
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
        # return only the next 48 hours
        for hour in hourly_json:
            hourly_dict = dict(hour)
            # for some reason, dewpoint is in Celsius, so convert to Fahrenheit
            dewpoint = hourly_dict.get("dewpoint").get("value", None)
            if dewpoint:
                dewpoint = int((int(dewpoint) * (9 / 5)) + 32)
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
                        "value", None
                    ),
                    humidity=hourly_dict.get("relativeHumidity").get("value", None),
                    dewpoint=dewpoint,
                    short_forecast=hourly_dict.get("shortForecast"),
                )
            )
        return new_hourly
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"An error occurred when formatting the hourly forecast: {str(e)}",
        )


async def get_user(id: PydanticObjectId) -> User:
    try:
        user = await User.get(id)
        if user == None:
            raise HTTPException(status_code=404, detail="No user found with that id!")
        return user
    except Exception as e:
        raise e


async def get_todo(id: PydanticObjectId) -> Todo:
    try:
        todo = await Todo.get(id)
        if todo == None:
            raise HTTPException(status_code=404, detail="No todo found with that id!")
        return todo
    except Exception as e:
        raise e
