#!/usr/bin/env python3
"""Debug wrapper for tts-mcp to log all input/output."""

import sys
import json
import subprocess
import datetime

def log(msg):
    """Log to stderr with timestamp."""
    timestamp = datetime.datetime.now().isoformat()
    print(f"[{timestamp}] {msg}", file=sys.stderr)

def main():
    """Run tts-mcp with logging."""
    log("Starting tts-mcp debug wrapper")
    
    # Start the actual tts-mcp process
    proc = subprocess.Popen(
        ["tts-mcp"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=0
    )
    
    try:
        while True:
            # Read from stdin
            line = sys.stdin.readline()
            if not line:
                break
            
            log(f"INPUT: {line.strip()}")
            
            # Send to tts-mcp
            proc.stdin.write(line)
            proc.stdin.flush()
            
            # Read response
            response = proc.stdout.readline()
            if response:
                log(f"OUTPUT: {response.strip()}")
                sys.stdout.write(response)
                sys.stdout.flush()
            
            # Check for errors
            stderr_line = proc.stderr.readline() 
            if stderr_line:
                log(f"STDERR: {stderr_line.strip()}")
                
    except Exception as e:
        log(f"ERROR: {e}")
    finally:
        proc.terminate()
        proc.wait()

if __name__ == "__main__":
    main()