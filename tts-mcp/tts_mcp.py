#!/usr/bin/env python3
import asyncio
import requests
from typing import Any
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

app = Server("tts-mcp")

def count_words(text: str) -> int:
    """Count the number of words in the text"""
    return len(text.split())

def send_tts_request(text: str, voice: str = "expr-voice-2-f") -> dict:
    """Send text to TTS service"""
    try:
        response = requests.post(
            "http://host.docker.internal:8000/tts",
            json={"text": text, "voice": voice},
            timeout=10
        )
        if response.status_code == 200:
            return {"success": True, "message": "Text sent to TTS successfully"}
        else:
            return {"success": False, "message": f"TTS service returned status {response.status_code}"}
    except requests.exceptions.Timeout:
        return {"success": False, "message": "TTS service timeout"}
    except requests.exceptions.ConnectionError:
        return {"success": False, "message": "Could not connect to TTS service"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="speak",
            description="Send text to the TTS (text-to-speech) service. Maximum 100 words.",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to speak (max 100 words)"
                    },
                    "voice": {
                        "type": "string",
                        "description": "Voice to use (default: expr-voice-2-f)",
                        "default": "expr-voice-2-f"
                    }
                },
                "required": ["text"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls"""
    if name == "speak":
        text = arguments.get("text", "")
        voice = arguments.get("voice", "expr-voice-2-f")
        
        word_count = count_words(text)
        if word_count > 100:
            return [TextContent(
                type="text",
                text=f"Error: Text exceeds 100 words limit (provided: {word_count} words)"
            )]
        
        if not text.strip():
            return [TextContent(
                type="text",
                text="Error: Text cannot be empty"
            )]
        
        result = await asyncio.get_event_loop().run_in_executor(
            None, send_tts_request, text, voice
        )
        
        return [TextContent(
            type="text",
            text=f"TTS Result: {result['message']}"
        )]
    else:
        return [TextContent(
            type="text",
            text=f"Unknown tool: {name}"
        )]

async def main():
    """Main entry point"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream)

if __name__ == "__main__":
    asyncio.run(main())