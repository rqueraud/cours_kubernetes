#!/bin/bash
echo "Démarrage de Post Consumer..."

kubectl apply -f post_consumer/post-consumer-deployment.yaml

echo "Post Consumer déployé. Vérification des pods..."
kubectl get pods | grep post-consumer
