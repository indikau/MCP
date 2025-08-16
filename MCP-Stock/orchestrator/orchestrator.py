from fastmcp import FastMCP
from dispatcher_logic import discover_trending_stocks

mcp = FastMCP("Orchestrator Agent")

@mcp.tool()
def discover_trending_stocks() -> list:
    """
    Retrieves trending stocks from multiple MCP servers.
    """
    trending = discover_trending_stocks()
    return trending

if __name__ == "__main__":
    mcp.run(transport="stdio")