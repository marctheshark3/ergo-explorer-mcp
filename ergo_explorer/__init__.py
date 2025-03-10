"""
Ergo Explorer MCP Server package.

This package provides an MCP server for exploring the Ergo blockchain.
"""

from ergo_explorer.server import mcp, run_server
from ergo_explorer.__main__ import main

__version__ = "0.1.0"
__all__ = ["mcp", "run_server", "main"]
