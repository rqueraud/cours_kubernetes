FROM python:3.9.20-slim-bookworm

RUN pip install google-cloud-bigquery kafka-python

COPY ./service-account.json ./service-account.json
COPY ./post_consumer/ ./
CMD [ "python", "main.py"]