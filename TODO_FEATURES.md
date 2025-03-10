# Ergo MCP Server - Feature Enhancement Plan

This document outlines planned features and enhancements for the Ergo MCP Server, organized by implementation phases.

## Feature Implementation Plan

### Phase 1 (High Priority)

| Feature | Description | API Required | Status |
|---------|-------------|--------------|--------|
| `get_block_by_height` | Retrieve block data by height | Ergo Explorer API | Completed |
| `get_block_by_hash` | Retrieve block data by hash | Ergo Explorer API | Completed |
| `get_latest_blocks` | Get most recent blocks (with pagination) | Ergo Explorer API | Completed |
| `get_block_transactions` | Get all transactions in a block | Ergo Explorer API | Completed |
| `get_network_hashrate` | Get current network hashrate | Ergo Explorer API | Completed |
| `get_mining_difficulty` | Get current mining difficulty | Ergo Explorer API | Completed |
| `get_blockchain_stats` | Get overall blockchain statistics | Ergo Explorer API | Completed |
| `get_mempool_info` | Get current mempool status and pending transactions | Node API | Completed |
| `get_token_price` | Get current price of a token | DEX APIs | Completed |

### Phase 2 (Medium Priority)

| Feature | Description | API Required | Status |
|---------|-------------|--------------|--------|
| `decode_ergoscript` | Decode and explain an ErgoScript contract | Node API | To Do |
| `validate_contract` | Check if a contract is valid | Node API | To Do |
| `get_contract_boxes` | Find boxes that match a specific contract | Explorer API | To Do |
| `search_transactions_by_asset` | Find transactions involving specific assets | Explorer API | To Do |
| `get_oracle_data` | Get latest data from oracle pools | Oracle Pool API | To Do |
| `get_oracle_history` | Get historical oracle data | Oracle Pool API | To Do |
| `list_active_oracles` | List all active oracle pools | Oracle Pool API | To Do |
| `calculate_portfolio_value` | Calculate total value of address holdings in USD | Explorer + DEX APIs | To Do |
| `get_price_history` | Get historical price data for tokens | DEX APIs | To Do |
| `get_liquidity_data` | Get DEX liquidity information | DEX APIs | To Do |

### Phase 3 (Lower Priority)

| Feature | Description | API Required | Status |
|---------|-------------|--------------|--------|
| `analyze_token_distribution` | Analyze distribution of a token across addresses | Explorer API + Custom | To Do |
| `detect_address_clusters` | Try to detect related addresses | Explorer API + Custom | To Do |
| `track_fund_flow` | Track flow of funds between addresses | Explorer API + Custom | To Do |
| `create_simple_transaction` | Create a basic ERG transfer | Node API | To Do |
| `create_token_transaction` | Create a token transfer | Node API | To Do |
| `estimate_transaction_fee` | Estimate fee for a transaction | Node API | To Do |
| `generate_unsigned_transaction` | Generate an unsigned transaction for hardware wallets | Node API | To Do |
| `search_rich_addresses` | Find addresses with highest balances | Explorer API | To Do |
| `find_p2pk_addresses` | Find all P2PK addresses derived from a public key | Custom | To Do |
| `search_transactions_by_amount` | Find transactions by approximate amount | Explorer API | To Do |

## Implementation Notes

- **Explorer API Integration**: Prioritize integrating with the Ergo Explorer API for phase 1 features.
- **Node API Requirements**: Features requiring Node API access will need direct access to an Ergo node.
- **DEX Integrations**: Price and liquidity features will require integration with Spectrum and/or ErgoDEX APIs.
- **Oracle Pool**: Oracle-related features will need integration with the Oracle Pool API.
- **Custom Analytics**: Phase 3 features marked with "Custom" require development of custom algorithms.

## Progress Tracking

As features are implemented, update their status in the tables above using one of these values:
- To Do
- In Progress
- Testing
- Completed

## API Documentation References

- [Ergo Explorer API](https://api.ergoplatform.com/api/v1/docs/)
- [Ergo Node API](https://github.com/ergoplatform/ergo/blob/master/src/main/resources/api/openapi.yaml)
- [Spectrum DEX](https://spectrum.fi/docs)
- [ErgoDEX](https://docs.ergodex.io/)
- [Oracle Pools](https://github.com/ergoplatform/oracle-core) 