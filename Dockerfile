FROM python:3.9-slim

WORKDIR /app

COPY . /app
ENV PULLUPS_BOT_TOKEN=<token>
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 && rm -rf /var/lib/apt/list/* && apt-get install ffmpeg -y

RUN pip install -r requirements.txt
RUN pip install "Pillow<10.0"
#VOLUME /home/asroilf/Documents/SRP_intern/pullup_counter:/app

CMD ["python", "main.py"]
