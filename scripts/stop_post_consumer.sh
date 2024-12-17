#!/bin/bash
echo "Arrêt de Post Consumer..."

kubectl delete -f post_consumer/post-consumer-deployment.yaml

echo "Post Consumer arrêté."
