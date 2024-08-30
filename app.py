import logging
import requests
import sqlite3
from flask import Flask, jsonify, render_template
from datetime import datetime
import pytz

app = Flask(__name__)

# Configuração de logging
logging.basicConfig(level=logging.INFO)  # Altere para ERROR para menos verbosidade
logger = logging.getLogger(__name__)

def init_db():
    conn = sqlite3.connect('crypto_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS crypto_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            symbol TEXT,
            current_price REAL,
            market_cap REAL,
            change_24h REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Função para salvar dados no banco de dados
def save_to_db(data):
    try:
        conn = sqlite3.connect('crypto_data.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO crypto_prices (name, symbol, current_price, market_cap, change_24h, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data['name'], data['symbol'], data['current_price'], data['market_cap'], data['24h_change'], data['timestamp']))
        conn.commit()
        conn.close()
        logger.info("Data saved to database successfully.")
    except sqlite3.Error as e:
        logger.error(f"Error saving data to the database: {e}")

# Função para obter dados da API
def get_crypto_data(crypto_id):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}"
    try:
        response = requests.get(url)
        logger.info(f"Fetching data from: {url}")
        if response.status_code == 200:
            data = response.json()
            formatted_data = {
                "name": data.get("name", "N/A"),
                "symbol": data.get("symbol", "N/A"),
                "current_price": data["market_data"]["current_price"].get("brl", 0),  # Usando 'brl' para preço em reais
                "market_cap": data["market_data"]["market_cap"].get("brl", 0),  # Usando 'brl' para market cap em reais
                "24h_change": data["market_data"].get("price_change_percentage_24h", 0),
                "timestamp": get_local_time()  # Ajusta para o fuso horário local
            }
            save_to_db(formatted_data)
            return formatted_data
        elif response.status_code == 429:  # Limite de requisições excedido
            logger.warning("API rate limit exceeded. Fetching the latest data from the database.")
            return fetch_latest_from_db(crypto_id)
        else:
            logger.error(f"Error fetching data: {response.status_code}, {response.text}")
            return {"error": "Failed to fetch data"}
    except Exception as e:
        logger.error(f"Exception occurred: {e}")
        return {"error": "Failed to fetch data"}

# Função para buscar os últimos dados disponíveis no banco de dados
def fetch_latest_from_db(crypto_name):
    try:
        conn = sqlite3.connect('crypto_data.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT name, symbol, current_price, market_cap, change_24h, timestamp
            FROM crypto_prices
            WHERE name = ?
            ORDER BY timestamp DESC
            LIMIT 1
        ''', (crypto_name.capitalize(),))  # Ajuste para capitalizar o nome da moeda
        result = cursor.fetchone()
        conn.close()
        if result:
            return {
                "name": result[0],
                "symbol": result[1],
                "current_price": result[2],
                "market_cap": result[3],
                "24h_change": result[4],
                "timestamp": result[5]
            }
        return {"error": "No data available"}
    except sqlite3.Error as e:
        logger.error(f"Error fetching data from the database: {e}")
        return {"error": "Failed to fetch data from the database"}

# Função para obter o horário local ajustado para o fuso horário
def get_local_time():
    timezone = pytz.timezone('America/Sao_Paulo')  # Ajuste para o seu fuso horário
    local_time = datetime.now(timezone)
    return local_time.strftime('%Y-%m-%d %H:%M:%S')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/crypto/<crypto_id>', methods=['GET'])
def crypto(crypto_id):
    data = get_crypto_data(crypto_id)
    return jsonify(data)

if __name__ == '__main__':
    init_db()  # Inicializa o banco de dados
    app.run(debug=True)
