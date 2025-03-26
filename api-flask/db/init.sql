CREATE TABLE IF NOT EXISTS tweets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content TEXT NOT NULL,
    sentiment_score FLOAT,
    model_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Exemple de données initiales
INSERT INTO tweets (content, sentiment_score, model_type)
VALUES
  ('I love this product', 1.0, 'transformer'),
  ('This is terrible', -1.0, 'transformer'),
  ('Not bad at all', 1.0, 'logistic'),
  ('Worst thing I bought', -1.0, 'logistic');