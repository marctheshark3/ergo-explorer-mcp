"""
Token-related tools for the Ergo Explorer MCP server.

This module provides tools for interacting with Ergo tokens:
- Get token price
- Get token information
- Get token price history
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

from ergo_explorer.api.ergodex import get_token_price as fetch_token_price, get_erg_price_usd

# Set up logging
logger = logging.getLogger(__name__)

async def get_token_price(token_id: str) -> Dict:
    """
    Get the current price of a token in ERG and USD.
    
    Args:
        token_id: ID of the token to check
        
    Returns:
        A dictionary containing price information
    """
    try:
        logger.info(f"Fetching price for token {token_id}")
        
        # Get token price in ERG
        price_data = await fetch_token_price(token_id)
        
        if "error" in price_data:
            return price_data
        
        # Get ERG price in USD to calculate token price in USD
        erg_price_usd = await get_erg_price_usd()
        
        # Calculate token price in USD
        price_in_erg = price_data.get("priceInErg", 0)
        price_in_usd = price_in_erg * erg_price_usd
        
        # Add USD price to the data
        price_data["priceInUsd"] = price_in_usd
        price_data["ergPriceUsd"] = erg_price_usd
        price_data["timestamp"] = datetime.now().timestamp() * 1000  # current time in milliseconds
        
        return price_data
    except Exception as e:
        logger.error(f"Error fetching token price: {str(e)}")
        return {"error": f"Error fetching token price: {str(e)}"}

async def format_token_price(price_data: Dict) -> str:
    """
    Format token price data into a readable string.
    
    Args:
        price_data: The price data to format
        
    Returns:
        A formatted string representation of the token price data
    """
    if "error" in price_data:
        return price_data["error"]
    
    # Extract relevant information
    token_id = price_data.get("tokenId", "Unknown")
    token_name = price_data.get("tokenName", "Unknown")
    token_ticker = price_data.get("tokenTicker", "Unknown")
    
    price_in_erg = price_data.get("priceInErg", 0)
    price_in_usd = price_data.get("priceInUsd", 0)
    erg_price_usd = price_data.get("ergPriceUsd", 0)
    
    # Get liquidity information
    liquidity_erg = price_data.get("liquidityErg", 0)
    liquidity_token = price_data.get("liquidityToken", 0)
    
    # Format timestamp
    if "timestamp" in price_data:
        timestamp = datetime.fromtimestamp(price_data["timestamp"] / 1000)
        formatted_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")
    else:
        formatted_timestamp = "Unknown"
    
    # Create a formatted string
    formatted_output = f"""
## Token Price Information

### {token_name} ({token_ticker})
- **Token ID**: {token_id}
- **Timestamp**: {formatted_timestamp}

### Price
- **Price in ERG**: {price_in_erg:.8f} ERG
- **Price in USD**: ${price_in_usd:.6f}
- **Current ERG Price**: ${erg_price_usd:.2f}

### Liquidity
- **ERG in Pool**: {liquidity_erg:.2f} ERG
- **Tokens in Pool**: {liquidity_token:,.2f} {token_ticker}
"""
    
    # Add pool information
    pool_id = price_data.get("poolId", None)
    if pool_id:
        dex_name = price_data.get("dexName", "Unknown DEX")
        formatted_output += f"""
### Source
- **DEX**: {dex_name}
- **Pool ID**: {pool_id}
"""
    
    # Add price change if available
    price_change_24h = price_data.get("priceChange24h", None)
    if price_change_24h is not None:
        change_direction = "increase" if price_change_24h >= 0 else "decrease"
        formatted_output += f"""
### Price Change
- **24h Change**: {abs(price_change_24h):.2f}% {change_direction}
"""
    
    return formatted_output 