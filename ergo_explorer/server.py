"""
Main server module for the Ergo Explorer MCP server.
"""

from datetime import datetime
from mcp.server.fastmcp import FastMCP, Image
from ergo_explorer.config import SERVER_NAME, SERVER_PORT, SERVER_DEPENDENCIES
from ergo_explorer.tools import (
    get_address_balance,
    get_transaction_history,
    analyze_address,
    analyze_transaction,
    search_for_token,
    get_network_status,
    get_address_balance_from_node,
    analyze_transaction_from_node,
    get_transaction_history_from_node,
    get_network_status_from_node,
    search_for_token_from_node
)
from ergo_explorer.resources import (
    get_address_balance_resource,
    get_transaction_resource,
    get_address_balance_node_resource,
    get_transaction_node_resource
)
from ergo_explorer.prompts import (
    check_balance_prompt,
    analyze_transaction_prompt,
    forensic_analysis_prompt
)

# Create MCP server
mcp = FastMCP(SERVER_NAME, dependencies=SERVER_DEPENDENCIES)

# Register MCP tools
mcp.tool()(get_address_balance)
mcp.tool()(get_transaction_history)
mcp.tool()(analyze_address)
mcp.tool()(analyze_transaction)
mcp.tool()(search_for_token)
mcp.tool()(get_network_status)

# Register node-specific MCP tools
mcp.tool()(get_address_balance_from_node)
mcp.tool()(analyze_transaction_from_node)
mcp.tool()(get_transaction_history_from_node)
mcp.tool()(get_network_status_from_node)
mcp.tool()(search_for_token_from_node)

# Register MCP resources
mcp.resource("ergo://address/{address}/balance")(get_address_balance_resource)
mcp.resource("ergo://transaction/{tx_id}")(get_transaction_resource)

# Register node-specific MCP resources
mcp.resource("ergo://node/address/{address}/balance")(get_address_balance_node_resource)
mcp.resource("ergo://node/transaction/{tx_id}")(get_transaction_node_resource)

# Register MCP prompts
mcp.prompt()(check_balance_prompt)
mcp.prompt()(analyze_transaction_prompt)
mcp.prompt()(forensic_analysis_prompt)

def run_server():
    """Run the MCP server."""
    mcp.run()

if __name__ == "__main__":
    run_server()
