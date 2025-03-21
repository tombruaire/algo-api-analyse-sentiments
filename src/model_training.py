import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Plus de données fictives (exemple)
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

# Séparer les données
X_train, X_test, y_train, y_test = train_test_split(
    df['text'], df['positive'], test_size=0.25, random_state=42
)

# Vectorisation TF-IDF
vectorizer = TfidfVectorizer(stop_words='english')
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Modèle Régression logistique
model = LogisticRegression()
model.fit(X_train_tfidf, y_train)

# Prédictions
y_pred = model.predict(X_test_tfidf)

# Évaluation du modèle
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred, zero_division=0))

# Matrice de confusion
cm = confusion_matrix(y_test, y_pred)

# Affichage graphique propre de la matrice de confusion
plt.figure(figsize=(8,6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Negatif','Positif'], yticklabels=['Negatif','Positif'])
plt.xlabel('Prédiction')
plt.ylabel('Vraie Valeur')
plt.title('Matrice de confusion')
plt.savefig('src/matrice_confusion.png')  # sauvegarder la matrice sous forme d'image dans src
plt.show()
