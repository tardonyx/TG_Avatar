# -*- coding: utf-8 -*-

import os
from datetime import datetime
from logging import Logger
from moviepy.editor import VideoFileClip
from PIL import Image, ImageDraw, ImageFont, ImageSequence
from typing import Union, Tuple, Optional

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
            bg_gif: Optional[str] = None,
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
            bg_gif: path to background gif file.
        """

        self._weather_data = weather_data
        self._logger = logger
        self._text_color = text_color
        self._bg_color = bg_color
        self._folder = image_folder
        self._font_temperature = ImageFont.truetype(font_file, 30)
        self._font_time = ImageFont.truetype(font_file, 50)
        self._font_time_larger = ImageFont.truetype(font_file, 60)
        self._bg_gif = Image.open(bg_gif) if bg_gif else None

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

    def generate(self) -> os.path:
        """
        Method which generates avatar image with time and current weather data
        or only with current time if weather data is not available.
        Returns:
            os.path object - absolute path to the generated avatar image.
        """

        # Create background
        bg_color = self._bg_color + ((0,) if self._bg_gif else (255,))
        bg = Image.new(mode="RGBA", size=(200, 200), color=bg_color)
        canvas = ImageDraw.Draw(bg)
        # Get and format current time
        current_time = datetime.now()
        time = "{:0>2d}:{:0>2d}".format(current_time.hour, current_time.minute)
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

        if self._bg_gif:
            # Set gif if necessary
            result_file = "avatar.mp4"
            frames = []
            to_frame = bg.copy()
            for frame in ImageSequence.Iterator(self._bg_gif):
                new_frame = frame.copy()
                new_frame = new_frame.resize((200, 200))
                new_frame = new_frame.convert("RGBA")
                new_frame.alpha_composite(to_frame)
                frames.append(new_frame)
            frames[0].save(
                "avatar.gif",
                save_all=True,
                append_images=frames[1:-1],
            )
            # Convert to MP4
            clip = VideoFileClip("avatar.gif")
            clip.write_videofile(result_file, logger=None)
        else:
            # Saving new avatar
            result_file = "avatar.png"
            bg.save(result_file)

        return os.path.abspath(result_file)


if __name__ == "__main__":

    from logging import getLogger

    weather_data = WeatherData(
        current_temperature=22,
        current_weather_image="04d",
    )

    generator = AvatarGenerator(
        weather_data=weather_data,
        text_color=(255, 255, 255),
        bg_color=(255, 255, 255),
        bg_gif="/Users/a19116473/Projects/TG_Avatar/bg_gif.gif",
        font_file="/Users/a19116473/Projects/TG_Avatar/OpenSans-Regular.ttf",
        image_folder="/Users/a19116473/Projects/TG_Avatar/API_Icons",
        logger=getLogger(),
    )

    generator.generate()
