FROM python:3.9.20-slim-bookworm

RUN pip install google-cloud-bigquery

COPY ./service-account.json ./service-account.json
COPY ./post-pusher/ ./
CMD [ "python", "main.py"]