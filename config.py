# Telegram API constants
telegram_api_id: int = <telegram API id>
telegram_api_hash: str = <telegram API hash>
tg_phone: str = <phone number in international format>
tg_pass: str = <telegram password>

# Proxy data (keep it empty if not necessary)
proxy_ip: str = ''
proxy_port: int = 0
proxy_pass: str = ''

# OpenWeather API
openweather_api_key: str = <OpenWeatherMap API key>
openweather_api_url: str = "http://api.openweathermap.org/data/2.5/weather"
openweather_api_cityid: int = 524901  # for Moscow (for other cities look at the site)
openweather_api_image_url: str = "http://openweathermap.org/img/wn/{}@2x.png"

# Customization
bg_color = (255, 255, 255)
txt_color = (0, 0, 0)
