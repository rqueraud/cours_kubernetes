#!/bin/bash
echo "Arrêt de Post Pusher..."

kubectl delete -f  cours_kafka/post_pusher/deployment.yaml

echo "Post Pusher arrêté."
