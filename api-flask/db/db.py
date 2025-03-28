import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST","localhost"),
        user=os.getenv("MYSQL_USER","root"),
        password=os.getenv("MYSQL_PASSWORD","rootpassword"),
        database=os.getenv("MYSQL_DATABASE","sentiment"),
    )

def save_tweet_to_db (content, score, model_type):
    conn= get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO tweets (content, sentiment_score, model_type) VALUES (%s, %s, %s)
    """

    cursor.execute(query, (content, score, model_type))
    conn.commit()
    cursor.close()
    conn.close()

def get_all_tweets(limit=100):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tweets ORDER BY created_at DESC LIMIT %s", (limit,))
    tweets = cursor.fetchall()
    cursor.close()
    conn.close()
    return tweets
