from mcp.client import MCPClient
from shared_schema import format_output

client = MCPClient("http://localhost:8001")  # Replace with actual Finance MCP URL

def get_finance_trending():
    data = client.call_tool("get_news", {"sector": "technology"})
    results = []
    for item in data["articles"]:
        results.append(format_output(
            source="FinanceMCP",
            symbol=item["symbol"],
            sentiment_score=item["sentiment"],
            headline_count=item["count"],
            trend=item["trend"],
            confidence=item.get("confidence", 0.85)
        ))
    return results