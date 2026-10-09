# creating MCP server instance
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("MY_KITCHEN")# server name is MY_KITCHEN


@mcp.tool()
def padho_add(a: int, b: int) -> int:
    """Adds two numbers."""
    return a + b + 100  # Deliberate bug for testing


if __name__ == "__main__":
    mcp.run()
