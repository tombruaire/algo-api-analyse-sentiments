import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Données fictives
data = {
    'text': [
        "J'adore ce produit", "C'est horrible, très déçu", 
        "Meilleur achat jamais fait", "C'est nul, ne recommande pas",
        "Je suis très content", "Très mauvais service",
    ],
    'positive': [1, 0, 1, 0, 1, 0]
}

df = pd.DataFrame(data)

# Séparer données
X_train, X_test, y_train, y_test = train_test_split(df['text'], df['positive'], test_size=0.33, random_state=42)

# Vectoriser les textes
vectorizer = TfidfVectorizer(stop_words='english')
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Régression logistique
model = LogisticRegression()
model.fit(X_train_tfidf, y_train)

# Prédictions
y_pred = model.predict(X_test_tfidf)

# Évaluation du modèle
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
