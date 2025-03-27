#!/bin/zsh

echo "réentrainement en cours......"
/usr/local/bin/docker exec -i flask-api python retrain_model.py
echo "réentrainement terminé"
