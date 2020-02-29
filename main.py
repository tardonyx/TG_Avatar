from telethon import TelegramClient
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from AvatarGenerator import AvatarGenerator
import sys
import asyncio
import config
import socks
from datetime import datetime


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
    return None


if __name__ == "__main__":

    # check if script launched with debug mode flag
    if len(sys.argv) > 1:
        if sys.argv[1] == "--debug":
            import logging
            logging.basicConfig()
            logging.getLogger('apscheduler').setLevel(logging.DEBUG)

    # creating an instance of AvatarGenerator class with necessary information
    generator = AvatarGenerator(
        api_token=config.openweather_api_key,
        api_url=config.openweather_api_url,
        image_url=config.openweather_api_image_url,
        text_color=config.txt_color,
        bg_color=config.bg_color,
    )

    # loading proxy info from config file or setting None if proxy info is empty
    proxy = None if not all((config.proxy_ip, config.proxy_port, config.proxy_pass)) \
        else (socks.SOCKS5, config.proxy_ip, config.proxy_port, True, config.proxy_pass, config.proxy_pass)

    # creating an instance of TelegramClient class
    client = TelegramClient(
        'TG_Avatar',                        # session name
        api_id=config.telegram_api_id,      # Telegram API ID
        api_hash=config.telegram_api_hash,  # Telegram API hash
        proxy=proxy,                        # Proxy data
    )
    # starting a session
    client.start(
        phone=lambda: config.tg_phone,      # Telegram phone number (must be callable)
        password=lambda: config.tg_pass,    # Telegram password (must be callable)
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
        args=(config.openweather_api_cityid,),
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
