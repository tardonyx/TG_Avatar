# TG_Avatar #

## Description ##

This script updates you avatar in Telegram every minute with adding time and weather data (weather icon and temperature) on it using Telegram API. Weather data getting from OpenWeatherMap API and updates every 10 minutes.
If all works fine, you will see something like that:

![Avatar Example](Avatar.png)

Or like that if weather data is not available:

![Avatar Example No Weather](Avatar_wo_weather.png)


## Getting Started ##

Before launching the script you should do some steps.

1. Telegram API

Get you own Telegram app api_id and app api_hash by following [this](https://core.telegram.org/api/obtaining_api_id) instruction.
Write them to `environment.py` file (in corresponds default values) with you phone number and password by adding corresponding values to variables.

2. OpenWeatherMap API

Get you own OpenWeatherMap API key from [there](https://openweathermap.org/api). Note that you should create an account first.
Write it to the `openweather_api_key` variable in `environment.py`. Then found youre city's id at openweathermap.org and write it to the `openweather_api_cityid` variable.

3. Installing requirements

To instaling requirement modules execute this commant in shell while located in TG_Avatar base directory:

	pip install -r requirements.txt

## Customization ##

You can set text and background color by changing corresponds values in `environment.py` file in block "customization".
Note that values must be tuples of three ints (RGB format).

## Launching (manual) ##

Execute in shell next command (while located in TG_Avatar base directory):

    python3 main.py

## Launching (with Docker) ##

First you should build the container:

    sudo docker build --tag tg_avatar .

Next change variables in `.env` file and launch the container (you should launch it in `interactive` mode because of
Telegram validation code):

    sudo docker run --env-file .env --interactive tg_avatar

## Files and folders description ##

* `AvatarGenerator.py` - basic class for requesting weather data and generate avatar image;
* `main.py` - main file, you must launch it;
* `environment.py` - settings that contains Telegram API, OpenWeatherMap API and customization constants;
* `Avatar.png` - example of avatar image;
* `Avatar_wo_weather.png` - example of avatar image if weather data is not available;
* `requirements.txt` - list of requirement python modules;
* `OpenSans-Regular.ttf` - font file;
* `API_Icons` - folder there OpenWeatherMap API icons collects;

## License ##

	"THE BEERWARE LICENSE" (Revision 42):
	Andrey Bibea wrote this code. As long as you retain this 
	notice, you can do whatever you want with this stuff. If we
	meet someday, and you think this stuff is worth it, you can
	buy me a beer in return.