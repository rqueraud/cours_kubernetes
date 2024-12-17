#!/bin/bash
echo "Démarrage de Post Pusher..."

kubectl apply -f cours_kafka/post_pusher/deployment.yaml

echo "Post Pusher déployé. Vérification des pods..."
kubectl get pods | grep post-pusher
