FROM python:3.8-buster

LABEL maintainer="andreybibea@gmail.com"

WORKDIR /tg_avatar

RUN apt update && apt install -y ffmpeg

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3",  "-m", "telegram_avatar"]
