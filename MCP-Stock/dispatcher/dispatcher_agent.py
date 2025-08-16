import os
import pandas as pd
import sqlite3
from dotenv import load_dotenv
from fastmcp import Client
from shared_schema import format_output

load_dotenv()

OUTPUT_MODE = os.getenv("OUTPUT_MODE", "csv")
CSV_PATH = os.getenv("CSV_PATH", "output/sentiment_log.csv")
SQLITE_PATH = os.getenv("SQLITE_PATH", "output/sentiment_log.db")

SOURCES = {
    "StockSense": os.getenv("STOCKSENSE_URL"),
    "Finance": os.getenv("FINANCE_URL"),
    "YahooFinance": os.getenv("YAHOO_URL"),
    "GoogleNewsTrends": os.getenv("GOOGLE_NEWS_URL"),
    "Tavily": os.getenv("TAVILY_URL")
}

import asyncio

async def query_mcp_server(name, url):
    try:
        tool_name = "get_trending_stocks"
        async with Client(url) as client:
            result = await client.call_tool(tool_name, {})
            formatted = [
                format_output(
                    source=name,
                    symbol=item["symbol"],
                    sentiment_score=item["sentiment_score"],
                    headline_count=item["headline_count"],
                    trend=item["trend"],
                    confidence=item.get("confidence", 0.9)
                ) for item in result["stocks"]
            ]
            return formatted
    except Exception as e:
        print(f"⚠️ {name} failed: {e}")
        return []

async def collect_all_sources():
    tasks = [query_mcp_server(name, url) for name, url in SOURCES.items()]
    results = await asyncio.gather(*tasks)
    all_data = []
    for result in results:
        all_data.extend(result)
    return all_data

def save_to_csv(data):
    df = pd.DataFrame(data)
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    if os.path.exists(CSV_PATH):
        df.to_csv(CSV_PATH, mode="a", header=False, index=False)
    else:
        df.to_csv(CSV_PATH, index=False)

def save_to_sqlite(data):
    df = pd.DataFrame(data)
    os.makedirs(os.path.dirname(SQLITE_PATH), exist_ok=True)
    conn = sqlite3.connect(SQLITE_PATH)
    df.to_sql("sentiment_log", conn, if_exists="append", index=False)
    conn.close()

async def run_dispatcher():
    data = await collect_all_sources()
    if OUTPUT_MODE == "csv":
        save_to_csv(data)
        print(f"✅ Saved to CSV: {CSV_PATH}")
    elif OUTPUT_MODE == "sqlite":
        save_to_sqlite(data)
        print(f"✅ Saved to SQLite: {SQLITE_PATH}")
    else:
        print("❌ Invalid OUTPUT_MODE")

if __name__ == "__main__":
    asyncio.run(run_dispatcher())