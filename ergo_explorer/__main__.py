#!/usr/bin/env python
"""
Main entry point for running the Ergo MCP server as a module.

This allows running the server with:
    python -m ergo_explorer [arguments]
"""

import sys
import os
import logging
import argparse
from ergo_explorer import run_server
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Parse command-line arguments and run the server."""
    parser = argparse.ArgumentParser(description="Ergo MCP Server")
    
    parser.add_argument(
        "--env-file", 
        type=str, 
        default=".env",
        help="Path to the environment file (default: .env)"
    )
    
    parser.add_argument(
        "--port", 
        type=int, 
        default=None,
        help="Port to run the server on (overrides config or env variable)"
    )
    
    parser.add_argument(
        "--host", 
        type=str, 
        default=None,
        help="Host to bind the server to (overrides config or env variable)"
    )
    
    parser.add_argument(
        "--debug", 
        action="store_true",
        help="Enable debug mode"
    )
    
    args = parser.parse_args()
    
    # Load environment variables from specified file
    if os.path.exists(args.env_file):
        logger.info(f"Loading environment from {args.env_file}")
        load_dotenv(args.env_file)
    else:
        logger.warning(f"Environment file {args.env_file} not found, using default environment")
    
    # Set additional environment variables based on command-line arguments
    if args.port:
        os.environ["SERVER_PORT"] = str(args.port)
        
    if args.host:
        os.environ["SERVER_HOST"] = args.host
        
    if args.debug:
        os.environ["DEBUG"] = "1"
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled")
    
    try:
        logger.info("Starting Ergo MCP server...")
        run_server()
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error starting server: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main() 