#!/bin/bash
echo "Arrêt global des services..."

./stop_airflow.sh
./stop_post_consumer.sh
./stop_post_pusher.sh
./stop_kafka.sh

echo "Tous les services sont arrêtés."
