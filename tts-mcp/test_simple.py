#!/usr/bin/env python3
"""Simple test to debug the MCP server."""

import asyncio
import sys
import os

# Disable logging for cleaner output
os.environ['DEBUG'] = ''

async def test_server():
    """Test the server directly."""
    from tts_mcp.server import main
    
    try:
        await main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_server())