import sqlite3
import requests
import logging
from datetime import datetime
import pytz
from time import sleep

# Configuração do logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Função para inicializar o banco de dados
def init_db():
    with sqlite3.connect('crypto_data.db', timeout=30) as conn:
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

# Função para obter dados da API e salvar no banco de dados
def fetch_and_save_crypto_data(crypto_id):
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
            
            # Salva os dados no banco de dados com retentativas
            save_to_db_with_retry(formatted_data)
            logger.info("Data fetched and saved to database successfully.")
        else:
            logger.error(f"Error fetching data: {response.status_code}, {response.text}")
    except Exception as e:
        logger.error(f"Exception occurred: {e}")

# Função para salvar os dados no banco de dados com retentativas
def save_to_db_with_retry(data, max_retries=5):
    attempt = 0
    while attempt < max_retries:
        try:
            with sqlite3.connect('crypto_data.db', timeout=30) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO crypto_prices (name, symbol, current_price, market_cap, change_24h, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (data['name'], data['symbol'], data['current_price'], data['market_cap'], data['24h_change'], data['timestamp']))
                conn.commit()
                logger.info("Data saved to database successfully.")
                return
        except sqlite3.OperationalError as e:
            if "locked" in str(e):
                attempt += 1
                wait_time = 2 ** attempt  # Exponential backoff
                logger.warning(f"Database is locked. Retrying in {wait_time} seconds... (Attempt {attempt}/{max_retries})")
                sleep(wait_time)
            else:
                logger.error(f"Unexpected error saving data to the database: {e}")
                break
    logger.error("Failed to save data after multiple attempts due to database lock.")

# Função para obter o horário local ajustado para o fuso horário
def get_local_time():
    timezone = pytz.timezone('America/Sao_Paulo')  # Ajuste para o seu fuso horário
    local_time = datetime.now(timezone)
    return local_time.strftime('%Y-%m-%d %H:%M:%S')

# Executa a função de inicialização do banco de dados
init_db()

# Testando a função para garantir que dados estão sendo salvos
fetch_and_save_crypto_data('bitcoin')  # Teste com Bitcoin
fetch_and_save_crypto_data('dogecoin')  # Teste com Dogecoin
