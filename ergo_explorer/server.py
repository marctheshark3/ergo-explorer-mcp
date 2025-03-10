"""
Ergo Explorer MCP Server implementation.
"""

import asyncio
import httpx
import logging
from typing import Dict, List, Any, Optional
from mcp.server.fastmcp import FastMCP, Context, Image
from dataclasses import dataclass
from ergo_explorer.tools.node import (
    get_address_balance_from_node,
    analyze_transaction_from_node,
    get_transaction_history_from_node,
    get_network_status_from_node,
    search_for_token_from_node,
<<<<<<< HEAD
    get_node_wallet_info
=======
    # Tokenomics tools
    get_token_price_info,
    get_token_price_chart,
    get_liquidity_pool_info,
    get_token_swap_info,
    # Smart contract tools
    analyze_smart_contract,
    get_contract_statistics,
    simulate_contract_execution
>>>>>>> main
)
from ergo_explorer.api.explorer import (
    fetch_box as get_box_by_id_explorer,
    search_tokens as get_token_by_id_explorer
)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create MCP server
<<<<<<< HEAD
mcp = FastMCP("Ergo Explorer", dependencies=["httpx"])
=======
mcp = FastMCP(SERVER_NAME, dependencies=SERVER_DEPENDENCIES)
>>>>>>> main

# Log server initialization
logger.info("Initializing Ergo Explorer MCP server...")

# Constants
ERGO_EXPLORER_API = "https://api.ergoplatform.com/api/v1"
USER_AGENT = "ErgoMCPServer/1.0"

<<<<<<< HEAD
# Helper API functions
async def fetch_api(endpoint: str, params: Optional[Dict] = None) -> Dict:
    """Make a request to the Ergo Explorer API."""
    url = f"{ERGO_EXPLORER_API}/{endpoint}"
    async with httpx.AsyncClient() as client:
        headers = {"User-Agent": USER_AGENT}
        response = await client.get(url, headers=headers, params=params, timeout=30.0)
        response.raise_for_status()
        return response.json()
=======
# Register tokenomics MCP tools
mcp.tool()(get_token_price_info)
mcp.tool()(get_token_price_chart)
mcp.tool()(get_liquidity_pool_info)
mcp.tool()(get_token_swap_info)

# Register smart contract MCP tools
mcp.tool()(analyze_smart_contract)
mcp.tool()(get_contract_statistics)
mcp.tool()(simulate_contract_execution)

# Register MCP resources
mcp.resource("ergo://address/{address}/balance")(get_address_balance_resource)
mcp.resource("ergo://transaction/{tx_id}")(get_transaction_resource)
>>>>>>> main

async def fetch_balance(address: str) -> Dict:
    """Fetch the confirmed balance for an address."""
    return await fetch_api(f"addresses/{address}/balance/confirmed")

async def fetch_address_transactions(address: str, limit: int = 20, offset: int = 0) -> Dict:
    """Fetch transactions for an address."""
    params = {"limit": limit, "offset": offset}
    return await fetch_api(f"addresses/{address}/transactions", params=params)

async def fetch_transaction(tx_id: str) -> Dict:
    """Fetch details for a specific transaction."""
    return await fetch_api(f"transactions/{tx_id}")

async def fetch_block(block_id: str) -> Dict:
    """Fetch details for a specific block."""
    return await fetch_api(f"blocks/{block_id}")

async def fetch_network_state() -> Dict:
    """Fetch the current network state."""
    return await fetch_api("networkState")

async def fetch_box(box_id: str) -> Dict:
    """Fetch details for a specific box (UTXO)."""
    return await fetch_api(f"boxes/{box_id}")

async def search_tokens(query: str) -> Dict:
    """Search for tokens by ID or symbol."""
    params = {"query": query}
    return await fetch_api("tokens/search", params=params)

# MCP Tools
@mcp.tool()
async def get_address_balance(address: str) -> str:
    """Get the confirmed balance for an Ergo address.
    
    Args:
        address: Ergo blockchain address
    """
    try:
        balance = await fetch_balance(address)
        
        # Format ERG amount
        erg_amount = balance.get("nanoErgs", 0) / 1_000_000_000
        
        result = f"Balance for {address}:\n"
        result += f"• {erg_amount:.9f} ERG\n"
        
        # Format token balances
        tokens = balance.get("tokens", [])
        if tokens:
            result += "\nTokens:\n"
            for token in tokens:
                token_amount = token.get("amount", 0)
                token_name = token.get("name", "Unknown Token")
                token_id = token.get("tokenId", "")
                token_decimals = token.get("decimals", 0)
                
                # Format decimal amount correctly
                if token_decimals > 0:
                    token_formatted_amount = token_amount / (10 ** token_decimals)
                    result += f"• {token_formatted_amount} {token_name} (ID: {token_id[:8]}...)\n"
                else:
                    result += f"• {token_amount} {token_name} (ID: {token_id[:8]}...)\n"
        else:
            result += "\nNo tokens found."
            
        return result
    except Exception as e:
        return f"Error fetching balance: {str(e)}"

@mcp.tool()
async def analyze_transaction(tx_id: str) -> str:
    """Analyze a transaction on the Ergo blockchain.
    
    Args:
        tx_id: Transaction ID (hash)
    """
    try:
        tx = await fetch_transaction(tx_id)
        
        # Basic transaction info
        result = f"Transaction: {tx_id}\n"
        result += f"Block: {tx.get('blockId', 'Unknown')[:8]}...\n"
        result += f"Height: {tx.get('inclusionHeight', 'Unknown')}\n"
        result += f"Timestamp: {tx.get('timestamp', 0)}\n"
        result += f"Confirmations: {tx.get('numConfirmations', 0)}\n"
        result += f"Size: {tx.get('size', 0)} bytes\n\n"
        
        # Analyze inputs
        inputs = tx.get("inputs", [])
        total_input_value = sum(input.get("value", 0) for input in inputs)
        input_erg = total_input_value / 1_000_000_000
        
        result += f"Inputs: {len(inputs)}\n"
        result += f"Total Input Value: {input_erg:.9f} ERG\n"
        
        # Input addresses
        input_addresses = set()
        for input in inputs:
            addr = input.get("address")
            if addr:
                input_addresses.add(addr)
        
        if input_addresses:
            result += f"Input Addresses: {', '.join(list(input_addresses)[:3])}"
            if len(input_addresses) > 3:
                result += f" and {len(input_addresses) - 3} more"
            result += "\n\n"
        
        # Analyze outputs
        outputs = tx.get("outputs", [])
        total_output_value = sum(output.get("value", 0) for output in outputs)
        output_erg = total_output_value / 1_000_000_000
        
        result += f"Outputs: {len(outputs)}\n"
        result += f"Total Output Value: {output_erg:.9f} ERG\n"
        
        # Output addresses
        output_addresses = set()
        for output in outputs:
            addr = output.get("address")
            if addr:
                output_addresses.add(addr)
        
        if output_addresses:
            result += f"Output Addresses: {', '.join(list(output_addresses)[:3])}"
            if len(output_addresses) > 3:
                result += f" and {len(output_addresses) - 3} more"
            result += "\n\n"
        
        # Fee calculation
        fee = total_input_value - total_output_value
        fee_erg = fee / 1_000_000_000
        result += f"Fee: {fee_erg:.9f} ERG\n"
        
        # Token transfers
        input_tokens = {}
        for input in inputs:
            for asset in input.get("assets", []):
                token_id = asset.get("tokenId")
                token_amount = asset.get("amount", 0)
                token_name = asset.get("name", "Unknown")
                
                if token_id in input_tokens:
                    input_tokens[token_id]["amount"] += token_amount
                else:
                    input_tokens[token_id] = {
                        "amount": token_amount,
                        "name": token_name,
                        "decimals": asset.get("decimals", 0)
                    }
        
        output_tokens = {}
        for output in outputs:
            for asset in output.get("assets", []):
                token_id = asset.get("tokenId")
                token_amount = asset.get("amount", 0)
                token_name = asset.get("name", "Unknown")
                
                if token_id in output_tokens:
                    output_tokens[token_id]["amount"] += token_amount
                else:
                    output_tokens[token_id] = {
                        "amount": token_amount,
                        "name": token_name,
                        "decimals": asset.get("decimals", 0)
                    }
        
        if input_tokens or output_tokens:
            result += "\nToken Transfers:\n"
            
            all_token_ids = set(list(input_tokens.keys()) + list(output_tokens.keys()))
            for token_id in all_token_ids:
                input_amount = input_tokens.get(token_id, {}).get("amount", 0)
                output_amount = output_tokens.get(token_id, {}).get("amount", 0)
                token_name = input_tokens.get(token_id, output_tokens.get(token_id))["name"]
                decimals = input_tokens.get(token_id, output_tokens.get(token_id)).get("decimals", 0)
                
                # Format the amounts according to decimals
                if decimals > 0:
                    input_formatted = input_amount / (10 ** decimals)
                    output_formatted = output_amount / (10 ** decimals)
                    difference = output_formatted - input_formatted
                else:
                    input_formatted = input_amount
                    output_formatted = output_amount
                    difference = output_formatted - input_formatted
                
                result += f"• {token_name} (ID: {token_id[:8]}...): "
                if difference > 0:
                    result += f"Minted {difference}\n"
                elif difference < 0:
                    result += f"Burned {abs(difference)}\n"
                else:
                    result += f"Transferred {input_formatted}\n"
        
        return result
    except Exception as e:
        return f"Error analyzing transaction: {str(e)}"

@mcp.tool()
async def get_transaction_history(address: str, limit: int = 20) -> str:
    """Get the transaction history for an Ergo address.
    
    Args:
        address: Ergo blockchain address
        limit: Maximum number of transactions to retrieve (default: 20)
    """
    try:
        tx_data = await fetch_address_transactions(address, limit=limit)
        transactions = tx_data.get("items", [])
        total = tx_data.get("total", 0)
        
        if not transactions:
            return f"No transactions found for address {address}"
        
        result = f"Transaction History for {address}\n"
        result += f"Showing {len(transactions)} of {total} total transactions\n\n"
        
        for tx in transactions:
            tx_id = tx.get("id", "Unknown")
            timestamp = tx.get("timestamp", 0)
            confirmations = tx.get("numConfirmations", 0)
            
            # Calculate value transferred
            inputs = tx.get("inputs", [])
            outputs = tx.get("outputs", [])
            
            # Track if this address is input or output
            is_input = any(input.get("address") == address for input in inputs)
            is_output = any(output.get("address") == address for output in outputs)
            
            # Calculate relevant value
            if is_input and is_output:
                direction = "SELF"
                relevant_value = sum(
                    output.get("value", 0) for output in outputs 
                    if output.get("address") == address
                )
            elif is_input:
                direction = "OUT"
                relevant_value = sum(
                    output.get("value", 0) for output in outputs 
                    if output.get("address") != address
                )
            else:
                direction = "IN"
                relevant_value = sum(
                    output.get("value", 0) for output in outputs 
                    if output.get("address") == address
                )
            
            value_erg = relevant_value / 1_000_000_000
            
            result += f"TX: {tx_id[:8]}...\n"
            result += f"Type: {direction}\n"
            result += f"Value: {value_erg:.9f} ERG\n"
            result += f"Confirmations: {confirmations}\n"
            result += f"Timestamp: {timestamp}\n\n"
        
        return result
    except Exception as e:
        return f"Error fetching transaction history: {str(e)}"

@mcp.tool()
async def analyze_address(address: str, depth: int = 2, tx_limit: int = 5) -> str:
    """Perform a deep analysis of an Ergo address, including transaction patterns and token holdings.
    
    Args:
        address: Ergo blockchain address
        depth: How many levels of related addresses to analyze (default: 2)
        tx_limit: Maximum number of transactions to analyze per address (default: 5)
    """
    try:
        result = f"Deep Analysis of Address: {address}\n\n"
        
        # Get initial balance
        balance = await fetch_balance(address)
        erg_amount = balance.get("nanoErgs", 0) / 1_000_000_000
        result += f"Current Balance: {erg_amount:.9f} ERG\n"
        
        # Token holdings
        tokens = balance.get("tokens", [])
        if tokens:
            result += "\nToken Holdings:\n"
            for token in tokens:
                token_amount = token.get("amount", 0)
                token_name = token.get("name", "Unknown Token")
                token_id = token.get("tokenId", "")
                token_decimals = token.get("decimals", 0)
                
                if token_decimals > 0:
                    token_formatted_amount = token_amount / (10 ** token_decimals)
                    result += f"• {token_formatted_amount} {token_name} (ID: {token_id[:8]}...)\n"
                else:
                    result += f"• {token_amount} {token_name} (ID: {token_id[:8]}...)\n"
        
        # Transaction analysis
        tx_data = await fetch_address_transactions(address, limit=tx_limit)
        transactions = tx_data.get("items", [])
        total_txs = tx_data.get("total", 0)
        
        result += f"\nTransaction Analysis:\n"
        result += f"Total Transactions: {total_txs}\n"
        
        if transactions:
            # Analyze transaction patterns
            incoming = 0
            outgoing = 0
            total_incoming_value = 0
            total_outgoing_value = 0
            
            for tx in transactions:
                inputs = tx.get("inputs", [])
                outputs = tx.get("outputs", [])
                
                is_input = any(input.get("address") == address for input in inputs)
                is_output = any(output.get("address") == address for output in outputs)
                
                if is_input:
                    outgoing += 1
                    total_outgoing_value += sum(
                        output.get("value", 0) for output in outputs 
                        if output.get("address") != address
                    )
                
                if is_output:
                    incoming += 1
                    total_incoming_value += sum(
                        output.get("value", 0) for output in outputs 
                        if output.get("address") == address
                    )
            
            result += f"Recent Activity:\n"
            result += f"• Incoming Transactions: {incoming}\n"
            result += f"• Outgoing Transactions: {outgoing}\n"
            result += f"• Total Received: {total_incoming_value / 1_000_000_000:.9f} ERG\n"
            result += f"• Total Sent: {total_outgoing_value / 1_000_000_000:.9f} ERG\n"
        
        return result
    except Exception as e:
        return f"Error analyzing address: {str(e)}"

@mcp.tool()
async def search_for_token(query: str) -> str:
    """Search for tokens on the Ergo blockchain.
    
    Args:
        query: Token ID or name to search for
    """
    try:
        tokens = await search_tokens(query)
        
        if not tokens:
            return f"No tokens found matching '{query}'"
        
        result = f"Token Search Results for '{query}':\n\n"
        
        for token in tokens:
            token_id = token.get("id", "Unknown")
            name = token.get("name", "Unknown Token")
            description = token.get("description", "No description")
            decimals = token.get("decimals", 0)
            
            result += f"Token: {name}\n"
            result += f"ID: {token_id}\n"
            result += f"Decimals: {decimals}\n"
            result += f"Description: {description}\n\n"
        
        return result
    except Exception as e:
        return f"Error searching for token: {str(e)}"

@mcp.tool()
async def get_network_status() -> str:
    """Get the current status of the Ergo network."""
    try:
        state = await fetch_network_state()
        
        result = "Ergo Network Status:\n"
        result += f"Height: {state.get('height', 'Unknown')}\n"
        result += f"State Type: {state.get('stateType', 'Unknown')}\n"
        result += f"Difficulty: {state.get('difficulty', 'Unknown')}\n"
        
        # Add more network stats as needed
        
        return result
    except Exception as e:
        return f"Error fetching network status: {str(e)}"

@mcp.resource("ergo://address/{address}/balance")
async def get_address_balance_resource(address: str) -> str:
    """Resource handler for address balance."""
    return await get_address_balance(address)

@mcp.resource("ergo://transaction/{tx_id}")
async def get_transaction_resource(tx_id: str) -> str:
    """Resource handler for transaction analysis."""
    return await analyze_transaction(tx_id)

@mcp.prompt()
def check_balance_prompt(address: str) -> str:
    """Generate a prompt for checking an address balance."""
    return f"Let me check the balance for address {address}..."

@mcp.prompt()
def analyze_transaction_prompt(tx_id: str) -> str:
    """Generate a prompt for analyzing a transaction."""
    return f"Analyzing transaction {tx_id}..."

@mcp.prompt()
def forensic_analysis_prompt(address: str, depth: int = 2, tx_limit: int = 5) -> str:
    """Generate a prompt for deep address analysis."""
    return f"Performing deep analysis of address {address} with depth {depth} and transaction limit {tx_limit}..."

@mcp.prompt()
def node_wallet_prompt() -> str:
    """Generate a prompt for node wallet info."""
    return "Fetching node wallet information..."

@mcp.tool()
async def get_node_wallet() -> str:
    """Get information about the connected node's wallet."""
    try:
        return await get_node_wallet_info()
    except Exception as e:
        return f"Error fetching node wallet info: {str(e)}"

def run_server():
    """Run the MCP server."""
    mcp.run()

# Export the server instance
__all__ = ["mcp", "run_server"]
