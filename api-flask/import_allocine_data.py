import pandas as pd
import os
from db.db import get_db_connection

# Chemin vers les fichiers Kaggle téléchargés
BASE_PATH = "kaggle_data"
FILES = ["train.csv", "test.csv", "valid.csv"]

# Charger et concaténer les datasets
dfs = []
for file in FILES:
    path = os.path.join(BASE_PATH, file)
    df = pd.read_csv(path)
    print(f"Colonnes dans {file} :", df.columns)
    dfs.append(df)

# Concaténer les données
df = pd.concat(dfs, ignore_index=True)

# Garder uniquement les colonnes pertinentes et les renommer
df = df[['review', 'polarity']].rename(columns={
    'review': 'content',
    'polarity': 'sentiment_score'
})

# Conversion des labels : 1 (positif), 0 (négatif)
df['sentiment_score'] = df['sentiment_score'].apply(lambda x: 1.0 if x == 1 else -1.0)

# Connexion à la base de données et insertion
conn = get_db_connection()
cursor = conn.cursor()

insert_query = """
    INSERT INTO tweets (content, sentiment_score, model_type)
    VALUES (%s, %s, %s)
"""

for _, row in df.iterrows():
    cursor.execute(insert_query, (row['content'], row['sentiment_score'], "allocine_dataset"))

conn.commit()
cursor.close()
conn.close()

print("✅ Données du dataset Allociné insérées avec succès.")
