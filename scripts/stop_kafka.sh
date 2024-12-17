#!/bin/bash
echo "Arrêt de Kafka et Zookeeper..."

kubectl delete -f kafka/zookeeper.yaml
kubectl delete -f kafka/kafka-confluent.yaml
kubectl delete -f kafka/kafka-service.yaml
echo "Kafka et Zookeeper arrêtés."
