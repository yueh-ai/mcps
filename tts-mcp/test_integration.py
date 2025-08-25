#!/usr/bin/env python3
"""Test script to verify TTS MCP integration."""

import json
import subprocess
import sys
import time

def test_mcp_server():
    """Test the MCP server responds to basic requests."""
    
    # Start the MCP server
    proc = subprocess.Popen(
        ["tts-mcp"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    try:
        # Send initialize request
        init_request = {
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {
                "protocolVersion": "1.0.0",
                "capabilities": {},
                "clientInfo": {"name": "test", "version": "1.0.0"}
            },
            "id": 1
        }
        
        proc.stdin.write(json.dumps(init_request) + "\n")
        proc.stdin.flush()
        
        # Wait for response (with timeout)
        start_time = time.time()
        response_line = ""
        while time.time() - start_time < 10:  # 10 second timeout
            try:
                response_line = proc.stdout.readline()
                if response_line:
                    break
            except:
                pass
            time.sleep(0.1)
        
        if response_line:
            response = json.loads(response_line)
            print("✅ Server initialized successfully!")
            print(f"Response: {json.dumps(response, indent=2)}")
            
            # Test list_tools
            tools_request = {
                "jsonrpc": "2.0",
                "method": "mcp/list_tools",
                "params": {},
                "id": 2
            }
            
            proc.stdin.write(json.dumps(tools_request) + "\n")
            proc.stdin.flush()
            
            tools_response = proc.stdout.readline()
            if tools_response:
                tools = json.loads(tools_response)
                print("\n✅ Tools listed successfully!")
                print(f"Available tools: {json.dumps(tools, indent=2)}")
        else:
            print("❌ Server did not respond within timeout")
            # Print stderr for debugging
            stderr_output = proc.stderr.read()
            if stderr_output:
                print(f"Server stderr: {stderr_output}")
            
    except Exception as e:
        print(f"❌ Error testing MCP server: {e}")
    finally:
        proc.terminate()
        proc.wait()

if __name__ == "__main__":
    print("Testing TTS MCP Server Integration...")
    print("-" * 40)
    test_mcp_server()