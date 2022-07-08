# -*- coding: utf-8 -*-

import os
from datetime import datetime
from logging import Logger
from PIL import Image, ImageDraw, ImageFont
from typing import Union, Tuple

from telegram_avatar.data_classes import WeatherData


class AvatarGenerator:
    """
    Class that generates avatar with current time and weather data
    (if it is available).
    """

    def __init__(
            self,
            weather_data: WeatherData,
            logger: Logger,
            font_file: str,
            image_folder: str,
            text_color: Tuple[int, int, int] = (0, 0, 0),
            bg_color: Tuple[int, int, int] = (255, 255, 255),
    ):
        """
        Initializer.
        Args:
            weather_data: the 'volume' in which weather data will be published.
            logger: logger object.
            font_file: path to font file.
            image_folder: path to folder with weather icons.
            text_color: text color in RGB format.
            bg_color: background color in RGB format.
        """

        self._weather_data = weather_data
        self._logger = logger
        self._text_color = text_color
        self._bg_color = bg_color
        self._folder = image_folder
        self._font_temperature = ImageFont.truetype(font_file, 30)
        self._font_time = ImageFont.truetype(font_file, 50)
        self._font_time_larger = ImageFont.truetype(font_file, 60)

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
                self._folder,
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


if __name__ == "__main__":

    from logging import getLogger

    weather_data = WeatherData(
        current_temperature=22,
        current_weather_image="01d",
    )

    generator = AvatarGenerator(
        weather_data=weather_data,
        text_color=(0, 0, 0),
        bg_color=(255, 255, 255),
        font_file="/Users/a19116473/Projects/TG_Avatar/OpenSans-Regular.ttf",
        image_folder="/Users/a19116473/Projects/TG_Avatar/API_Icons",
        logger=getLogger(),
    )

    generator.generate()
