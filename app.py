import logging
import requests
from flask import Flask, jsonify, render_template
import time

app = Flask(__name__)

# Configuração de logging
logging.basicConfig(level=logging.INFO)  # Altere para ERROR para menos verbosidade
logger = logging.getLogger(__name__)

# Cache para armazenar dados temporariamente
cache = {
    "data": None,
    "timestamp": 0
}

CACHE_DURATION = 60  # Cache por 60 segundos

def get_crypto_data(crypto_id):
    current_time = time.time()
    # Verifica se o cache ainda é válido
    if cache["data"] and current_time - cache["timestamp"] < CACHE_DURATION:
        logger.info("Returning cached data.")
        return cache["data"]
    
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}"
    try:
        response = requests.get(url)
        logger.info(f"Fetching data from: {url}")
        if response.status_code == 200:
            data = response.json()
            formatted_data = {
                "name": data.get("name", "N/A"),
                "symbol": data.get("symbol", "N/A"),
                "current_price": data["market_data"]["current_price"].get("usd", "N/A"),
                "market_cap": data["market_data"]["market_cap"].get("usd", "N/A"),
                "24h_change": data["market_data"].get("price_change_percentage_24h", "N/A")
            }
            # Armazena no cache
            cache["data"] = formatted_data
            cache["timestamp"] = current_time
            logger.info("Data cached successfully.")
            return formatted_data
        else:
            logger.error(f"Error fetching data: {response.status_code}, {response.text}")
            return {"error": "Failed to fetch data"}
    except Exception as e:
        logger.error(f"Exception occurred: {e}")
        return {"error": "Failed to fetch data"}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/crypto/<crypto_id>', methods=['GET'])
def crypto(crypto_id):
    data = get_crypto_data(crypto_id)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
