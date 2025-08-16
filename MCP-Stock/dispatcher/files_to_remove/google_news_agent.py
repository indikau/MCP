from mcp.client import MCPClient
from shared_schema import format_output

client = MCPClient("http://localhost:8003")  # Replace with actual Google News MCP URL

def get_google_trending():
    keywords = client.call_tool("get_trending_keywords", {"location": "US"})
    results = []
    for keyword in keywords["trending"]:
        results.append(format_output(
            source="GoogleNewsTrends",
            symbol=keyword["symbol"],
            sentiment_score=keyword["score"],
            headline_count=keyword["count"],
            trend=keyword["trend"],
            confidence=keyword.get("confidence", 0.88)
        ))
    return results