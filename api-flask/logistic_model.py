import joblib
import os

# Charger le modèle et le vectorizer entraînés et sauvegardés
model_path = os.path.join("models", "model.pkl")
vectorizer_path = os.path.join("models", "vectorizer.pkl")

model = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)

def predict_sentiment(tweets):
    """
    Prend une liste de tweets et retourne une prédiction de sentiment :
    -1 pour négatif, 1 pour positif
    """
    X_tweets = vectorizer.transform(tweets)
    predictions = model.predict(X_tweets)
    return [1 if pred == 1 else -1 for pred in predictions]
