FROM python:3.9-slim

WORKDIR /app

COPY . /app
ENV PULLUPS_BOT_TOKEN=<TOKEN>
ENV CHAT_ID=<CHAT_ID>
ENV THREAD_ID=<THREAD_ID>
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 && rm -rf /var/lib/apt/list/* && apt-get install ffmpeg -y

RUN pip install -r requirements.txt
VOLUME ./pullup_counter:/app

CMD ["python", "main.py"]
