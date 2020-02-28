from telethon import TelegramClient#, sync
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from AvatarGenerator import AvatarGenerator
import asyncio
import config
import socks


import logging

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)


async def change_avatar(tg_client, avatar_generator):
    await tg_client(DeletePhotosRequest(await tg_client.get_profile_photos('me')))
    file = await tg_client.upload_file(avatar_generator.generate())
    await tg_client(UploadProfilePhotoRequest(file))


if __name__ == "__main__":

    generator = AvatarGenerator(
        api_token=config.openweather_api_key,
        api_url=config.openweather_api_url,
        image_url=config.openweather_api_image_url,
        text_color = config.txt_color,
        bg_color = config.bg_color,
    )

    proxy = None if not all((config.proxy_ip, config.proxy_port, config.proxy_pass)) \
        else (socks.SOCKS5, config.proxy_ip, config.proxy_port, True, config.proxy_pass, config.proxy_pass)

    client = TelegramClient(
        'TG_Avatar',
        api_id=config.telegram_api_id,
        api_hash=config.telegram_api_hash,
        proxy=proxy,
    )
    client.start(
        phone=lambda: config.tg_phone,
        password=lambda: config.tg_pass,
    )
    client.send_message('me', "TEST")

    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        change_avatar,
        args=(client, generator),
        trigger='cron',
        minute='*',
    )
    scheduler.add_job(
        generator.update_weather_data,
        args=(config.openweather_api_cityid,),
        trigger='cron',
        minute='*/10',
        hour='*',
    )
    scheduler.start()

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
