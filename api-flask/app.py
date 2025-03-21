import os
import re
from flask import Flask, jsonify, request
from transformers import pipeline
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)

# Utiliser le pipeline de Hugging Face pour l'analyse de sentiment
sentiment_analyser = pipeline("sentiment-analysis")

# Définir les longueurs minimale et maximale des tweets
MIN_TWEET_LENGTH = 5
MAX_TWEET_LENGTH = 280

def get_sentiment_score(tweet):
    """Utilise un modèle multilingue pour analyser le sentiment du tweet"""
    resultat = sentiment_analyser(tweet)
    sentiment_score = resultat[0]['score']
    
    # Si le label est 'NEGATIVE', le score sera négatif, sinon positif
    if resultat[0]['label'] == 'NEGATIVE':
        sentiment_score = -sentiment_score
    
    # Arrondi le score à 2 décimales
    return round(sentiment_score, 2)

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
                sentiment_score = get_sentiment_score(tweet)
                sentiment_resultat[f"tweet{index+1}"] = sentiment_score
        else:
            sentiment_resultat[f"tweet{index+1}"] = "Erreur: Tweet non valide, Veuillez fournir un text valide"

    return jsonify(sentiment_resultat)

if __name__ == '__main__':
    # Lancer l'application Flask sur le port spécifié ou par défaut
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    app.run(debug=debug_mode, host="0.0.0.0", port=port)
