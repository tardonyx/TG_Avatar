# -*- coding: utf-8 -*-

import json
import config
import os
import aiohttp
from datetime import datetime as dt
from typing import Union, Tuple
from PIL import Image, ImageDraw, ImageFont


class AvatarGenerator(object):

    __api_token: str
    __api_url: str
    __image_url: str

    __last_temperature: Union[str, None] = None
    __last_icon: Union[str, None] = None

    __text_color: Tuple[int]
    __bg_color: Tuple[int]

    def __init__(self, api_token, api_url, image_url, text_color=(0, 0, 0), bg_color=(255, 255, 255)):
        self.__api_token = api_token
        self.__api_url = api_url
        self.__image_url = image_url
        self.__text_color = text_color
        self.__bg_color = bg_color

    async def update_weather_data(self, city_id=524901):
        payload = {
            "id": city_id,
            "appid": self.__api_token,
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=self.__api_url,
                params=payload,
            ) as response:
                if response.status == 200:
                    data = await response.json(encoding="utf-8")
                    self.__last_temperature = data["main"]["temp"]
                    self.__last_icon = data["weather"][0]["icon"]
                    await self.__check_weather_image(self.__last_icon)
        return self.__last_temperature, self.__last_icon

    @staticmethod
    def __weather_image_exists(image_name=""):
        img_path = os.path.join(os.getcwd(), "API_Icons", image_name+".png")
        return os.path.exists(img_path)

    async def __check_weather_image(self, image_name=""):
        if not self.__weather_image_exists(image_name):
            url = self.__image_url.format(image_name)
            async with aiohttp.ClientSession() as session:
                async with session.get(url=url) as response:
                    if response.status == 200:
                        with open(os.path.join(os.getcwd(), "API_Icons", image_name+".png"), "wb") as f:
                            f.write(await response.read())
        return None

    @staticmethod
    def __get_celsius_from_kelvin(t_kelvin: Union[int, float, str]) -> str:
        t_kelvin = int(t_kelvin)
        t_celsius = t_kelvin-273
        result = u"{} C".format(str(t_celsius))
        if t_celsius >= 0:
            result = "+" + result
        return result

    def generate(self, avatar_name="Avatar.png"):
        bg = Image.new("RGBA", (200, 200), self.__bg_color+(255,))
        canvas = ImageDraw.Draw(bg)
        time = "{:0>2d}:{:0>2d}".format(dt.now().hour, dt.now().minute)
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


if __name__ == "__main__":

    generator = AvatarGenerator(
        api_token=config.openweather_api_key,
        api_url=config.openweather_api_url,
        image_url=config.openweather_api_image_url,
        text_color=config.txt_color,
        bg_color=config.bg_color,
    )
    generator.generate()
