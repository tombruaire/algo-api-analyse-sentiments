CREATE TABLE IF NOT EXISTS tweets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content TEXT NOT NULL,
    sentiment_score FLOAT,
    model_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Exemple de données initiales
INSERT INSERT INTO tweets (content, sentiment_score, model_type) VALUES
("I absolutely love this product!", 1.0, 'logistic'),
("Worst experience I've ever had.", -1.0, 'logistic'),
("It’s fine I guess, nothing special.", 0.0, 'transformer'),
("Amazing service, would buy again!", 1.0, 'transformer'),
("I hate this app. It keeps crashing.", -1.0, 'logistic'),
("Totally worth the price.", 1.0, 'transformer'),
("Do not recommend at all.", -1.0, 'logistic'),
("It's okay, does what it says.", 0.0, 'logistic'),
("Best feature update so far!", 1.0, 'transformer'),
("This is a joke, right?", -1.0, 'logistic'),
("Absolutely useless.", -1.0, 'transformer'),
("Solid performance and clean design.", 1.0, 'logistic'),
("Meh... not impressed.", 0.0, 'transformer'),
("Pretty decent overall.", 0.5, 'logistic'),
("Loved the experience!", 1.0, 'transformer'),
("Terrible UX. Couldn't find anything.", -1.0, 'logistic'),
("It's not bad, could be better.", 0.2, 'logistic'),
("Fantastic work on this version.", 1.0, 'transformer'),
("I’ve seen worse. I’ve also seen better.", 0.0, 'transformer'),
("Works as expected. Nothing more.", 0.0, 'logistic');