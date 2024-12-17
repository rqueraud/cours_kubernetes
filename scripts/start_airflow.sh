#!/bin/bash
echo "Démarrage d'Airflow..."

kubectl apply -f airflow/airflow-dags-pv.yaml
kubectl apply -f airflow/airflow-dags-pvc.yaml
helm upgrade --install airflow apache-airflow/airflow \
  --namespace airflow \
  --set dags.persistence.existingClaim=airflow-dags

echo "Airflow déployé avec succès. Vérification des pods..."
kubectl get pods -n airflow

# Afficher Airflow UI
get_external_ip() {
    EXTERNAL_IP=$(curl -s ifconfig.me || echo "34.79.68.61")
    echo "$EXTERNAL_IP"
}
EXTERNAL_IP=$(get_external_ip)
echo "Airflow UI : http://$EXTERNAL_IP:30080"
