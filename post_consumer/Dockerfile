FROM python:3.10.19-slim-bookworm

RUN pip install google-cloud-bigquery kafka-python
ENV PYTHONUNBUFFERED=1

COPY ./service-account.json ./service-account.json
COPY ./post_consumer/ ./
CMD ["python", "main.py", "--multiple", "--kafka_host=kafka-broker-service:9092"]
