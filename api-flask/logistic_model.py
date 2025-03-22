import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Data fictive (remplace par une vraie connexion MySQL plus tard)
data = {
    'text': [
        "J'adore ce produit", "C'est horrible, très déçu",
        "Meilleur achat jamais fait", "C'est nul, ne recommande pas",
        "Je suis très content", "Très mauvais service",
        "Excellent travail, très satisfait", "Terrible expérience, plus jamais",
        "Produit incroyable", "Déception totale",
        "Je recommande vivement", "Catastrophique, à éviter",
        "Très agréable à utiliser", "Ça ne marche pas du tout",
        "Super ! j'aime beaucoup", "Service très médiocre",
        "Une très bonne expérience", "Très insatisfait, mauvais produit",
        "Absolument parfait", "Horrible, je n'aime pas du tout"
    ],
    'positive': [
        1, 0, 1, 0, 1, 0, 1, 0, 1, 0,
        1, 0, 1, 0, 1, 0, 1, 0, 1, 0
    ]
}

df = pd.DataFrame(data)

# Entraînement du modèle
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(df['text'])
y = df['positive']

model = LogisticRegression()
model.fit(X, y)

# Fonction d'analyse de sentiment
def predict_sentiment(tweets):
    X_tweets = vectorizer.transform(tweets)
    predictions = model.predict(X_tweets)
    # Convertir les prédictions en scores -1 (négatif), 1 (positif)
    scores = [1 if pred == 1 else -1 for pred in predictions]
    return scores
