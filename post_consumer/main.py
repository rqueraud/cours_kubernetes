from google.cloud import bigquery
from kafka import KafkaConsumer
import json
import os
import argparse

# Configuration Kafka
TOPIC = "posts"

# Configuration BigQuery
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./service-account.json"

def write_to_bigquery(client, table_id, rows):
    errors = client.insert_rows_json(table_id, rows)
    if errors:
        print(f"Encountered errors while inserting rows: {errors}")
    else:
        print(f"Inserted {len(rows)} rows into BigQuery.")

def main(multiple, kafka_host):
    # Initialiser le client BigQuery
    client = bigquery.Client()
    PROJECT_ID = client.project
    DATASET_ID = 'data_devops'
    TABLE_ID = 'posts'

    # Consumer Kafka
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=[kafka_host],
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="consumer-group-1",
        value_deserializer=lambda x: json.loads(x.decode("utf-8"))
    )

    print(f"Listening to Kafka topic '{TOPIC}'...")
    for message in consumer:
        print(f"Received message: {message.value}")
        # Transformez le message pour BigQuery (ajustez selon votre schéma)
        rows_to_insert = [message.value]
        write_to_bigquery(client, f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}", rows_to_insert)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--multiple', action='store_true', help='Send one message and exit')
    parser.add_argument('--kafka_host', type=str, required=False, default=None, help='The Kafka host address, changing BigQuery target to Kafka')
    args = parser.parse_args()

    main(
        multiple=args.multiple,
        kafka_host=args.kafka_host
    )