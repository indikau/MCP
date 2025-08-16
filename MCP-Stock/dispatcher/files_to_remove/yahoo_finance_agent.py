from mcp.client import MCPClient
from shared_schema import format_output

client = MCPClient("http://localhost:8002")  # Replace with actual Yahoo MCP URL

def get_yahoo_trending():
    news = client.call_tool("get_yahoo_finance_news", {"ticker": "AAPL"})
    results = []
    for article in news["articles"]:
        results.append(format_output(
            source="YahooFinance",
            symbol="AAPL",
            sentiment_score=article["sentiment"],
            headline_count=1,
            trend="Bullish" if article["sentiment"] > 0.5 else "Neutral",
            confidence=0.9
        ))
    return results