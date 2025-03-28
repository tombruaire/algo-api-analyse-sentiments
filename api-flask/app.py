import os
import re
from flask import Flask, jsonify, request
from transformers import pipeline
from dotenv import load_dotenv
from logistic_model import predict_sentiment
from flask_cors import CORS
from db.db import save_tweet_to_db, get_all_tweets

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)
CORS(app)

# Utiliser le pipeline de Hugging Face pour l'analyse de sentiment
sentiment_analyser = pipeline("sentiment-analysis")

# Définir les longueurs minimale et maximale des tweets
MIN_TWEET_LENGTH = 4
MAX_TWEET_LENGTH = 280


def get_sentiment_score(tweet):
    """Utilise un modèle multilingue pour analyser le sentiment du tweet"""
    resultat = sentiment_analyser(tweet)
    sentiment_score = resultat[0]['score']

    if resultat[0]['label'] == 'NEGATIVE':
        sentiment_score = -sentiment_score

    return round(sentiment_score, 2)


@app.route('/')
def home():
    return jsonify({
        "message": "Bienvenue sur l'API d'analyse des sentiments ! Utilisez l'endpoint POST '/api/analyse_sentiment' pour analyser les sentiments de tweets."
    })


@app.route('/api/analyse_sentiment', methods=['POST'])
def analyse_sentiment_route():
    data = request.get_json()

    if not data or not isinstance(data, list):
        return jsonify({"error": "La requête doit contenir une liste de tweets."}), 400

    sentiment_resultat = {}

    for index, tweet in enumerate(data):
        if isinstance(tweet, str):
            tweet_length = len(tweet)
            if tweet_length < MIN_TWEET_LENGTH:
                sentiment_resultat[f"tweet{index + 1}"] = "Erreur: le tweet est trop court (min 5 caractères)."
            elif tweet_length > MAX_TWEET_LENGTH:
                sentiment_resultat[f"tweet{index + 1}"] = "Erreur: le tweet est trop long (max 280 caractères)."
            elif re.match(r'^[\d\s]+$', tweet):
                sentiment_resultat[
                    f"tweet{index + 1}"] = "Erreur: le tweet ne doit contenir que des lettres et des espaces."
            elif not re.match(r'^[\wÀ-ÿ\s.,!?\'"-]+$', tweet, re.UNICODE):
                sentiment_resultat[
                    f"tweet{index + 1}"] = "Erreur: le tweet ne doit contenir que des lettres et des espaces."
            else:
                sentiment_score = get_sentiment_score(tweet)
                sentiment_resultat[f"tweet{index + 1}"] = sentiment_score
                save_tweet_to_db(tweet, sentiment_score, "transformer")  # ✅ ENREGISTREMENT
        else:
            sentiment_resultat[f"tweet{index + 1}"] = "Erreur: Tweet non valide, Veuillez fournir un text valide"

    return jsonify(sentiment_resultat)


@app.route('/api/logistic_regression_sentiment', methods=['POST'])
def logistic_regression_sentiment():
    data = request.get_json()

    if not data or not isinstance(data, list):
        return jsonify({"error": "La requête doit contenir une liste de tweets."}), 400

    try:
        predictions = predict_sentiment(data)
        resultat = {}

        for i, tweet in enumerate(data):
            resultat[f"tweet{i + 1}"] = predictions[i]
            save_tweet_to_db(tweet, predictions[i], "logistic")  # ✅ ENREGISTREMENT

        return jsonify(resultat)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

import os
import re
from flask import Flask, jsonify, request
from transformers import pipeline
from dotenv import load_dotenv
from logistic_model import predict_sentiment
from flask_cors import CORS
from db.db import save_tweet_to_db, get_all_tweets

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)
CORS(app)

# Utiliser le pipeline de Hugging Face pour l'analyse de sentiment
sentiment_analyser = pipeline("sentiment-analysis")

# Définir les longueurs minimale et maximale des tweets
MIN_TWEET_LENGTH = 4
MAX_TWEET_LENGTH = 280


def get_sentiment_score(tweet):
    """Utilise un modèle multilingue pour analyser le sentiment du tweet"""
    resultat = sentiment_analyser(tweet)
    sentiment_score = resultat[0]['score']

    if resultat[0]['label'] == 'NEGATIVE':
        sentiment_score = -sentiment_score

    return round(sentiment_score, 2)


@app.route('/')
def home():
    return jsonify({
        "message": "Bienvenue sur l'API d'analyse des sentiments ! Utilisez l'endpoint POST '/api/analyse_sentiment' pour analyser les sentiments de tweets."
    })


@app.route('/api/analyse_sentiment', methods=['POST'])
def analyse_sentiment_route():
    data = request.get_json()

    if not data or not isinstance(data, list):
        return jsonify({"error": "La requête doit contenir une liste de tweets."}), 400

    sentiment_resultat = {}

    for index, tweet in enumerate(data):
        if isinstance(tweet, str):
            tweet_length = len(tweet)
            if tweet_length < MIN_TWEET_LENGTH:
                sentiment_resultat[f"tweet{index + 1}"] = "Erreur: le tweet est trop court (min 5 caractères)."
            elif tweet_length > MAX_TWEET_LENGTH:
                sentiment_resultat[f"tweet{index + 1}"] = "Erreur: le tweet est trop long (max 280 caractères)."
            elif re.match(r'^[\d\s]+$', tweet):
                sentiment_resultat[
                    f"tweet{index + 1}"] = "Erreur: le tweet ne doit contenir que des lettres et des espaces."
            elif not re.match(r'^[\wÀ-ÿ\s.,!?\'"-]+$', tweet, re.UNICODE):
                sentiment_resultat[
                    f"tweet{index + 1}"] = "Erreur: le tweet ne doit contenir que des lettres et des espaces."
            else:
                sentiment_score = get_sentiment_score(tweet)
                sentiment_resultat[f"tweet{index + 1}"] = sentiment_score
                save_tweet_to_db(tweet, sentiment_score, "transformer")  # ✅ ENREGISTREMENT
        else:
            sentiment_resultat[f"tweet{index + 1}"] = "Erreur: Tweet non valide, Veuillez fournir un text valide"

    return jsonify(sentiment_resultat)


@app.route('/api/logistic_regression_sentiment', methods=['POST'])
def logistic_regression_sentiment():
    data = request.get_json()

    if not data or not isinstance(data, list):
        return jsonify({"error": "La requête doit contenir une liste de tweets."}), 400

    try:
        predictions = predict_sentiment(data)
        resultat = {}

        for i, tweet in enumerate(data):
            resultat[f"tweet{i + 1}"] = predictions[i]
            save_tweet_to_db(tweet, predictions[i], "logistic")  # ✅ ENREGISTREMENT

        return jsonify(resultat)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tweets', methods=['GET'])
def fetch_all_tweets():
    try:
        tweets = get_all_tweets()
        return jsonify(tweets)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    debug_mode = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    app.run(debug=debug_mode, host="0.0.0.0", port=port)



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    debug_mode = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    app.run(debug=debug_mode, host="0.0.0.0", port=port)
