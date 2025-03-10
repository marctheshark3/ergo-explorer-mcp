"""
Network-related tools for the Ergo Explorer MCP server.

This module provides tools for interacting with Ergo blockchain network:
- Get network statistics
- Get mining difficulty
- Get network hashrate
- Get mempool information
"""

import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

from ergo_explorer.api.explorer import fetch_api, fetch_network_state
from ergo_explorer.api.node import (
    get_mempool_transactions_node,
    get_mempool_size_node,
    get_mempool_statistics_node
)

# Set up logging
logger = logging.getLogger(__name__)

async def get_blockchain_stats() -> Dict:
    """
    Fetch overall statistics about the Ergo blockchain.
    
    Returns:
        A dictionary containing blockchain statistics
    """
    try:
        logger.info("Fetching blockchain statistics")
        # Get the network state, which includes statistics
        stats_data = await fetch_network_state()
        
        # Fetch additional stats from the /info endpoint
        additional_stats = await fetch_api("info")
        
        # Combine the data
        combined_stats = {
            "networkState": stats_data,
            "additionalInfo": additional_stats
        }
        
        return combined_stats
    except Exception as e:
        logger.error(f"Error fetching blockchain statistics: {str(e)}")
        return {"error": f"Error fetching blockchain statistics: {str(e)}"}

async def get_network_hashrate() -> Dict:
    """
    Estimate the current network hashrate of the Ergo blockchain.
    
    The hashrate is estimated based on the current difficulty.
    
    Returns:
        A dictionary containing the estimated hashrate in different units
    """
    try:
        logger.info("Fetching network hashrate")
        # Get the network state, which includes difficulty
        network_state = await fetch_network_state()
        
        # Extract difficulty
        difficulty = network_state.get("difficulty", 0)
        
        # Calculate hashrate from the difficulty
        # Ergo hashrate estimate: difficulty / 8192 * 2^32 / 120
        estimated_hashrate = difficulty * (2**32) / (8192 * 120) if difficulty else 0
        
        # Convert to different units
        hashrate_h = estimated_hashrate  # Hashes per second
        hashrate_kh = estimated_hashrate / 1000  # KH/s
        hashrate_mh = estimated_hashrate / 1000000  # MH/s
        hashrate_gh = estimated_hashrate / 1000000000  # GH/s
        hashrate_th = estimated_hashrate / 1000000000000  # TH/s
        hashrate_ph = estimated_hashrate / 1000000000000000  # PH/s
        
        # Prepare result
        hashrate_data = {
            "difficulty": difficulty,
            "estimatedHashrate": hashrate_h,
            "hashrateH": hashrate_h,
            "hashrateKH": hashrate_kh,
            "hashrateMH": hashrate_mh,
            "hashrateGH": hashrate_gh,
            "hashrateTH": hashrate_th,
            "hashratePH": hashrate_ph,
            "timestamp": datetime.now().timestamp() * 1000  # current time in milliseconds
        }
        
        return hashrate_data
    except Exception as e:
        logger.error(f"Error estimating network hashrate: {str(e)}")
        return {"error": f"Error estimating network hashrate: {str(e)}"}

async def get_mining_difficulty() -> Dict:
    """
    Fetch the current mining difficulty of the Ergo blockchain.
    
    Returns:
        A dictionary containing the mining difficulty and related data
    """
    try:
        logger.info("Fetching mining difficulty")
        # Get the network state, which includes difficulty
        network_state = await fetch_network_state()
        
        # Extract relevant information
        difficulty = network_state.get("difficulty", 0)
        
        # Get additional info from /info endpoint to get block time target
        additional_info = await fetch_api("info")
        
        # Extract useful information
        if "parameters" in additional_info:
            block_time_target = additional_info.get("parameters", {}).get("blockInterval", 120)  # in seconds
        else:
            block_time_target = 120  # default is 120 seconds
            
        # Get last blocks for difficulty adjustment info
        last_blocks = network_state.get("lastBlocks", [])
        difficulty_change = None
        
        if len(last_blocks) >= 2:
            # Calculate difficulty change between last two blocks
            current_diff = last_blocks[0].get("difficulty", 0)
            previous_diff = last_blocks[1].get("difficulty", 0)
            
            if previous_diff > 0:
                difficulty_change_pct = (current_diff - previous_diff) / previous_diff * 100
                difficulty_change = {
                    "previousDifficulty": previous_diff,
                    "currentDifficulty": current_diff,
                    "changePercent": difficulty_change_pct
                }
        
        # Prepare result
        difficulty_data = {
            "difficulty": difficulty,
            "blockTimeTarget": block_time_target,
            "difficultyChange": difficulty_change,
            "timestamp": datetime.now().timestamp() * 1000  # current time in milliseconds
        }
        
        return difficulty_data
    except Exception as e:
        logger.error(f"Error fetching mining difficulty: {str(e)}")
        return {"error": f"Error fetching mining difficulty: {str(e)}"}

async def format_blockchain_stats(stats_data: Dict) -> str:
    """
    Format blockchain statistics into a readable string.
    
    Args:
        stats_data: The blockchain statistics data to format
        
    Returns:
        A formatted string representation of the blockchain statistics
    """
    if "error" in stats_data:
        return stats_data["error"]
    
    network_state = stats_data.get("networkState", {})
    additional_info = stats_data.get("additionalInfo", {})
    
    # Extract relevant information
    last_blocks = network_state.get("lastBlocks", [])
    height = last_blocks[0].get("height") if last_blocks else "Unknown"
    
    # Format timestamp
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # Calculate hashrate from the difficulty
    difficulty = network_state.get("difficulty", 0)
    # Ergo hashrate estimate: difficulty / 8192 * 2^32 / 120
    estimated_hashrate = difficulty * (2**32) / (8192 * 120) if difficulty else 0
    hashrate_th = estimated_hashrate / (10**12)  # Convert to TH/s
    
    # Get supply info
    supply_info = additional_info.get("supply", {})
    circulating_supply = supply_info.get("circulating", 0) / 1000000000 if supply_info else 0  # Convert nanoERG to ERG
    max_supply = supply_info.get("max", 0) / 1000000000 if supply_info else 0  # Convert nanoERG to ERG
    
    # Get version info
    version = additional_info.get("version", "Unknown")
    
    # Transaction stats
    total_transactions = additional_info.get("transactionsCount", 0)
    
    # Create a formatted string
    formatted_output = f"""
## Ergo Blockchain Statistics

### General Information
- **Current Height**: {height}
- **Timestamp**: {current_timestamp}
- **Network Version**: {version}

### Mining Statistics
- **Difficulty**: {difficulty:,}
- **Estimated Hashrate**: {hashrate_th:.2f} TH/s

### Supply Information
- **Circulating Supply**: {circulating_supply:,.2f} ERG
- **Maximum Supply**: {max_supply:,.2f} ERG
- **Emission Percentage**: {(circulating_supply / max_supply * 100) if max_supply else 0:.2f}%

### Transaction Statistics
- **Total Transactions**: {total_transactions:,}
"""
    
    # Add additional stats if available
    if "blockSummary" in additional_info:
        block_summary = additional_info["blockSummary"]
        block_size = block_summary.get("avgBlockSize", 0)
        avg_tx_per_block = block_summary.get("avgTxsPerBlock", 0)
        
        formatted_output += f"""
### Block Statistics
- **Average Block Size**: {block_size:,} bytes
- **Average Transactions Per Block**: {avg_tx_per_block:.2f}
"""
    
    return formatted_output

async def format_network_hashrate(hashrate_data: Dict) -> str:
    """
    Format network hashrate data into a readable string.
    
    Args:
        hashrate_data: The hashrate data to format
        
    Returns:
        A formatted string representation of the network hashrate
    """
    if "error" in hashrate_data:
        return hashrate_data["error"]
    
    # Extract relevant information
    difficulty = hashrate_data.get("difficulty", 0)
    hashrate_th = hashrate_data.get("hashrateTH", 0)
    hashrate_ph = hashrate_data.get("hashratePH", 0)
    
    # Format timestamp
    if "timestamp" in hashrate_data:
        timestamp = datetime.fromtimestamp(hashrate_data["timestamp"] / 1000)
        formatted_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")
    else:
        formatted_timestamp = "Unknown"
    
    # Create a formatted string
    formatted_output = f"""
## Ergo Network Hashrate

- **Estimated Hashrate**: {hashrate_th:.2f} TH/s ({hashrate_ph:.6f} PH/s)
- **Current Difficulty**: {difficulty:,}
- **Timestamp**: {formatted_timestamp}

### Hashrate Explanation

The hashrate is an estimate calculated from the current network difficulty.
Formula used: `hashrate = difficulty * 2^32 / (8192 * 120)`

### Note

The actual network hashrate may fluctuate based on several factors including:
- Number of active miners
- Mining hardware efficiency
- Network difficulty adjustments
"""
    
    return formatted_output

async def format_mining_difficulty(difficulty_data: Dict) -> str:
    """
    Format mining difficulty data into a readable string.
    
    Args:
        difficulty_data: The difficulty data to format
        
    Returns:
        A formatted string representation of the mining difficulty
    """
    if "error" in difficulty_data:
        return difficulty_data["error"]
    
    # Extract relevant information
    difficulty = difficulty_data.get("difficulty", 0)
    block_time_target = difficulty_data.get("blockTimeTarget", 120)
    difficulty_change = difficulty_data.get("difficultyChange", None)
    
    # Format timestamp
    if "timestamp" in difficulty_data:
        timestamp = datetime.fromtimestamp(difficulty_data["timestamp"] / 1000)
        formatted_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")
    else:
        formatted_timestamp = "Unknown"
    
    # Create a formatted string
    formatted_output = f"""
## Ergo Mining Difficulty

- **Current Difficulty**: {difficulty:,}
- **Target Block Time**: {block_time_target} seconds
- **Timestamp**: {formatted_timestamp}
"""
    
    # Add difficulty change information if available
    if difficulty_change:
        prev_diff = difficulty_change.get("previousDifficulty", 0)
        change_pct = difficulty_change.get("changePercent", 0)
        change_direction = "increase" if change_pct >= 0 else "decrease"
        
        formatted_output += f"""
### Recent Difficulty Adjustment

- **Previous Difficulty**: {prev_diff:,}
- **Change**: {abs(change_pct):.2f}% {change_direction}
"""
    
    # Add explanation
    formatted_output += """
### Difficulty Explanation

The mining difficulty automatically adjusts to maintain the target block time.
- If blocks are found too quickly, difficulty increases
- If blocks are found too slowly, difficulty decreases

This mechanism ensures that blocks are found approximately every 2 minutes, regardless of the total network hashrate.
"""
    
    return formatted_output

async def get_mempool_info() -> Dict:
    """
    Fetch information about the current mempool state.
    
    This function requires direct connection to an Ergo node.
    
    Returns:
        A dictionary containing mempool statistics and transactions
    """
    try:
        logger.info("Fetching mempool information")
        
        # Get mempool statistics from the node
        mempool_data = await get_mempool_statistics_node()
        
        # Extract and calculate additional statistics
        transactions = mempool_data.get("transactions", [])
        if isinstance(transactions, list):
            tx_count = len(transactions)
        else:
            # If the transactions are paginated
            tx_count = transactions.get("size", 0)
            transactions = transactions.get("items", [])
        
        # Calculate total size in bytes
        total_bytes = sum([tx.get("size", 0) for tx in transactions]) if transactions else 0
        
        # Calculate total value in nanoERG
        total_value = 0
        for tx in transactions:
            outputs = tx.get("outputs", [])
            tx_value = sum([output.get("value", 0) for output in outputs])
            total_value += tx_value
        
        # Convert to ERG
        total_value_erg = total_value / 1000000000
        
        # Calculate average transaction size and value
        avg_size = total_bytes / tx_count if tx_count > 0 else 0
        avg_value_erg = total_value_erg / tx_count if tx_count > 0 else 0
        
        # Calculate fee statistics
        fees = []
        for tx in transactions:
            # Fee calculation is simplified here - in a real implementation,
            # you would need to account for input values minus output values
            fee = tx.get("fee", 0)
            fees.append(fee)
        
        # Calculate fee statistics
        if fees:
            avg_fee = sum(fees) / len(fees)
            min_fee = min(fees) if fees else 0
            max_fee = max(fees) if fees else 0
        else:
            avg_fee = min_fee = max_fee = 0
        
        # Convert fees to ERG
        avg_fee_erg = avg_fee / 1000000000
        min_fee_erg = min_fee / 1000000000
        max_fee_erg = max_fee / 1000000000
        
        # Combine all statistics
        mempool_stats = {
            "timestamp": datetime.now().timestamp() * 1000,  # current time in milliseconds
            "size": mempool_data.get("size", 0),
            "transactionCount": tx_count,
            "totalBytes": total_bytes,
            "totalValue": total_value,
            "totalValueERG": total_value_erg,
            "averageSize": avg_size,
            "averageValueERG": avg_value_erg,
            "feeStats": {
                "averageFee": avg_fee,
                "averageFeeERG": avg_fee_erg,
                "minFee": min_fee,
                "minFeeERG": min_fee_erg,
                "maxFee": max_fee,
                "maxFeeERG": max_fee_erg
            },
            "transactions": transactions[:10]  # Include only first 10 transactions for brevity
        }
        
        return mempool_stats
    except Exception as e:
        logger.error(f"Error fetching mempool information: {str(e)}")
        return {"error": f"Error fetching mempool information: {str(e)}"}

async def format_mempool_info(mempool_data: Dict) -> str:
    """
    Format mempool information into a readable string.
    
    Args:
        mempool_data: The mempool data to format
        
    Returns:
        A formatted string representation of the mempool information
    """
    if "error" in mempool_data:
        return mempool_data["error"]
    
    # Format timestamp
    if "timestamp" in mempool_data:
        timestamp = datetime.fromtimestamp(mempool_data["timestamp"] / 1000)
        formatted_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")
    else:
        formatted_timestamp = "Unknown"
    
    # Extract statistics
    tx_count = mempool_data.get("transactionCount", 0)
    size = mempool_data.get("size", 0)
    total_bytes = mempool_data.get("totalBytes", 0)
    total_value_erg = mempool_data.get("totalValueERG", 0)
    avg_size = mempool_data.get("averageSize", 0)
    avg_value_erg = mempool_data.get("averageValueERG", 0)
    
    # Fee statistics
    fee_stats = mempool_data.get("feeStats", {})
    avg_fee_erg = fee_stats.get("averageFeeERG", 0)
    min_fee_erg = fee_stats.get("minFeeERG", 0)
    max_fee_erg = fee_stats.get("maxFeeERG", 0)
    
    # Create a formatted string
    formatted_output = f"""
## Ergo Mempool Status

- **Timestamp**: {formatted_timestamp}
- **Pending Transactions**: {tx_count:,}
- **Mempool Size**: {size:,}
- **Total Size**: {total_bytes:,} bytes

### Transaction Statistics
- **Total Value**: {total_value_erg:,.2f} ERG
- **Average Transaction Size**: {avg_size:.2f} bytes
- **Average Transaction Value**: {avg_value_erg:.6f} ERG

### Fee Statistics
- **Average Fee**: {avg_fee_erg:.6f} ERG
- **Minimum Fee**: {min_fee_erg:.6f} ERG
- **Maximum Fee**: {max_fee_erg:.6f} ERG
"""
    
    # Add recent transaction list if available
    transactions = mempool_data.get("transactions", [])
    if transactions:
        formatted_output += "\n### Recent Pending Transactions\n"
        
        for i, tx in enumerate(transactions[:5], 1):  # Show only first 5 transactions
            tx_id = tx.get("id", "Unknown")
            tx_size = tx.get("size", 0)
            tx_fee = tx.get("fee", 0) / 1000000000  # Convert to ERG
            
            formatted_output += f"""
**Transaction {i}**
- ID: {tx_id}
- Size: {tx_size:,} bytes
- Fee: {tx_fee:.6f} ERG
""" 