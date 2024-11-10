FROM python:3.9.20-bookworm

RUN pip install google-cloud-bigquery "fastapi[standard]"

COPY ./service-account.json ./service-account.json
COPY ./post_api/ ./
CMD [ "python", "main.py"]