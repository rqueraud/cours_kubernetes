#!/bin/bash
echo "Arrêt d'Airflow..."

helm uninstall airflow -n airflow
kubectl delete pvc airflow-dags -n airflow

echo "Airflow arrêté."
