# -*- coding: utf-8 -*-

import os
from datetime import datetime
from typing import Union, Tuple
from logging import Logger

from PIL import Image, ImageDraw, ImageFont
from telegram_avatar.data_classes import WeatherData
from telegram_avatar.config import WEATHER_ICONS_FOLDER_NAME, FONT_FILE_NAME


class AvatarGenerator:
    """
    Class that generates avatar with current time and weather data
    (if it available).
    """

    def __init__(
            self,
            weather_data: WeatherData,
            logger: Logger,
            text_color: Tuple[int, int, int] = (0, 0, 0),
            bg_color: Tuple[int, int, int] = (255, 255, 255),
    ):
        """
        Initializer.
        Args:
            weather_data: the 'volume' in which weather data will be published.
            logger: logger object.
            text_color: text color in RGB format.
            bg_color: background color in RGB format.
        """
        self._weather_data = weather_data
        self._logger = logger
        self._text_color = text_color
        self._bg_color = bg_color
        self._font_temperature = ImageFont.truetype(FONT_FILE_NAME, 30)
        self._font_time = ImageFont.truetype(FONT_FILE_NAME, 50)
        self._font_time_larger = ImageFont.truetype(FONT_FILE_NAME, 60)
        return

    @staticmethod
    def _get_celsius_from_kelvin(t_kelvin: Union[int, float, str]) -> str:
        """
        Method which converts temperature from Kelvin scale to Celsius
        and formats it to the "<sign><temperature> C" like view.
        Args:
            t_kelvin: string or number with Kelvin scale temperature.
        Returns:
            string with formatted temperature in Celsius scale.
        """
        t_kelvin = int(t_kelvin)
        t_celsius = t_kelvin-273
        result = u"{} C".format(str(t_celsius))
        if t_celsius >= 0:
            result = "+" + result
        return result

    def generate(self, avatar_name: str = "Avatar.png") -> os.path:
        """
        Method which generates avatar image with time and current weather data
        or only with current time if weather data is not available.
        Args:
            avatar_name: the name of the file with which the generated
                avatar will be saved.
        Returns:
            os.path object - absolute path to the generated avatar image.
        """
        # Create background
        bg = Image.new(
            mode="RGBA",
            size=(200, 200),
            color=self._bg_color + (255,),
        )
        canvas = ImageDraw.Draw(bg)
        # Get and format current time
        current_time = datetime.now()
        time = "{:0>2d}:{:0>2d}".format(current_time.hour, current_time.minute)
        self._logger.info(f"Creating new avatar with name {avatar_name}...")
        # If up-to-date weather data exists
        if self._weather_data.is_up_to_date():
            # Prepare weather icon
            icon_path = os.path.join(
                os.getcwd(),
                WEATHER_ICONS_FOLDER_NAME,
                self._weather_data.current_weather_image + ".png",
            )
            icon = Image.open(icon_path, "r")
            # Convert temperature
            temperature = self._get_celsius_from_kelvin(
                t_kelvin=self._weather_data.current_temperature,
            )
            # Draw icon on background
            bg.paste(im=icon, box=(50, 55), mask=icon)
            # Draw time in background
            canvas.text(
                xy=(35, 20),
                text=time,
                font=self._font_time,
                fill=self._text_color,
            )
            # Draw temperature on background
            canvas.text(
                xy=(65, 130),
                text=temperature,
                font=self._font_temperature,
                fill=self._text_color,
            )
        # If weather data is out of date
        else:
            # Draw just time on background with larger font
            canvas.text(
                xy=(20, 55),
                text=time,
                font=self._font_time_larger,
                fill=self._text_color,
            )
        # Saving new avatar
        bg.save(avatar_name)
        return os.path.abspath(avatar_name)
