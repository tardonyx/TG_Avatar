from os import environ

# Telegram API constants
TELEGRAM_API_ID = int(environ.get("TG_AVATAR_TELEGRAM_API_ID", '0'))
TELEGRAM_API_HASH = environ.get("TG_AVATAR_TELEGRAM_API_HASH", '')
TELEGRAM_PHONE = environ.get("TG_AVATAR_TELEGRAM_PHONE", '')
TELEGRAM_PASSWORD = environ.get("TG_AVATAR_TELEGRAM_PASSWORD", '')

# Proxy data (keep it empty if not necessary)
PROXY_IP = environ.get("TG_AVATAR_PROXY_IP", '')
PROXY_PORT = int(environ.get("TG_AVATAR_PROXY_PORT", '0') or '0')
PROXY_PASSWORD = environ.get("TG_AVATAR_PROXY_PASSWORD", '')

# OpenWeather API
OPENWEATHER_API_KEY = environ.get("TG_AVATAR_OPENWEATHER_API_KEY", '')
OPENWEATHER_API_URL = environ.get("TG_AVATAR_OPENWEATHER_API_URL", "http://api.openweathermap.org/data/2.5/weather")
OPENWEATHER_API_CITYID = int(environ.get("TG_AVATAR_OPENWEATHER_API_CITY_ID", "524901"))
OPENWEATHER_API_IMAGE_URL = environ.get(
    "TG_AVATAR_OPENWEATHER_API_IMAGE_URL",
    "http://openweathermap.org/img/wn/{}@2x.png",
)

# Customization

__bg_color = environ.get("TG_AVATAR_COLOR_BACKGROUND", "255,255,255")
BACKGROUND_COLOR = tuple([int(n) for n in __bg_color.split(',')])

__text_color = environ.get("TG_AVATAR_COLOR_TEXT", "0,0,0")
TEXT_COLOR = tuple([int(n) for n in __text_color.split(',')])
