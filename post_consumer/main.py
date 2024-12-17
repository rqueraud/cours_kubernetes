from kafka import KafkaConsumer
import json
import os
from google.cloud import bigquery
import logging
import re
import argparse

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

KAFKA_BOOTSTRAP_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVER")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID")

def create_dataset_if_not_exists(client, dataset_id, project_id):
    dataset_ref = bigquery.DatasetReference(project_id, dataset_id)
    try:
        client.get_dataset(dataset_ref)
        log.info(f"Dataset {dataset_id} already exists.")
    except Exception:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "US"
        dataset.default_table_expiration_ms = 3600000 * 24
        client.create_dataset(dataset)
        log.info(f"Created dataset {dataset_id}.")

def transform_key(key):
    key = key.replace('@', '')
    key = re.sub(r'(?<!^)(?=[A-Z])', '_', key).lower()
    return key

def transform_post(post, allowed_columns):
    transformed_post = {transform_key(k): v for k, v in post.items()}
    return {k: v for k, v in transformed_post.items() if k in allowed_columns}

def insert_post_to_bigquery(client, dataset_id, table_id, post, schema):
    table_ref = client.dataset(dataset_id).table(table_id)
    allowed_columns = {field.name for field in schema}
    transformed_post = transform_post(post, allowed_columns)

    job_config = bigquery.LoadJobConfig(
        schema=schema,
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    )
    temp_filepath = '/tmp/kafka_post.json'
    with open(temp_filepath, 'w') as json_file:
        json.dump(transformed_post, json_file)

    with open(temp_filepath, 'rb') as json_file:
        job = client.load_table_from_file(json_file, table_ref, job_config=job_config)
    job.result()  # Wait for job to complete
    if job.errors:
        log.error(f"Error inserting post: {job.errors}")
    else:
        log.info(f"Inserted post with id: {transformed_post.get('id')}")

def consume_and_write_to_bigquery(kafka_host):
    # Kafka Consumer configuration
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=[kafka_host],  # Replace with your Kafka server(s)
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id=KAFKA_GROUP_ID,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    # BigQuery client and configuration
    #os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./service-account.json"
    client = bigquery.Client()

    dataset_id = 'data_devops'
    table_id = 'posts'
    project_id = client.project

    create_dataset_if_not_exists(client, dataset_id, project_id)

    schema = [
        bigquery.SchemaField('id', 'STRING', mode='REQUIRED'),
        bigquery.SchemaField('post_type_id', 'STRING', mode='REQUIRED'),
        bigquery.SchemaField('accepted_answer_id', 'STRING', mode='NULLABLE'),
        bigquery.SchemaField('creation_date', 'TIMESTAMP', mode='REQUIRED'),
        bigquery.SchemaField('score', 'INTEGER', mode='REQUIRED'),
        bigquery.SchemaField('view_count', 'INTEGER', mode='NULLABLE'),
        bigquery.SchemaField('body', 'STRING', mode='REQUIRED'),
        bigquery.SchemaField('owner_user_id', 'STRING', mode='REQUIRED'),
        bigquery.SchemaField('last_editor_user_id', 'STRING', mode='NULLABLE'),
        bigquery.SchemaField('last_edit_date', 'TIMESTAMP', mode='NULLABLE'),
        bigquery.SchemaField('last_activity_date', 'TIMESTAMP', mode='NULLABLE'),
        bigquery.SchemaField('title', 'STRING', mode='NULLABLE'),
        bigquery.SchemaField('tags', 'STRING', mode='NULLABLE'),
        bigquery.SchemaField('answer_count', 'INTEGER', mode='NULLABLE'),
        bigquery.SchemaField('comment_count', 'INTEGER', mode='REQUIRED'),
        bigquery.SchemaField('content_license', 'STRING', mode='REQUIRED'),
        bigquery.SchemaField('parent_id', 'STRING', mode='NULLABLE')
    ]

    # Consume messages and write to BigQuery
    for message in consumer:
        try:
            log.info(f"Consumed message: {message.value}")
            insert_post_to_bigquery(client, dataset_id, table_id, message.value, schema)
        except Exception as e:
            log.error(f"Error processing message: {e}")

# Main execution
if __name__ == "__main__":
    
    consume_and_write_to_bigquery(KAFKA_BOOTSTRAP_SERVER)
