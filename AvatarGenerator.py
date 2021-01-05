# -*- coding: utf-8 -*-

import os
import aiohttp
from datetime import datetime as dt
from typing import Union, Tuple, Optional
from PIL import Image, ImageDraw, ImageFont


WEATHER_ICONS_FOLDER_NAME = "API_Icons"  # A folder name where weather icons will be collecting.


class AvatarGenerator(object):
    """
    Class that generates avatar with current time and weather data if it available.

    Class AvatarGenerator uses OpenWeatherMap API to load weather information (specifically
    temperature and weather icon) for your city and generate avatar image with current time,
    current temperature and weather icon on it.
    The essence of this class is two methods:
        AvatarGenerator.update_weather_data() - updates the weather information and stores it.
        AvatarGenerator.generate() - generates avatar image with actually information.
    Note that if it impossible to load weather information avatar image will be generate
    only with current time on it.

    Attributes:
        api_token: OpenWeatherMap API token - necessary string for loading weather information from API.
        api_url: OpenWeatherMap API url - necessary string for loading weather information from API.
        image_url: OpenWeatherMap API url pattern to load weather icon. Later in this pattern will be paste
            string with weather icon name.
        text_color: Tuple of three ints from 0 to 255 which encodes RGB color to text on avatar image - not
            necessary attribute. (0, 0, 0) - by default.
        bg_color: Tuple of three ints from 0 to 255 which encodes RGB color to background of avatar image - not
            necessary attribute. (255, 255, 255) - by default.
    """

    __api_token: str    # Variable which stores OpenWeatherMap API token
    __api_url: str      # Variable which stores OpenWeatherMap API url
    __image_url: str    # Variable which stores OpenWeatherMap API url pattern to load weather icon

    __last_temperature: Optional[str] = None    # Last loaded temperature from OpenWeatherMap API or None
    __last_icon: Optional[str] = None           # Last loaded weather icon name from OpenWeatherMap API or None

    __text_color: Tuple[int]    # Text color (must be a tuple of three ints from 0 to 255 - RGB format)
    __bg_color: Tuple[int]      # Background color (must be a tuple of three ints from 0 to 255 - RGB format)

    def __init__(self, api_token, api_url, image_url, logger, text_color=(0, 0, 0), bg_color=(255, 255, 255)):
        """Inits AvatarGenerator with necessary API information and colors for text and background."""
        self.__api_token = api_token
        self.__api_url = api_url
        self.__image_url = image_url
        self.__logger = logger
        self.__text_color = text_color
        self.__bg_color = bg_color

    async def update_weather_data(self, city_id: int = 524901) -> Tuple[Optional[str], Optional[str]]:
        """
        Method which makes a GET request to OpenWeatherMap API in order to get current temperature and
        weather icon name to your city. It overwrites stored weather data with actual weather data or
        with None if request is unsuccessfully. Returns the tuple of updated weather data (temperature
        and weather icon name).

        Args:
            city_id: The code of the city for which you want to receive the weather data. Code for the Moscow
                city by default.

        Returns:
            Tuple of updated temperature and weather icon name or with Nones.
        """
        # Necessary information for request which loading in query string
        payload = {
            "id": city_id,
            "appid": self.__api_token,
        }
        self.__logger.info(f"Updating weather information with payload: {payload}")
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=self.__api_url,
                params=payload,
            ) as response:
                self.__logger.info(
                    f"New response from weather service. "
                    f"Status: {response.status}, body: {await response.json()}"
                )
                if response.status == 200:
                    # if request is success updating weather data with actual
                    data = await response.json(encoding="utf-8")
                    self.__last_temperature = data["main"]["temp"]
                    self.__last_icon = data["weather"][0]["icon"]
                    await self.__check_weather_image(self.__last_icon)
                else:
                    # if request is not success - updating with Nones
                    self.__last_temperature = None
                    self.__last_icon = None
        return self.__last_temperature, self.__last_icon

    def __weather_image_exists(self, image_name: str) -> bool:
        """Check if weather image icon is exists in folder."""
        img_path = os.path.join(os.getcwd(), WEATHER_ICONS_FOLDER_NAME, image_name+".png")
        exists = os.path.exists(img_path)
        self.__logger.info(f"Image with name {image_name} existing: {exists}")
        return exists

    async def __check_weather_image(self, image_name: str) -> None:
        """
        Method which checks if weather icon is already downloaded or download it.
        If downloading is not success - sets None to __last_icon.

        Args:
            image_name: Name of weather icon without file type part.

        Returns:
            None
        """
        if not self.__weather_image_exists(image_name):
            url = self.__image_url.format(image_name)
            self.__logger.info(f"Loading image with name: {image_name}...")
            async with aiohttp.ClientSession() as session:
                async with session.get(url=url) as response:
                    self.__logger.info(f"Getting response with status: {response.status}")
                    if response.status == 200:
                        data = await response.read()
                        with open(os.path.join(os.getcwd(), WEATHER_ICONS_FOLDER_NAME, image_name+".png"), "wb") as f:
                            f.write(data)
                        self.__logger.info(f"Saving new image ({len(data)} bytes)")
                    else:
                        self.__last_icon = None
        return

    @staticmethod
    def __get_celsius_from_kelvin(t_kelvin: Union[int, float, str]) -> str:
        """
        Method which converts temperature from Kelvin scale to Celsius and formats it to the
        "<sign><temperature> C" like view.

        Args:
            t_kelvin: String or number with Kelvin scale temperature.

        Returns:
            String with formatted temperature in Celsius scale.

        """
        t_kelvin = int(t_kelvin)
        t_celsius = t_kelvin-273
        result = u"{} C".format(str(t_celsius))
        if t_celsius >= 0:
            result = "+" + result
        return result

    def generate(self, avatar_name: str = "Avatar.png") -> os.path:
        """
        Method which generates avatar image with time and current weather data or only with current time
        if weather data is not available.

        Args:
            avatar_name: The name of the file with which the generated avatar will be savedю

        Returns:
            os.path object - absolute path to the generated avatar image.
        """
        bg = Image.new("RGBA", (200, 200), self.__bg_color+(255,))
        canvas = ImageDraw.Draw(bg)
        current_time = dt.now()
        self.__logger.info(f"Creating new avatar with name {avatar_name}...")
        time = "{:0>2d}:{:0>2d}".format(current_time.hour, current_time.minute)
        if all((self.__last_icon, self.__last_temperature)):
            icon_path = os.path.join("API_Icons", self.__last_icon+".png")
            icon = Image.open(icon_path, "r")
            font_temperature = ImageFont.truetype("OpenSans-Regular.ttf", 30)
            font_time = ImageFont.truetype("OpenSans-Regular.ttf", 50)
            temperature = self.__get_celsius_from_kelvin(self.__last_temperature)
            bg.paste(icon, (50, 55), icon)
            canvas.text((35, 20), time, font=font_time, fill=self.__text_color)
            canvas.text((65, 130), temperature, font=font_temperature, fill=self.__text_color)
        else:
            font_time = ImageFont.truetype("OpenSans-Regular.ttf", 60)
            canvas.text((20, 55), time, font=font_time, fill=self.__text_color)
        bg.save(avatar_name)
        return os.path.abspath(avatar_name)
