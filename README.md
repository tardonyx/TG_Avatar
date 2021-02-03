# TG_Avatar #

## Description ##

This script updates you avatar in Telegram every minute with adding time and 
weather data (weather icon and temperature) on it using Telegram API. Weather 
data getting from OpenWeatherMap API and updates every 10 minutes.
If all works fine, you will see something like that:

![Avatar Example](example_avatar.png)

Or like that if weather data is not available:

![Avatar Example No Weather](example_avatar_wo_weather.png)


## Getting Started ##

Before launching the script you should do some steps.

1. Telegram API

Get you own Telegram app api_id and app api_hash by following 
[this](https://core.telegram.org/api/obtaining_api_id) instruction.
Write them to `config.py` file or `.env` (in corresponds default values) with 
you phone number and password by adding corresponding values to variables.

2. OpenWeatherMap API

Get you own OpenWeatherMap API key from [there](https://openweathermap.org/api).
Note that you should create an account first. Write it to the 
`openweather_api_key` variable in `config.py` or `.env`. Then found you're 
city's id at openweathermap.org and write it to the 
`openweather_api_cityid` variable.

3. Installing requirements (not relevant for launching via Docker)

To installing requirements create virtual environment and use it for 
manual launching:

```shell script
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Customization ##

You can set text and background color by changing corresponds values 
in `config.py` file in block "customization" in manual launching mode or 
in `.env` file if launching in Docker.  
Note that values must be tuples of three ints (RGB format).  
Also you can change text font by using another font file and changing
path to it in `config.py` file in block "customization" in manual 
launching mode or in `.env` file if launching in Docker.  
Note that file must be TrueType or OpenType.  

## Launching (manual) ##

Execute in shell next command (while located in TG_Avatar base directory):

```shell script
python -m telegram_avatar
```

## Launching (with Docker) ##

First you should build the container:

```shell script
sudo docker build --tag tg_avatar .
```

Next change variables in `.env` file and launch the container 
(you should launch it in `interactive` mode because of
Telegram validation code):

```shell script
sudo docker run --env-file .env --interactive --name tg-avatar-1 tg_avatar
```

## License ##

	"THE BEERWARE LICENSE" (Revision 42):
	Andrey Bibea wrote this code. As long as you retain this 
	notice, you can do whatever you want with this stuff. If we
	meet someday, and you think this stuff is worth it, you can
	buy me a beer in return.