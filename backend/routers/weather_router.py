import requests
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, HTTPException
from datetime import datetime, date, timedelta


router = APIRouter(
    prefix="/weather",
    tags=["weather"],
)


def hourly_forecast_formatter(coords: str):
    try:
        result = requests.get(f'https://api.weather.gov/points/{coords}').json()
        hourly = requests.get(result["properties"]["forecastHourly"]).json()
        hourly_json = jsonable_encoder(hourly['properties']['periods'])
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred when getting the hourly forecast: {str(e)}")
    
    try:
        # 39.77,-84.0823
        new_hourly = []
        for hour in hourly_json:
            new_hourly.append({
                "temperature": f"{hour['temperature']}° F",
                "icon": hour['icon'],
                "windSpeed": hour['windSpeed'],
                "windDirection": hour['windDirection'],
                "chanceOfRain": f"{day['probabilityOfPrecipitation']['value'] if day['probabilityOfPrecipitation']['value'] else 0}%",
                "humidity": f"{day['relativeHumidity']['value']}%"
            })
        return hourly_json
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred when formatting the hourly forecast: {str(e)}")
    

def weekly_forecast_formatter(coords: str):
    try:
        result = requests.get(f'https://api.weather.gov/points/{coords}').json()
        hourly = requests.get(result["properties"]["forecast"]).json()
        weekly_json = jsonable_encoder(hourly['properties']['periods'])
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred when getting the weekly forecast: {str(e)}")
    
    try:
        new_weekly = []
        for day in weekly_json:
            temp_dt = datetime.fromisoformat(day['startTime'])
            today = date.today()
            # if it's not today's date.
            if temp_dt.day != today.day:
                new_weekly.append({
                    "name": day['name'],
                    "temperature": f"{day['temperature']}° F",
                    "icon": day['icon'].replace('medium','large'),
                    "windSpeed": day['windSpeed'],
                    "windDirection": day['windDirection'],
                    "detailedForecast": day['detailedForecast'],
                    "chanceOfRain": f"{day['probabilityOfPrecipitation']['value'] if day['probabilityOfPrecipitation']['value'] else 0}%"
                })
            # it's today's date, and it's before 6pm, and the forecast is for 6pm and later
            elif temp_dt.day == today.day:
                if datetime.now().hour < 18 and temp_dt.hour >= 18:
                    new_weekly.append({
                        "name": day['name'],
                        "temperature": f"{day['temperature']}° F",
                        "icon": day['icon'].replace('medium','large'),
                        "windSpeed": day['windSpeed'],
                        "windDirection": day['windDirection'],
                        "detailedForecast": day['detailedForecast'],
                        "chanceOfRain": f"{day['probabilityOfPrecipitation']['value'] if day['probabilityOfPrecipitation']['value'] else 0}%"
                    })
        return new_weekly
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred when formatting the weekly forecast: {str(e)}")
    

@router.get('/hourly')
async def get_hourly_forecast(coords: str):
    try:
        return hourly_forecast_formatter(coords)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")


@router.get('/weekly')
async def get_weekly_forecast(coords: str):
    try:
        return weekly_forecast_formatter(coords)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")