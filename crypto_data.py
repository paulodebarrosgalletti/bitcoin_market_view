import requests

def get_crypto_data(crypto_id):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "name": data["name"],
            "symbol": data["symbol"],
            "current_price": data["market_data"]["current_price"]["usd"],
            "market_cap": data["market_data"]["market_cap"]["usd"],
            "24h_change": data["market_data"]["price_change_percentage_24h"]
        }
    else:
        return {"error": "Failed to fetch data"}
