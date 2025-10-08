FROM python:3.12-slim AS builder

WORKDIR /app

COPY ./src/* .

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED 1
CMD ["python", "service.py"]