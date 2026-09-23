from mcp.server import MCPServer

mcp = MCPServer("Research Tools")


@mcp.tool()
def get_research_sources() -> list[str]:
    """Provides a list of research sources."""
    search_sources = [
        "Wikipedia",
        "Google",
        "YouTube",
    ]
    return search_sources