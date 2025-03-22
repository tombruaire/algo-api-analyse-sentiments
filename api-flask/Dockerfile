FROM python:3.9-slim

WORKDIR /app

# Arguments et variables d'environnement pour Flask
ARG PORT
ARG FLASK_APP
ARG FLASK_ENV
ARG FLASK_DEBUG

ENV PORT=${PORT}
ENV FLASK_APP=${FLASK_APP}
ENV FLASK_ENV=${FLASK_ENV}
ENV FLASK_DEBUG=${FLASK_DEBUG}

# Variables d'environnement pour la base de données
ENV DB_HOST=${DB_HOST}
ENV DB_USER=${DB_USER}
ENV DB_PASSWORD=${DB_PASSWORD}
ENV DB_NAME=${DB_NAME}

# Installation des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install mysql-connector-python

# Copie du code source
COPY . .

# Exposition du port
EXPOSE ${PORT}

# Commande de démarrage
CMD ["python3", "app.py"]