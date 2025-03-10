"""
Ergo Node API client for direct node interaction.
"""
import httpx
from typing import Dict, List, Any, Optional
from ergo_explorer.config import ERGO_NODE_API, ERGO_NODE_API_KEY, USER_AGENT

async def fetch_node_api(endpoint: str, params: Optional[Dict] = None, method: str = "GET", json_data: Optional[Dict] = None) -> Dict:
    """Make a request to the Ergo Node API."""
    url = f"{ERGO_NODE_API}/{endpoint}"
    async with httpx.AsyncClient() as client:
        headers = {
            "User-Agent": USER_AGENT,
            "Content-Type": "application/json"
        }
        
        # Add API key if available
        if ERGO_NODE_API_KEY:
            headers["api_key"] = ERGO_NODE_API_KEY
            
        if method == "GET":
            response = await client.get(url, headers=headers, params=params, timeout=30.0)
        elif method == "POST":
            response = await client.post(url, headers=headers, params=params, json=json_data, timeout=30.0)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
            
        response.raise_for_status()
        return response.json()

# Address-related endpoints
async def get_address_balance_node(address: str) -> Dict:
    """Get the confirmed balance for an address directly from the node."""
    return await fetch_node_api(f"blockchain/balance", method="POST", json_data=address)

# Transaction-related endpoints
async def get_transaction_node(tx_id: str) -> Dict:
    """Get transaction details directly from the node."""
    return await fetch_node_api(f"blockchain/transaction/byId/{tx_id}")

async def get_transaction_by_address_node(address: str, offset: int = 0, limit: int = 20) -> Dict:
    """Get transactions for an address directly from the node."""
    return await fetch_node_api(f"blockchain/transaction/byAddress", 
                               method="POST", 
                               json_data=address,
                               params={"offset": offset, "limit": limit})

async def submit_transaction_node(tx_data: Dict) -> Dict:
    """Submit a transaction to the node."""
    return await fetch_node_api("transactions", method="POST", json_data=tx_data)

# Box-related endpoints
async def get_box_by_id_node(box_id: str) -> Dict:
    """Get box details directly from the node."""
    return await fetch_node_api(f"blockchain/box/byId/{box_id}")

async def get_box_by_address_node(address: str, offset: int = 0, limit: int = 20) -> Dict:
    """Get boxes for an address directly from the node."""
    return await fetch_node_api(f"blockchain/box/byAddress", 
                               method="POST", 
                               json_data=address,
                               params={"offset": offset, "limit": limit})

async def get_unspent_boxes_by_address_node(address: str, offset: int = 0, limit: int = 20) -> Dict:
    """Get unspent boxes for an address directly from the node."""
    return await fetch_node_api(f"blockchain/box/unspent/byAddress", 
                               method="POST", 
                               json_data=address,
                               params={"offset": offset, "limit": limit})

# Token-related endpoints
async def get_token_by_id_node(token_id: str) -> Dict:
    """Get token details directly from the node."""
    return await fetch_node_api(f"blockchain/token/byId/{token_id}")

async def search_for_token_node(query: str) -> Dict:
    """Search for tokens on the node."""
    return await fetch_node_api("search_for_token", method="POST", json_data={"query": query})

# Utility endpoints
async def get_network_info_node() -> Dict:
    """Get network information directly from the node."""
    return await fetch_node_api("info")

async def get_node_wallet_addresses() -> List[str]:
    """Get all wallet addresses from the node wallet."""
    return await fetch_node_api("wallet/addresses")

# Mempool-related endpoints
async def get_mempool_transactions_node(offset: int = 0, limit: int = 100) -> Dict:
    """
    Get transactions currently in the mempool.
    
    Args:
        offset: Number of transactions to skip
        limit: Maximum number of transactions to return
        
    Returns:
        A dictionary containing mempool transactions
    """
    return await fetch_node_api("transactions/unconfirmed", params={"offset": offset, "limit": limit})

async def get_mempool_size_node() -> Dict:
    """
    Get the current size of the mempool.
    
    Returns:
        A dictionary containing the mempool size
    """
    return await fetch_node_api("transactions/unconfirmed/size")

async def get_mempool_statistics_node() -> Dict:
    """
    Get detailed statistics about the mempool.
    
    Returns:
        A dictionary containing mempool statistics
    """
    # Fetch both the mempool transactions and size
    transactions = await get_mempool_transactions_node(limit=1000)  # Get up to 1000 transactions
    size = await get_mempool_size_node()
    
    # Combine the data
    mempool_data = {
        "size": size.get("size", 0),
        "transactions": transactions
    }
    
    return mempool_data 