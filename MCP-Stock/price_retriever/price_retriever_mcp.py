# filename: price_retriever_mcp.py

import os, requests
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env


ALPHA_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
# print("ALPHA_KEY:", ALPHA_KEY)  # Debugging line to check if the key is loaded
FINNHUB_KEY = os.getenv("FINNHUB_API_KEY")
# print("FINNHUB_KEY:", FINNHUB_KEY)  # Debugging line to check if the key is loaded
mcp = FastMCP("MultiSource Price Retriever")

def fetch_alpha_vantage(symbol):
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": ALPHA_KEY
    }
    try:
        resp = requests.get(url, params=params, timeout=5)
        print("AlphaVantage response:", resp.json())  # Add this line
        data = resp.json().get("Global Quote", {})
        return {
            "source": "AlphaVantage",
            "symbol": symbol,
            "price": float(data.get("05. price", 0)),
            "change_percent": float(data.get("10. change percent", "0%").strip('%'))
        }
    except Exception as e:
        print(f"AlphaVantage failed: {e}")
        return None

def fetch_finnhub(symbol):
    url = f"https://finnhub.io/api/v1/quote"
    params = {
        "symbol": symbol,
        "token": FINNHUB_KEY
    }
    try:
        resp = requests.get(url, params=params, timeout=5)
        print("finnhub response:", resp.json())
        data = resp.json()
        return {
            "source": "Finnhub",
            "symbol": symbol,
            "price": float(data.get("c", 0)),
            "change_percent": float(data.get("dp", 0))
        }
    except Exception as e:
        print(f"Finnhub failed: {e}")
        return None

@mcp.tool()
def get_stock_price(symbol: str) -> dict:
    """Fetch stock price and % change from multiple sources with fallback."""
    result = fetch_alpha_vantage(symbol)
    if result:
        return result
    fallback = fetch_finnhub(symbol)
    if fallback:
        return fallback
    return {
        "source": "None",
        "symbol": symbol,
        "price": None,
        "change_percent": None,
        "error": "All sources failed"
    }

if __name__ == "__main__":
    print(get_stock_price("AAPL"))  # Example symbol
# ...existing code...
    mcp.run(transport="stdio")