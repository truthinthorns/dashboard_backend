from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, timedelta


class Weather(BaseModel):
    number: int = Field(
        description="The number of the forecast from the response.", ge=1
    )
    start_time: datetime = Field(
        description="The datetime for which this forecast is start being applicable",
    )
    end_time: datetime = Field(
        description="The datetime for which this forecast is no longer applicable",
    )
    temperature: int = Field(
        description="The temperature in Fahrenheit", ge=-40, le=140
    )
    icon: str = Field(
        description="A link to an icon representing the weather conditions",
    )
    wind_speed: str = Field(description="The wind speed along with mph")
    wind_direction: str = Field(
        description="The direction the wind is blowing", max_length=3
    )
    chance_of_rain: int = Field(
        description="The percentage for chance of rain", ge=0, le=100
    )
    humidity: int = Field(description="The percentage for humidity", ge=0, le=100)
    dewpoint: int = Field(description="The dewpoint in Fahrenheit", ge=-40, le=140)
    short_forecast: str = Field(
        description="A short English description of what weather conditions to expect",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "number": 1,
                "start_time": datetime.now(),
                "end_time": datetime.now() + timedelta(days=1),
                "temperature": 65,
                "icon": "https://api.weather.gov/icons/land/night/bkn?size=small",
                "wind_speed": "15 mph",
                "wind_direction": "E",
                "chance_of_rain": 85,
                "humidity": 10,
                "dewpoint": 50,
                "short_forecast": "Cloudy with a chance",
            }
        }
    )
