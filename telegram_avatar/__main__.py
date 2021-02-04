import asyncio
import logging
import os
import socks
import sys
from datetime import datetime

from telethon import TelegramClient
from telethon.tl.functions.photos import (
    UploadProfilePhotoRequest, DeletePhotosRequest
)

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from telegram_avatar.avatar_generator import AvatarGenerator
from telegram_avatar.open_weather_map_api import OpenWeatherMapAPI
from telegram_avatar.data_classes import WeatherData
from telegram_avatar.config import *


async def change_avatar(
        tg_client: TelegramClient,
        avatar_generator: AvatarGenerator,
) -> None:
    """
    Function which updates Telegram avatar with generated new one.
    Args:
        tg_client: authorised telethon.TelegramClient object.
        avatar_generator: AvatarGenerator object which generates
            new avatar image.
    """
    # Deleting Telegram avatar
    await tg_client(
        DeletePhotosRequest(await tg_client.get_profile_photos('me'))
    )
    # Generating and load a new Telegram avatar
    file = await tg_client.upload_file(
        avatar_generator.generate()
    )
    # Updating Telegram avatar
    await tg_client(
        UploadProfilePhotoRequest(file)
    )
    return


def get_logger() -> logging.Logger:
    """
    Method which creates server logger.
    Returns:
        logger object.
    """
    server_logger = logging.Logger(name="TG_Avatar")
    logger_format = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    server_logger.setLevel(logging.INFO)
    logging_handler = logging.StreamHandler(sys.stdout)
    logging_handler.setFormatter(logger_format)
    server_logger.addHandler(logging_handler)
    return server_logger


if __name__ == "__main__":

    # Get logger
    logger = get_logger()

    # Create folder for weather images if not exists
    if not os.path.exists(WEATHER_ICONS_FOLDER_NAME):
        os.mkdir(WEATHER_ICONS_FOLDER_NAME)

    # Loading proxy info
    if not all((PROXY_IP, PROXY_PORT, PROXY_PASS)):
        proxy = None
    else:
        proxy = (
            socks.SOCKS5, PROXY_IP, PROXY_PORT, True, PROXY_PASS, PROXY_PASS,
        )

    # Creating an instance of TelegramClient class
    client = TelegramClient(
        'TG_Avatar',                            # Session name
        api_id=TELEGRAM_API_ID,                 # Telegram API ID
        api_hash=TELEGRAM_API_HASH,             # Telegram API hash
        proxy=proxy,                            # Proxy data
    )
    # Starting a session
    client.start(
        phone=lambda: TELEGRAM_PHONE,           # Telegram phone number
        password=lambda: TELEGRAM_PASSWORD,     # Telegram password
    )

    # The 'volume' through which weather data will be exchanged
    weather_data = WeatherData()

    # Creating an instance of AvatarGenerator class
    generator = AvatarGenerator(
        weather_data=weather_data,
        text_color=TEXT_COLOR,
        bg_color=BACKGROUND_COLOR,
        logger=logger,
    )

    # Creating an instance of OpenWeatherMapAPI class
    weather_updater = OpenWeatherMapAPI(
        api_token=OPENWEATHER_API_KEY,
        api_url=OPENWEATHER_API_URL,
        image_url_template=OPENWEATHER_API_IMAGE_URL,
        weather_data=weather_data,
        logger=logger,
    )

    # Creating task scheduler instance
    scheduler = AsyncIOScheduler()

    # Adding a job which updating avatar every beginning of a minute
    scheduler.add_job(
        change_avatar,
        args=(client, generator),
        next_run_time=datetime.now(),
        trigger='cron',
        minute='*',
    )

    # Adding a job which updating weather data every beginning of a tenth minute
    scheduler.add_job(
        weather_updater.update_weather_data,
        args=(OPENWEATHER_API_CITYID,),
        next_run_time=datetime.now(),
        trigger='cron',
        minute='*/10',
        hour='*',
    )

    # Starting task loop
    scheduler.start()

    # Getting and starting asyncio event loop
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        sys.exit(1)
