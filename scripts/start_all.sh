#!/bin/bash
echo "Démarrage global des services..."

./start_kafka.sh
sleep 10  # Laissez Kafka démarrer correctement

./start_post_pusher.sh
./start_post_consumer.sh
./start_airflow.sh

echo "Tous les services sont démarrés."
kubectl get pods
