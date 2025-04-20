from pydantic import BaseModel, Field
from datetime import datetime, timedelta


class Weather(BaseModel):
    number: int = Field(default=1, ge=1)
    start_time: datetime = Field(default=datetime.now())
    end_time: datetime = Field(default=datetime.now()+timedelta(days=1))
    temperature: int = Field(default=65, ge=-40, le=140)
    icon: str = Field(default="https://api.weather.gov/icons/land/night/bkn?size=small")
    wind_speed: str = Field(default="15 mph")
    wind_direction: str = Field(default="E", max_length=3)
    chance_of_rain: int = Field(default=85, ge=0, le=100)
    humidity: int = Field(default=10, ge=0, le=100)
    dewpoint: int = Field(default=50, ge=-40, le=140)
    short_forecast: str = Field(default="Cloudy with a chance")