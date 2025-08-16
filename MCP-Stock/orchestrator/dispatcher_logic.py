import os
import pandas as pd
import sqlite3
from dotenv import load_dotenv
from mcp.client import MCPClient
from datetime import datetime

# Load environment variables
load_dotenv()

# Output settings
OUTPUT_MODE = os.getenv("OUTPUT_MODE", "csv").lower()
CSV_PATH = os.getenv("CSV_PATH", "output/sentiment_log.csv")
SQLITE_PATH = os.getenv("SQLITE_PATH", "output/sentiment_log.db")

# MCP server URLs
SOURCES = {
    "StockSense": os.getenv("STOCKSENSE_URL"),
    "Finance": os.getenv("FINANCE_URL"),
    "YahooFinance": os.getenv("YAHOO_URL"),
    "GoogleNewsTrends": os.getenv("GOOGLE_NEWS_URL"),
    "Tavily": os.getenv("TAVILY_URL")
}

def format_output(source, symbol, sentiment_score, headline_count, trend, confidence):
    return {
        "timestamp": datetime.now().isoformat(),
        "source": source,
        "symbol": symbol,
        "sentiment_score": sentiment_score,
        "headline_count": headline_count,
        "trend": trend,
        "confidence": confidence
    }

def query_mcp_server(name, url):
    try:
        client = MCPClient(url)
        result = client.call_tool("get_trending_stocks", {})
        formatted = [
            format_output(
                source=name,
                symbol=item["symbol"],
                sentiment_score=item["sentiment_score"],
                headline_count=item.get("headline_count", 1),
                trend=item.get("trend", "Neutral"),
                confidence=item.get("confidence", 0.9)
            ) for item in result["stocks"]
        ]
        return formatted
    except Exception as e:
        print(f"⚠️ Failed to fetch from {name}: {e}")
        return []

def discover_trending_stocks():
    all_trending = []
    for name, url in SOURCES.items():
        if url:
            all_trending.extend(query_mcp_server(name, url))
    return all_trending

def save_to_csv(data):
    df = pd.DataFrame(data)
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    if os.path.exists(CSV_PATH):
        df.to_csv(CSV_PATH, mode='a', header=False, index=False)
    else:
        df.to_csv(CSV_PATH, index=False)

def save_to_sqlite(data):
    df = pd.DataFrame(data)
    os.makedirs(os.path.dirname(SQLITE_PATH), exist_ok=True)
    conn = sqlite3.connect(SQLITE_PATH)
    df.to_sql("sentiment_log", conn, if_exists="append", index=False)
    conn.close()

def run_dispatcher():
    print("🚀 Running Dispatcher...")
    data = discover_trending_stocks()
    if not data:
        print("⚠️ No data retrieved.")
        return

    if OUTPUT_MODE == "csv":
        save_to_csv(data)
        print(f"✅ Saved to CSV: {CSV_PATH}")
    elif OUTPUT_MODE == "sqlite":
        save_to_sqlite(data)
        print(f"✅ Saved to SQLite: {SQLITE_PATH}")
    else:
        print(f"❌ Invalid OUTPUT_MODE '{OUTPUT_MODE}' specified in .env")

if __name__ == "__main__":
    run_dispatcher()