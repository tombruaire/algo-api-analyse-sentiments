import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import os

from db.db import get_db_connection

def retrain_logistic_model():
    print(" Reentrainement du modèle en cours...")

    # Connexion à la base de données
    conn = get_db_connection()
    query = "SELECT content, sentiment_score FROM tweets"
    df = pd.read_sql(query, conn)
    conn.close()

    # Nettoyage des données : filtrer uniquement les scores valides
    df = df[df['sentiment_score'].isin([-1.0, 1.0])]
    df['label'] = (df['sentiment_score'] > 0).astype(int)

    # Vérification : au moins 2 classes différentes
    if len(set(df['label'])) < 2:
        print("Pas assez de classes différentes pour réentrainer le modèle.")
        return

    X = df["content"]
    y = df["label"]

    # Vectorisation
    vectorizer = TfidfVectorizer(stop_words='english')
    X_tfidf = vectorizer.fit_transform(X)

    # Entraînement
    model = LogisticRegression()
    model.fit(X_tfidf, y)

    # Sauvegarde du modele et du vectorizer
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, os.path.join("models", "model.pkl"))
    joblib.dump(vectorizer, os.path.join("models", "vectorizer.pkl"))

    print("Modèle réentrainé et sauvegardé avec succès dans le dossier /models.")

    print(f"Nombre total de tweets utilisés pour le réentraînement : {len(df)}")
    print(f"Répartition des classes :\n{df['label'].value_counts()}")


if __name__ == "__main__":
    retrain_logistic_model()
