from typing import Tuple
from logging import Logger
import os

from aiohttp import ClientSession, ClientError
from pydantic import ValidationError
from telegram_avatar.config import WEATHER_ICONS_FOLDER_NAME
from telegram_avatar.data_classes import WeatherData, OpenWeatherMap
from telegram_avatar.exceptions import (
    WeatherDataDownloadError, ImageDownloadError,
)


class OpenWeatherMapAPI:

    def __init__(
            self,
            api_token: str,
            api_url: str,
            image_url_template: str,
            weather_data: WeatherData,
            logger: Logger,
    ):
        """
        Initializer.
        Args:
            api_token: OpenWeatherMap API token.
            api_url: OpenWeatherMap API URL.
            image_url_template: URL template for downloading weather image.
            weather_data: the 'volume' in which weather data will be published.
            logger: logger object.
        """
        self._api_token = api_token
        self._api_url = api_url
        self._api_image_url = image_url_template
        self._weather_data = weather_data
        self._logger = logger
        self._client_session = ClientSession()
        return

    def _weather_image_exists(self, image_name: str) -> bool:
        """
        Check if weather image icon is exists in folder.
        Args:
            image_name: name of image (w/o extension).
        Returns:
            True if image is exist, else False.
        """
        img_path = os.path.join(
            os.getcwd(),
            WEATHER_ICONS_FOLDER_NAME,
            image_name + ".png",
        )
        exists = os.path.exists(img_path)
        self._logger.info(f"Image with name {image_name} existing: {exists}")
        return exists

    async def _get_weather_image(self, image_name: str) -> None:
        """
        Method which downloads a weather icon from OpenWeatherMap API.
        Args:
            image_name: name of weather icon (w/o extension).
        Raises:
            ImageDownloadError: if OpenWeatherMap API returns response
                with status code different from 200 or request raises
                aiohttp.ClientError.
        Returns:
            None.
        """
        url = self._api_image_url.format(image_name)
        self._logger.info(f"Loading image with name: {image_name}...")
        try:
            resp = await self._client_session.get(url=url)
        except ClientError as request_error:
            self._logger.exception(request_error)
            raise ImageDownloadError(
                "Couldn't download weather icon from OpenWeatherMap..."
            )
        self._logger.info(f"Getting response with status: {resp.status}")
        if resp.status != 200:
            raise ImageDownloadError(
                "Couldn't download weather icon from OpenWeatherMap..."
            )
        data = await resp.read()
        new_image_path = os.path.join(
            os.getcwd(),
            WEATHER_ICONS_FOLDER_NAME,
            image_name + ".png",
        )
        with open(new_image_path, "wb") as image_file:
            image_file.write(data)
        self._logger.info(f"Saving new image ({len(data)} bytes)")
        return

    async def _get_weather_data(self, city_id: int) -> Tuple[float, str]:
        """
        Method which makes a GET request to OpenWeatherMap API in order to
        get current temperature and weather icon name to your city.
        Returns the tuple of updated weather data (temperature
        and weather icon name).
        Args:
            city_id: the code of the city for which you want to receive
                the weather data.
        Raises:
            WeatherDataDownloadError: if OpenWeatherMap API returns
                response with status code different from 200.
        Returns:
            tuple with current temperature and weather icon name.
        """
        # Necessary information for request which loading in query string
        payload = {
            "id": city_id,
            "appid": self._api_token,
        }
        self._logger.info(
            f"Updating weather information with payload: {payload}"
        )
        # Trying making request
        try:
            response = await self._client_session.get(
                url=self._api_url,
                params=payload,
            )
        except ClientError as request_error:
            self._logger.exception(request_error)
            raise WeatherDataDownloadError(
                "Couldn't update weather data from OpenWeatherMap..."
            )
        # Trying validate response body
        try:
            response_body = await response.json(encoding="utf-8")
            validated_response_body = OpenWeatherMap(**response_body)
        except ValidationError as error:
            self._logger.exception(error)
            raise WeatherDataDownloadError(
                "Couldn't update weather data from OpenWeatherMap..."
            )
        self._logger.info(
            f"New response from weather service. "
            f"Status: {response.status}, body: {validated_response_body}"
        )
        if response.status != 200:
            raise WeatherDataDownloadError(
                "Couldn't update weather data from OpenWeatherMap..."
            )
        # If request is success updating weather data with actual
        new_temperature = validated_response_body.main.temp
        new_icon = validated_response_body.weather[0].icon
        if not self._weather_image_exists(new_icon):
            await self._get_weather_image(new_icon)
        return new_temperature, new_icon

    async def update_weather_data(self, city_id: int) -> None:
        """
        Main method which updates weather data and publish it into a queue.
        Args:
            city_id: the code of the city for which you want to receive
                the weather data. Code for the Moscow city by default.
        Returns:
            None.
        """
        try:
            new_temp, new_icon = await self._get_weather_data(city_id=city_id)
            self._weather_data.current_temperature = new_temp
            self._weather_data.current_weather_image = new_icon
        except (WeatherDataDownloadError, ImageDownloadError) as err:
            self._logger.exception(err)
            self._weather_data.current_temperature = None
            self._weather_data.current_weather_image = None
        return
