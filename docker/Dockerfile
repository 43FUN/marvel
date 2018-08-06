FROM python:3.6.4-alpine

ENV PYTHONUNBUFFERED=true

WORKDIR /app
COPY . /app

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "main.py"]
