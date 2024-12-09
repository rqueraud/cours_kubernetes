# TP Kubernetes - Cours Data DevOps - Enseirb-Matmeca

Installer git-lfs avant de cloner le repo pour pouvoir telecharger le fichier de données :

```bash
brew install git-lfs
git lfs install
git clone git@github.com:rqueraud/cours_kubernetes.git
```

Placez le fichier `service-account.json`à la racine du projet.

Pour builder les images : 
```bash
docker build -t 2024_kubernetes_post_pusher -f ./post_pusher/Dockerfile .
docker build -t 2024_kubernetes_post_consumer -f ./post_consumer/Dockerfile .
```

Pour executer les images :
```bash
docker run 2024_kubernetes_post_pusher
```

## Partie Kafka

```bash
git pull origin main

kind delete cluster
kind create cluster --config ./kind/config.yaml

kind load docker-image 2024_kubernetes_post_pusher
kind load docker-image 2024_kubernetes_post_consumer  

kubectl apply -f cours_kafka/kafka/deployment.yaml 
kubectl apply -f cours_kafka/ui/deployment.yaml 
kubectl apply -f post_pusher/deployment.yaml 
kubectl apply -f post_consumer/deployment.yaml 
```