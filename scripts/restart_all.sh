#!/bin/bash
echo "Redémarrage global des services..."

./stop_all.sh
sleep 5
./start_all.sh

echo "Redémarrage global terminé."
