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
docker build -t 2024_kubernetes_post_api -f ./post_api/Dockerfile .
```

Pour executer les images :
```bash
docker run 2024_kubernetes_post_pusher
docker run -p 8000:8000 2024_kubernetes_post_api
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

## Configuration ArgoCD

Créer un namespace pour argocd et l'installer à l'aide du manifest de la documentation officielle.

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

Forward le port afin d'avoir accès à la web interface.
```bash
kubectl port-forward --address 0.0.0.0 svc/argocd-server 8080:80 -n argocd
```

A partir de là nous pouvons déjà avoir accès au service web.

Nous pouvons nous connecter à l'aide du username `admin` et du mot de passe donné par la commande : 
```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
```

Cependant nous avons opté pour l'utilisation de la CLI de ArgoCD qui est plus claire.

Nous avons défini le namespace à celui de ArgoCD avec :

```bash
kubectl config set-context --current --namespace=argocd
```

Puis nous avons créé l'app avec :

```bash
argocd app create cours-kafka \
  --project default \
  --repo https://github.com/Misak0o/tp-devops \
  --path cours_kafka \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace default
```
Ici nous précisons le nom du projet (Définit à default si nous ne le précisons pas). Le lien du dépôt Github que ArgoCD va consulter. Le chemin vers les manifests (deployment, service, etc...). Le serveur de destination qui est définit comme ceci pour dire à ArgoCD d'aller voir le cluster dans lequel il est. Et enfin le namespace à default pour préciser où est déployée l'application.

Nous devons le déployer à l'aide de la commande :

```bash
argocd app sync cours-kafka
```

Cette commande va permettre de synchroniser la version locale à la version du dépôt distant et appliquer les changements.


Maintenant ArgoCD va surveiller notre repo Git. Il va lire les manifests du chemin cours-kafka et dès qu'il y a un changement, il va se mettre en OutOfSync et si on lance un Sync (manuellement ou automatiquement), il va appliquer les manifests nécessaires pour atteindre l'état désiré.

Si on veut rendre la synchronisation automatique on doit modifier la configuration d'ArgoCD avec la commande qui suit:

```bash
argocd app set cours-kafka --sync-policy automated --self-heal
```
