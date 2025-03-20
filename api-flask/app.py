import os
from flask import Flask, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message" : "Bienvenue sur mon api Flask !"})

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({"data" : [1, 2, 3, 4, 5]})

if __name__ == '__main__':
   port = int(os.environ.get("PORT", 5000))
   debug_mode = os.getenv("FLASK_DEBUG", "True").lower() == "true"
   app.run(debug=debug_mode, host="0.0.0.0", port=port)