# TP Kubernetes - Cours Data DevOps - ENSEIRB-Matmeca

Mathias ROSA - Mathieu MOREL

## Prérequis

- Docker et Docker Desktop
- Kubernetes (via Kind)
- kubectl
- k9s (optionnel mais recommandé)
- Git LFS pour les fichiers volumineux

## Installation

### 1. Cloner le repository avec Git LFS

```bash
brew install git-lfs
git lfs install
git clone git@github.com:rqueraud/cours_kubernetes.git
```

### 2. Configuration

Créez le fichier `service-account.json` à la racine du projet.

### 3. Créer un cluster Kind

```bash
kind create cluster --config ./kind/config.yaml
kind get clusters  # Vérifie qu'il existe bien un cluster kind
```

## Construction des images Docker

Construisez les trois images requises :

```bash
docker build -t kubernetes_post_pusher -f ./post_pusher/Dockerfile .
docker build -t kubernetes_post_api -f ./post_api/Dockerfile .
docker build -t kubernetes_post_consumer -f ./post_consumer/Dockerfile .
```

Charger les images dans Kind :

```bash
kind load docker-image kubernetes_post_pusher
kind load docker-image kubernetes_post_api
kind load docker-image kubernetes_post_consumer
```

## Déploiement Kubernetes

### Créer le namespace

```bash
kubectl create ns cours-kubernetes
```

### Appliquer les configurations

#### Avec ArgoCD

Installer ArgoCD : <https://argo-cd.readthedocs.io/en/stable/getting_started/>

**Install Argo CD**
```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

**Download Argo CD CLI**

```bash
brew install argocd
```

**Access The Argo CD API Server**

Change the argocd-server service type to LoadBalancer:
```bash
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'
```

And then :
```bash
kubectl get svc argocd-server -n argocd -o=jsonpath='{.status.loadBalancer.ingress[0].ip}'
```

Port Forwarding¶
> We changed the port to 8081 to avoid conflict with other services that may be using port 8080 on your local machine.
```bash
kubectl port-forward svc/argocd-server -n argocd 8081:443
```

**Apply config**
```bash
kubectl apply -f ./argocd/

```


#### Sans ArgoCD

```bash
kubectl apply -n cours-kubernetes -f ./argocd/namespace.yml
kubectl apply -n cours-kubernetes -f ./argocd/kafka.yml
kubectl apply -n cours-kubernetes -f ./argocd/kafka-ui.yml
kubectl apply -n cours-kubernetes -f ./argocd/post-pusher.yml
kubectl apply -n cours-kubernetes -f ./argocd/post-consumer.yml

# UI et autres services
kubectl apply -n cours-kubernetes -f ./ui/configmap.yaml
kubectl apply -n cours-kubernetes -f ./ui/deployment.yaml
kubectl apply -n cours-kubernetes -f ./ui/service.yaml
```

### Monitorer le déploiement

```bash
# Avec k9s (interface interactive recommandée)
k9s -n cours-kubernetes
```

## Commandes utiles

```bash
kind create cluster --config ./kind/config.yaml
kind get clusters  # Vérifie qu'il existe bien un cluster kind
kind load docker-image my_image

k9s -n cours-kubernetes # Controller l'état du déploiement kubernetes

kubectl create ns cours-kubernetes  # Créer un namespace
kubectl apply -n cours-kubernetes -f my_file.yaml

kubectl delete all -n cours-kubernetes --all  # Supprime tout dans le namespace
```

## Nettoyage

Pour supprimer complètement le namespace et toutes ses ressources :

```bash
kubectl delete namespace cours-kubernetes
```
