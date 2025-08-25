#!/usr/bin/env python3
"""CLI entry point for tts-mcp."""

import asyncio
import sys
import traceback
from .server import main as async_main

def main():
    """Synchronous wrapper for the async main function."""
    try:
        asyncio.run(async_main())
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if "TaskGroup" in str(e):
            # Print the full traceback for TaskGroup errors
            traceback.print_exc(file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()