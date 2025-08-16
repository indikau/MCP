from mcp.client import MCPClient
from shared_schema import format_output

client = MCPClient("https://stocksense.glama.ai")  # Replace with actual StockSense MCP URL

def get_stocksense_trending():
    trending = client.call_tool("track_market_trends", {})
    results = []
    for item in trending["stocks"]:
        results.append(format_output(
            source="StockSense",
            symbol=item["symbol"],
            sentiment_score=item["sentiment_score"],
            headline_count=item["headline_count"],
            trend=item["trend"],
            confidence=item["confidence"]
        ))
    return results