import os
import re
import mysql.connector
from flask import Flask, jsonify, request
from transformers import pipeline
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)

connection_params = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'database': os.environ.get('DB_NAME', 'socialmetricsai'),
}

# Fonction pour créer la base de données et la table si elles n'existent pas
def create_database_and_table():
    try:
        connection = mysql.connector.connect(
            host=os.environ.get('DB_HOST', 'localhost'),
            user=os.environ.get('DB_USER', 'root'),
            password=os.environ.get('DB_PASSWORD', '')
        )

        cursor = connection.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS socialmetricsai;")
        cursor.execute("USE socialmetricsai;")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tweets (
                id INT(11) NOT NULL AUTO_INCREMENT,
                contenu TEXT NOT NULL,
                positive INT NOT NULL,
                negative INT NOT NULL,
                PRIMARY KEY (id)
            ) ENGINE=InnoDB;
        """)

        connection.commit()
        cursor.close()
        connection.close()
        print("Base de données et table créées avec succès.")
    except mysql.connector.Error as e:
        print(f"Erreur de connexion ou d'exécution SQL : {e}")

# Utiliser le pipeline de Hugging Face pour l'analyse de sentiment
sentiment_analyser = pipeline("sentiment-analysis")

# Définir les longueurs minimale et maximale des tweets
MIN_TWEET_LENGTH = 5
MAX_TWEET_LENGTH = 280

def get_sentiment_score(tweet):
    """Utilise un modèle multilingue pour analyser le sentiment du tweet"""

    # Vérifier des mots-clés négatifs spécifiques avant d'utiliser Hugging Face
    negative_keywords = ['n\'aime pas', 'bof', 'mauvais', 'détesté', 'horrible', 'nul', 'médiocre']
    if any(keyword in tweet.lower() for keyword in negative_keywords):
        return -0.8, "NEGATIVE"

    # Si aucun mot-clé négatif n'est trouvé, procéder avec Hugging Face
    resultat = sentiment_analyser(tweet)
    sentiment_score = resultat[0]['score']
    label = resultat[0]['label']

    # Ajustement pour mieux gérer les scores
    if label == 'NEGATIVE':
        sentiment_score = -sentiment_score

    # Logique pour ajuster la classification en fonction du score
    if sentiment_score >= 0.5:
        label = "POSITIVE"
    elif sentiment_score <= -0.5:
        label = "NEGATIVE"
    else:
        label = "NEUTRAL"
    
    sentiment_score = round(sentiment_score, 2)

    return sentiment_score, label

def save_to_database(tweet, positive, negative):
    """Sauvegarde de l'analyse de sentiment dans la base de données"""
    try:
        print(f"Connexion à la base de données avec les paramètres : {connection_params}")  # Debugging
        with mysql.connector.connect(**connection_params) as db:
            with db.cursor() as c:
                print(f"Insertion dans la base de données : {tweet}, Positive: {positive}, Negative: {negative}")  # Debugging
                c.execute("""
                    INSERT INTO tweets (contenu, positive, negative) 
                    VALUES (%s, %s, %s)
                """, (tweet, positive, negative))
                db.commit()
                print(f"Données insérées avec succès pour le tweet : {tweet}")
    except Exception as e:
        print(f"Erreur lors de l'enregistrement dans la base de données : {e}")

@app.route('/')
def home():
    return jsonify({"message": "Bienvenue sur l'API d'analyse des sentiments ! Utilisez l'endpoint POST '/api/analyse_sentiment' pour analyser les sentiments de tweets."})

@app.route('/api/analyse_sentiment', methods=['POST'])
def analyse_sentiment_route():
    """
    Analyse le sentiment des tweets reçus dans la requête POST.
    
    La requête doit contenir une liste de tweets.
    """
    data = request.get_json()

    # Vérification que la requête contient bien une liste de tweets
    if not data or not isinstance(data, list):
        return jsonify({"error": "La requête doit contenir une liste de tweets."}), 400

    sentiment_resultat = {}

    for index, tweet in enumerate(data):
        # Vérification que chaque tweet est une chaîne de caractères
        if isinstance(tweet, str):
            tweet_length = len(tweet)
            if tweet_length < MIN_TWEET_LENGTH:
                sentiment_resultat[f"tweet{index+1}"] = "Erreur: le tweet est trop court (min 5 caractères)."
            elif tweet_length > MAX_TWEET_LENGTH:
                sentiment_resultat[f"tweet{index+1}"] = "Erreur: le tweet est trop long (max 280 caractères)."
            elif re.match(r'^[\d\s]+$', tweet):
                sentiment_resultat[f"tweet{index+1}"] = "Erreur: le tweet ne doit contenir que des lettres et des espaces."
            elif not re.match(r'^[\wÀ-ÿ\s.,!?\'"-]+$', tweet, re.UNICODE):
                sentiment_resultat[f"tweet{index+1}"] = "Erreur: le tweet ne doit contenir que des lettres et des espaces."
            else:
                # Analyser le sentiment du tweet
                score, label = get_sentiment_score(tweet)

                # Définir les colonnes pour POSITIVE et NEGATIVE
                positive = 1 if label == "POSITIVE" else 0
                negative = 1 if label == "NEGATIVE" else 0

                # Sauvegarder dans la base de données (sans score)
                save_to_database(tweet, positive, negative)

                sentiment_resultat[f"tweet{index+1}"] = {"label": label, "score": score}
        else:
            sentiment_resultat[f"tweet{index+1}"] = "Erreur: Tweet non valide, Veuillez fournir un texte valide"

    return jsonify(sentiment_resultat)


if __name__ == '__main__':
    # Créer la base de données et la table avant de démarrer l'API Flask
    create_database_and_table()

    # Lancer l'application Flask sur le port spécifié ou par défaut
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    app.run(debug=debug_mode, host="0.0.0.0", port=port)
