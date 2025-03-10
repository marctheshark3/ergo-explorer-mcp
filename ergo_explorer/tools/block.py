"""
Block-related tools for the Ergo Explorer MCP server.

This module provides tools for interacting with Ergo blockchain blocks:
- Retrieving blocks by height
- Retrieving blocks by hash
- Getting latest blocks
- Fetching transactions from a block
"""

import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

from ergo_explorer.api.explorer import (
    fetch_api, 
    fetch_block, 
    fetch_blocks_at_height,
    fetch_latest_blocks,
    fetch_block_transactions
)

# Set up logging
logger = logging.getLogger(__name__)

async def get_block_by_height(height: int) -> Dict:
    """
    Fetch a block by its height from the Ergo blockchain.
    
    Args:
        height: The height of the block to fetch
        
    Returns:
        A dictionary containing block data
    """
    try:
        logger.info(f"Fetching block at height {height}")
        # Use the at endpoint to get block at specific height
        response = await fetch_blocks_at_height(height)
        # The response contains an array of blocks at the specific height
        # Normally there should be only one block at a given height
        if response and isinstance(response, list) and len(response) > 0:
            # Get the block ID from the response
            block_id = response[0]["id"]
            # Fetch the complete block data using the ID
            block_data = await fetch_block(block_id)
            return block_data
        else:
            logger.warning(f"No block found at height {height}")
            return {"error": f"No block found at height {height}"}
    except Exception as e:
        logger.error(f"Error fetching block at height {height}: {str(e)}")
        return {"error": f"Error fetching block: {str(e)}"}

async def get_block_by_hash(block_hash: str) -> Dict:
    """
    Fetch a block by its hash from the Ergo blockchain.
    
    Args:
        block_hash: The hash (ID) of the block to fetch
        
    Returns:
        A dictionary containing block data
    """
    try:
        logger.info(f"Fetching block with hash {block_hash}")
        block_data = await fetch_block(block_hash)
        return block_data
    except Exception as e:
        logger.error(f"Error fetching block with hash {block_hash}: {str(e)}")
        return {"error": f"Error fetching block: {str(e)}"}

async def get_latest_blocks(limit: int = 10) -> Dict:
    """
    Fetch the latest blocks from the Ergo blockchain.
    
    Args:
        limit: Maximum number of blocks to retrieve (default: 10)
        
    Returns:
        A dictionary containing the latest blocks
    """
    try:
        logger.info(f"Fetching latest {limit} blocks")
        response = await fetch_latest_blocks(limit=limit)
        return response
    except Exception as e:
        logger.error(f"Error fetching latest blocks: {str(e)}")
        return {"error": f"Error fetching latest blocks: {str(e)}"}

async def get_block_transactions(block_id: str, limit: int = 100) -> Dict:
    """
    Fetch transactions from a specific block.
    
    Args:
        block_id: The ID of the block
        limit: Maximum number of transactions to retrieve (default: 100)
        
    Returns:
        A dictionary containing the block's transactions
    """
    try:
        logger.info(f"Fetching transactions for block {block_id}")
        response = await fetch_block_transactions(block_id, limit=limit)
        return response
    except Exception as e:
        logger.error(f"Error fetching transactions for block {block_id}: {str(e)}")
        return {"error": f"Error fetching block transactions: {str(e)}"}

async def format_block_data(block_data: Dict) -> str:
    """
    Format block data into a readable string.
    
    Args:
        block_data: The block data to format
        
    Returns:
        A formatted string representation of the block data
    """
    if "error" in block_data:
        return block_data["error"]
    
    # Extract relevant information from the block data
    block_info = {
        "height": block_data.get("height"),
        "id": block_data.get("id"),
        "timestamp": block_data.get("timestamp"),
        "transactionsCount": block_data.get("transactionsCount"),
        "size": block_data.get("size"),
        "difficulty": block_data.get("difficulty"),
        "miner": block_data.get("miner", {}).get("name", "Unknown"),
        "minerAddress": block_data.get("miner", {}).get("address", "Unknown"),
        "minerReward": block_data.get("minerReward") / 1000000000 if block_data.get("minerReward") else 0,
        "blockTime": block_data.get("blockTime"),
        "mainChain": block_data.get("mainChain", False),
    }
    
    # Format timestamp
    if block_info["timestamp"]:
        timestamp = datetime.fromtimestamp(block_info["timestamp"] / 1000)
        formatted_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")
    else:
        formatted_timestamp = "Unknown"
    
    # Create a formatted string
    formatted_output = f"""
## Block Details

- **Height**: {block_info['height']}
- **ID**: {block_info['id']}
- **Timestamp**: {formatted_timestamp}
- **Transactions**: {block_info['transactionsCount']}
- **Size**: {block_info['size']} bytes
- **Difficulty**: {block_info['difficulty']}
- **Miner**: {block_info['miner']}
- **Miner Address**: {block_info['minerAddress']}
- **Miner Reward**: {block_info['minerReward']} ERG
- **Block Time**: {block_info['blockTime']} ms
- **Main Chain**: {block_info['mainChain']}
"""
    return formatted_output

async def format_latest_blocks(blocks_data: Dict) -> str:
    """
    Format latest blocks data into a readable string.
    
    Args:
        blocks_data: The blocks data to format
        
    Returns:
        A formatted string representation of the latest blocks
    """
    if "error" in blocks_data:
        return blocks_data["error"]
    
    if "items" not in blocks_data or not blocks_data["items"]:
        return "No blocks found."
    
    blocks = blocks_data["items"]
    formatted_output = "## Latest Blocks\n\n"
    
    for block in blocks:
        # Format timestamp
        if block.get("timestamp"):
            timestamp = datetime.fromtimestamp(block["timestamp"] / 1000)
            formatted_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")
        else:
            formatted_timestamp = "Unknown"
        
        miner_name = block.get("miner", {}).get("name", "Unknown")
        miner_reward = block.get("minerReward", 0) / 1000000000  # Convert nanoERG to ERG
        
        formatted_output += f"""
### Block {block.get('height')}
- **ID**: {block.get('id')}
- **Timestamp**: {formatted_timestamp}
- **Transactions**: {block.get('transactionsCount')}
- **Size**: {block.get('size')} bytes
- **Miner**: {miner_name}
- **Reward**: {miner_reward} ERG
"""
    
    return formatted_output

async def format_block_transactions(tx_data: Dict, block_id: str) -> str:
    """
    Format block transactions data into a readable string.
    
    Args:
        tx_data: The transactions data to format
        block_id: The ID of the block
        
    Returns:
        A formatted string representation of the block transactions
    """
    if "error" in tx_data:
        return tx_data["error"]
    
    if "items" not in tx_data or not tx_data["items"]:
        return f"No transactions found for block {block_id}."
    
    transactions = tx_data["items"]
    formatted_output = f"## Transactions in Block {block_id}\n\n"
    
    for idx, tx in enumerate(transactions, 1):
        tx_id = tx.get("id", "Unknown")
        tx_size = tx.get("size", 0)
        
        inputs_count = len(tx.get("inputs", []))
        outputs_count = len(tx.get("outputs", []))
        
        # Calculate total value
        total_value = sum([output.get("value", 0) for output in tx.get("outputs", [])])
        total_value_erg = total_value / 1000000000  # Convert nanoERG to ERG
        
        formatted_output += f"""
### Transaction {idx}
- **ID**: {tx_id}
- **Size**: {tx_size} bytes
- **Inputs**: {inputs_count}
- **Outputs**: {outputs_count}
- **Total Value**: {total_value_erg} ERG
"""
    
    return formatted_output 