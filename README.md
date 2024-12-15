# TP Kubernetes - Cours Data DevOps - Enseirb-Matmeca

Installer git-lfs avant de cloner le repo pour pouvoir telecharger le fichier de données :

```bash
brew install git-lfs
git lfs install
git clone git@github.com:rqueraud/cours_kubernetes.git
```

Placez le fichier `service-account.json` à la racine du projet.

Pour builder les images : 
```bash
docker build -t 2024_kubernetes_post_pusher -f ./post_pusher/Dockerfile .
docker build -t 2024_kubernetes_post_consumer -f ./post_consumer/Dockerfile .
```

Pour executer les images :
```bash
docker run 2024_kubernetes_post_pusher
```

## Lancer le déploiement

Depuis deploy.sh ou :

```bash
echo "Creating Kind cluster..."
kind delete cluster || true
kind create cluster --config ./kind/config.yaml

echo "Building Docker images..."
docker build -t 2024_kubernetes_post_pusher -f ./post_pusher/Dockerfile .
docker build -t 2024_kubernetes_post_consumer -f ./post_consumer/Dockerfile .

echo "Loading Docker images into Kind..."
kind load docker-image 2024_kubernetes_post_pusher
kind load docker-image 2024_kubernetes_post_consumer  

echo "Creating namespaces..."
kubectl create namespace airflow || true
kubectl create namespace app || true

echo "Deploying Airflow..."
kubectl apply -f ./airflow/airflow-dags-pv.yaml 
kubectl apply -f ./airflow/airflow-dags-pvc.yaml 
helm repo add airflow-stable https://airflow-helm.github.io/charts
helm install airflow airflow-stable/airflow --namespace airflow --version 8.9.0 --values ./airflow/custom-values.yaml 

echo "Deploying Kafka..."
kubectl apply -f cours_kafka/kafka/service.yaml
kubectl apply -f cours_kafka/kafka/deployment.yaml 

echo "Deploying Kafka UI..."
kubectl apply -f cours_kafka/ui/configmap.yaml
kubectl apply -f cours_kafka/ui/service.yaml
kubectl apply -f cours_kafka/ui/deployment.yaml

echo "Deploying application services..."
kubectl apply -f post_pusher/deployment.yaml 
kubectl apply -f post_consumer/deployment.yaml 

echo "Port-forwarding Airflow UI..."
kubectl port-forward svc/airflow-web 8080:8080 --namespace airflow

```