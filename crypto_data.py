import requests

def get_crypto_data(crypto_id):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}"
    try:
        response = requests.get(url)
        print(f"Fetching data from: {url}")
        if response.status_code == 200:
            data = response.json()
            print("Data received from CoinGecko:", data)  # Log para verificar a resposta completa
            return {
                "name": data.get("name", "N/A"),
                "symbol": data.get("symbol", "N/A"),
                "current_price": data["market_data"]["current_price"].get("usd", "N/A"),
                "market_cap": data["market_data"]["market_cap"].get("usd", "N/A"),
                "24h_change": data["market_data"].get("price_change_percentage_24h", "N/A")
            }
        else:
            print(f"Error fetching data: {response.status_code}, {response.text}")
            return {"error": "Failed to fetch data"}
    except Exception as e:
        print(f"Exception occurred: {e}")
        return {"error": "Failed to fetch data"}