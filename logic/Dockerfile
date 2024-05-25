FROM ubuntu:20.04
FROM python:3.10.2-slim
ENV DEBIAN_FRONTEND="noninteractive"

RUN apt-get update -y \
    && apt-get install -y python3-pip \
    && apt-get install -y libpython3.7 \
    && apt-get install -y pkg-config libicu-dev \
    && apt-get install poppler-utils -y \
    && apt-get -y install tesseract-ocr-rus

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python3", "main.py"]
