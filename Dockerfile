FROM python:3.9-slim

WORKDIR /app

COPY . /app
ENV PULLUPS_BOT_TOKEN=5397138212:AAGaFHLpHFu3lRgSxVhkOhvJG3s8c3j0JH8
ENV CHAT_ID=-1002500779625_659
ENV THREAD_ID=659
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 && rm -rf /var/lib/apt/list/* && apt-get install ffmpeg -y

RUN pip install -r requirements.txt
VOLUME ./pullup_counter:/app

CMD ["python", "main.py"]
