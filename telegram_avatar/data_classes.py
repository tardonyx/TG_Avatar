from typing import Optional, List, Union

from dataclasses import dataclass
from pydantic import BaseModel, Field


@dataclass
class WeatherData:
    """
    Dataclass to exchange weather data throw tasks.
    """
    current_temperature: Optional[float] = None
    current_weather_image: Optional[str] = None

    def is_up_to_date(self) -> bool:
        """
        Checking if weather data is up-to-date.
        Returns:
            True if weather data is up-to-date else False.
        """
        return all(self.__dict__.values())


# Models for validating response from OpenWeatherMap

class OpenWeatherMapCoordinates(BaseModel):
    """
    Model which represents 'coord' field in OpenWeatherMap API response.
    """
    lon: float
    lat: float


class OpenWeatherMapWeather(BaseModel):
    """
    Model which represents 'weather' field in OpenWeatherMap API response.
    """
    id: int
    main: str
    description: str
    icon: str


class OpenWeatherMapMain(BaseModel):
    """
    Model which represents 'main' field in OpenWeatherMap API response.
    """
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int


class OpenWeatherMapWind(BaseModel):
    """
    Model which represents 'wind' field in OpenWeatherMap API response.
    """
    speed: float
    deg: int


class OpeWeatherMapClouds(BaseModel):
    """
    Model which represents 'clouds' field in OpenWeatherMap API response.
    """
    all: int


class OpenWeatherMapSys(BaseModel):
    """
    Model which represents 'sys' field in OpenWeatherMap API response.
    """
    type: int
    id: int
    message: Optional[float] = None
    country: str
    sunrise: int
    sunset: int


class OpenWeatherMapRain(BaseModel):
    """
    Model which represents 'rain' field in OpenWeatherMap API response.
    """
    _1h: Union[int, str, float] = Field(alias="1h")
    _3h: Union[int, str, float] = Field(alias="3h")


class OpenWeatherMapSnow(BaseModel):
    """
    Model which represents 'snow' field in OpenWeatherMap API response.
    """
    _1h: Union[int, str, float] = Field(alias="1h")
    _3h: Union[int, str, float] = Field(alias="3h")


class OpenWeatherMap(BaseModel):
    """
    Model which represents full response from OpenWeatherMap API.
    """
    coord: OpenWeatherMapCoordinates
    weather: List[OpenWeatherMapWeather]
    base: str
    main: OpenWeatherMapMain
    visibility: int
    wind: Optional[OpenWeatherMapWind] = None
    clouds: Optional[OpeWeatherMapClouds] = None
    rain: Optional[OpenWeatherMapRain] = None
    show: Optional[OpenWeatherMapSnow] = None
    dt: int
    sys: Optional[OpenWeatherMapSys] = None
    timezone: int
    id: int
    name: str
    cod: int
