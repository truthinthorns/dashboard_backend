from pydantic import BaseModel, Field
from datetime import datetime, timedelta


class Weather(BaseModel):
    number: int = Field(default=1, description="The number of the forecast from the response.", ge=1)
    start_time: datetime = Field(default=datetime.now(), description="The datetime for which this forecast is start being applicable")
    end_time: datetime = Field(default=datetime.now()+timedelta(days=1), description="The datetime for which this forecast is no longer applicable")
    temperature: int = Field(default=65, description="The temperature in Fahrenheit",ge=-40, le=140)
    icon: str = Field(default="https://api.weather.gov/icons/land/night/bkn?size=small", description="A link to an icon representing the weather conditions")
    wind_speed: str = Field(default="15 mph", description="The wind speed along with mph")
    wind_direction: str = Field(default="E", description="The direction the wind is blowing",max_length=3)
    chance_of_rain: int = Field(default=85, description="The percentage for chance of rain", ge=0, le=100)
    humidity: int = Field(default=10, description="The percentage for humidity", ge=0, le=100)
    dewpoint: int = Field(default=50, description="The dewpoint in Fahrenheit", ge=-40, le=140)
    short_forecast: str = Field(default="Cloudy with a chance", description="A short English description of what weather conditions to expect")