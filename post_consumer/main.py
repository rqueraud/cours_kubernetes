import os
import json
from kafka import KafkaConsumer
from google.cloud import bigquery

def main():
    # Configuration du consumer Kafka
    consumer = KafkaConsumer(
        'posts',
        bootstrap_servers='kafka-broker-service:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='post-consumer-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    # Configuration BigQuery
    # Le fichier de service account est monté dans /secrets/service-account.json par le secret
    client = bigquery.Client.from_service_account_json('/secrets/service-account.json')
    project_id = client.project

    dataset_name = os.getenv('DATASET_NAME', 'data_devops')
    table_name = os.getenv('TABLE_NAME', 'posts')
    table_id = f"{project_id}.{dataset_name}.{table_name}"

    print(f"Consumer démarré. Projet: {project_id}, Dataset: {dataset_name}, Table: {table_name}")
    print("En attente de messages sur Kafka...")

    for message in consumer:
        data = message.value
        print(f"Message reçu : {data}")
        try:
            errors = client.insert_rows_json(table_id, [data])
            if errors:
                print(f"Erreurs lors de l'insertion: {errors}")
            else:
                print("Message inséré avec succès dans BigQuery")
        except Exception as e:
            print(f"Erreur lors du traitement du message: {e}")

if __name__ == "__main__":
    main()
