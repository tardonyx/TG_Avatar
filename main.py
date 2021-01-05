from telethon import TelegramClient
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from AvatarGenerator import AvatarGenerator
from datetime import datetime
from environment import *
import sys
import logging
import asyncio
import socks


async def change_avatar(tg_client: TelegramClient, avatar_generator: AvatarGenerator) -> None:
    """
    Function which updates Telegram avatar with generated new one.

    Args:
        tg_client: Authorised telethon.TelegramClient object.
        avatar_generator: AvatarGenerator object which generates new avatar image.

    Returns:
        None
    """
    await tg_client(DeletePhotosRequest(await tg_client.get_profile_photos('me')))  # deleting Telegram avatar
    file = await tg_client.upload_file(avatar_generator.generate())  # generating and load a new Telegram avatar
    await tg_client(UploadProfilePhotoRequest(file))  # updating Telegram avatar
    return


if __name__ == "__main__":

    # logging settings
    server_logger = logging.getLogger(__name__)
    logger_format = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    server_logger.setLevel(logging.INFO)
    logging_handler = logging.StreamHandler(sys.stdout)
    logging_handler.setFormatter(logger_format)
    server_logger.addHandler(logging_handler)

    # creating an instance of AvatarGenerator class with necessary information
    generator = AvatarGenerator(
        api_token=OPENWEATHER_API_KEY,
        api_url=OPENWEATHER_API_URL,
        image_url=OPENWEATHER_API_IMAGE_URL,
        logger=server_logger,
        text_color=TEXT_COLOR,
        bg_color=BACKGROUND_COLOR,
    )

    # loading proxy info from config file or setting None if proxy info is empty
    proxy = None if not all((PROXY_IP, PROXY_PORT, PROXY_PASSWORD)) \
        else (socks.SOCKS5, PROXY_IP, PROXY_PORT, True, PROXY_PASSWORD, PROXY_PASSWORD)

    # creating an instance of TelegramClient class
    client = TelegramClient(
        'TG_Avatar',                        # session name
        api_id=TELEGRAM_API_ID,             # Telegram API ID
        api_hash=TELEGRAM_API_HASH,         # Telegram API hash
        proxy=proxy,                        # Proxy data
    )
    # starting a session
    client.start(
        phone=lambda: TELEGRAM_PHONE,        # Telegram phone number (must be callable)
        password=lambda: TELEGRAM_PASSWORD,  # Telegram password (must be callable)
    )

    # creating task scheduler instance
    scheduler = AsyncIOScheduler()
    # adding a job which updating avatar every beginning of a minute (and starts immediately)
    scheduler.add_job(
        change_avatar,
        args=(client, generator),
        next_run_time=datetime.now(),
        trigger='cron',
        minute='*',
    )
    # adding a job which updating weather data every beginning of a tenth minute (and starts immediately)
    scheduler.add_job(
        generator.update_weather_data,
        args=(OPENWEATHER_API_CITYID,),
        next_run_time=datetime.now(),
        trigger='cron',
        minute='*/10',
        hour='*',
    )
    # starting task loop
    scheduler.start()

    # getting and starting asyncio event loop
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
