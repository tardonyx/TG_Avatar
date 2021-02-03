class OpenWeatherMapAPIError(Exception):
    pass


class ImageDownloadError(OpenWeatherMapAPIError):
    pass


class WeatherDataDownloadError(OpenWeatherMapAPIError):
    pass
