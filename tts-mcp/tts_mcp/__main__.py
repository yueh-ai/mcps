#!/usr/bin/env python3
"""Entry point for tts-mcp command."""

import asyncio
import sys
import traceback
from .server import main

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if "TaskGroup" in str(e):
            # Print the full traceback for TaskGroup errors
            traceback.print_exc(file=sys.stderr)
        sys.exit(1)