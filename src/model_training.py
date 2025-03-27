import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import mysql.connector
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Connexion à la base de données MySQL
conn = mysql.connector.connect(
    host="db",  
    user="root",
    password="rootpassword",
    database="sentiments"
)

# Récupérer les tweets avec leurs scores
query = "SELECT content, sentiment_score FROM tweets WHERE sentiment_score IS NOT NULL"
df = pd.read_sql(query, conn)
conn.close()

# Création des labels : 1 = positif, 0 = négatif
df['label'] = df['sentiment_score'].apply(lambda x: 1 if x > 0 else 0)

# Vérifie qu'on a assez de données
if df.shape[0] < 2:
    print("Pas assez de données.")
    exit()

# Séparer les données
X_train, X_test, y_train, y_test = train_test_split(
    df['content'], df['label'], test_size=0.3, random_state=42
)

# Vectorisation TF-IDF
vectorizer = TfidfVectorizer(stop_words='english')
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Modèle : Régression logistique
model = LogisticRegression()
model.fit(X_train_tfidf, y_train)

# Prédictions
y_pred = model.predict(X_test_tfidf)

# Évaluation
print(" Accuracy:", accuracy_score(y_test, y_pred))
print("\n Classification Report:\n", classification_report(y_test, y_pred, zero_division=0))

# Créer le dossier logs s'il n'existe pas
os.makedirs("logs", exist_ok=True)

# Sauvegarder le rapport dans logs
report = classification_report(y_test, y_pred, zero_division=0)
with open("logs/classification_report.txt", "w") as f:
    f.write(report)

# Matrice de confusion standard
cm = confusion_matrix(y_test, y_pred)

# Matrice de confusion – classe POSITIVE
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Greens',
            xticklabels=['Négatif', 'Positif'],
            yticklabels=['Négatif', 'Positif'])
plt.title("Matrice de confusion – Classe Positive")
plt.xlabel("Prédiction")
plt.ylabel("Valeur réelle")
plt.tight_layout()
plt.savefig("logs/matrice_positive.png")
plt.close()

# Matrice de confusion – classe NÉGATIVE (vue inversée)
plt.figure(figsize=(6, 5))
sns.heatmap(cm[::-1, ::-1], annot=True, fmt='d', cmap='Blues',
            xticklabels=['Positif', 'Négatif'],
            yticklabels=['Positif', 'Négatif'])
plt.title("Matrice de confusion – Classe Négative")
plt.xlabel("Prédiction")
plt.ylabel("Valeur réelle")
plt.tight_layout()
plt.savefig("logs/matrice_negative.png")
plt.close()
