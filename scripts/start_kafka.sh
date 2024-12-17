#!/bin/bash
echo "Démarrage de Kafka et Zookeeper..."

kubectl apply -f kafka/zookeeper.yaml
kubectl apply -f kafka/kafka-confluent.yaml
kubectl apply -f kafka/kafka-service.yaml

echo "Kafka et Zookeeper déployés. Vérification des pods..."
kubectl get pods | grep -E 'zookeeper|kafka'

# Afficher Kafka UI
get_external_ip() {
    EXTERNAL_IP=$(curl -s ifconfig.me || echo "34.79.68.61")
    echo "$EXTERNAL_IP"
}
EXTERNAL_IP=$(get_external_ip)
echo "Kafka UI : http://$EXTERNAL_IP:30000"
