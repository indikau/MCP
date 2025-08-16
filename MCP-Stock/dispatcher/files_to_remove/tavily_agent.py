from mcp.client import MCPClient
from shared_schema import format_output

client = MCPClient("http://localhost:8004")  # Replace with actual Tavily MCP URL

def get_tavily_trending():
    news = client.call_tool("tavily_news_search", {"query": "AI stocks", "days": 3})
    results = []
    for article in news["results"]:
        results.append(format_output(
            source="Tavily",
            symbol=article["symbol"],
            sentiment_score=article["sentiment"],
            headline_count=1,
            trend=article["trend"],
            confidence=article.get("confidence", 0.9)
        ))
    return results