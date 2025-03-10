# Ergo MCP

A Machine-in-the-Middle Communication Protocol (MCP) server for interacting with the Ergo blockchain. This package provides a set of tools for exploring blocks, transactions, addresses, and other aspects of the Ergo blockchain.

## Features

- Block exploration: retrieve blocks by height or hash, get latest blocks, etc.
- Network statistics: blockchain stats, hashrate, mining difficulty, etc.
- Mempool information: pending transactions status and statistics
- Token price information: get token prices from DEXes

## Installation

### Using a Virtual Environment (Recommended)

We strongly recommend using a virtual environment to isolate dependencies:

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Linux/Mac:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate

# Install the package
pip install ergo-mcp
```

### Using pip (System-wide)

```bash
pip install ergo-mcp
```

### From Source

```bash
git clone https://github.com/marctheshark3/ergo-mcp.git
cd ergo-mcp

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the package
pip install .
```

## Usage

### As a Module

Run the MCP server as a Python module from your virtual environment:

```bash
# Make sure your virtual environment is activated, or use the full path to Python
# Using the full path (recommended to ensure the correct Python is used):
/path/to/your/project/.venv/bin/python -m ergo_explorer

# Or with activated virtual environment:
python -m ergo_explorer
```

With custom configuration:

```bash
/path/to/your/project/.venv/bin/python -m ergo_explorer --port 3002 --env-file .env.local --debug
```

### As a Command-line Tool

After installation, you can run the server directly from the command line:

```bash
# Using the full path to the virtual environment:
/path/to/your/project/.venv/bin/ergo-mcp

# Or with activated virtual environment:
ergo-mcp
```

With custom configuration:

```bash
/path/to/your/project/.venv/bin/ergo-mcp --port 3002 --env-file .env.local --debug
```

### Environment Variables

The server can be configured using environment variables in a `.env` file:

- `SERVER_HOST`: Host to bind the server to (default: 0.0.0.0)
- `SERVER_PORT`: Port to run the server on (default: 3001)
- `SERVER_WORKERS`: Number of worker processes (default: 4)
- `ERGO_NODE_API`: URL of the Ergo node API (for node-specific features)
- `ERGO_NODE_API_KEY`: API key for the Ergo node (if required)

### Configure for Claude.app

Add to your Claude settings, making sure to use the full path to your virtual environment's Python:

```json
"mcpServers": {
  "ergo": {
    "command": "/path/to/your/project/.venv/bin/python",
    "args": ["-m", "ergo_explorer"]
  }
}
```

Or if installed via pip in your virtual environment:

```json
"mcpServers": {
  "ergo": {
    "command": "/path/to/your/project/.venv/bin/ergo-mcp",
    "args": []
  }
}
```

## API Documentation

Once the server is running, you can access the API documentation at:

```
http://localhost:3001/docs
```

## Development

### Setting Up a Development Environment

```bash
git clone https://github.com/marctheshark3/ergo-mcp.git
cd ergo-mcp
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

### Running Tests

```bash
# Make sure your virtual environment is activated
pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.