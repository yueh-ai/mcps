#!/usr/bin/env python3
"""MCP server with embedded Text-to-Speech using KittenTTS."""

import asyncio
import logging
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.server.models import InitializationOptions
from mcp.types import Tool, TextContent, ServerCapabilities, ToolsCapability
from contextlib import asynccontextmanager

from .tts_engine import get_engine
from .voices import DEFAULT_VOICE, AVAILABLE_VOICES

import os
import sys

    
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan():
    """Manage TTS engine lifecycle."""
    engine = get_engine()
    try:
        await engine.initialize()
        logger.info("TTS engine initialized")
    except Exception as e:
        logger.warning(f"TTS engine initialization failed: {e}")
    
    try:
        yield
    finally:
        await engine.cleanup()
        logger.info("TTS engine cleaned up")

app = Server("tts-mcp")


def count_words(text: str) -> int:
    """Count the number of words in the text."""
    return len(text.split())


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="speak",
            description="Convert text to speech and play it. Maximum 100 words.",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to speak (max 100 words)"
                    },
                    "voice": {
                        "type": "string",
                        "description": f"Voice to use (default: {DEFAULT_VOICE})",
                        "default": DEFAULT_VOICE,
                        "enum": [v["id"] for v in AVAILABLE_VOICES]
                    },
                    "speed": {
                        "type": "number",
                        "description": "Playback speed factor (1.0 = normal, 1.3 = 30% faster)",
                        "default": 1.3,
                        "minimum": 0.5,
                        "maximum": 2.0
                    }
                },
                "required": ["text"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls."""
    
    if name == "speak":
        text = arguments.get("text", "")
        voice = arguments.get("voice", DEFAULT_VOICE)
        robotic = arguments.get("robotic", False)
        speed = arguments.get("speed", 1.3)
        
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
        
        try:
            engine = get_engine()
            if not engine._initialized:
                return [TextContent(
                    type="text",
                    text="Error: TTS engine is not available. Please check dependencies are installed."
                )]
            
            result = await engine.speak(
                text=text,
                voice=voice,
                play=True,
                apply_smoothing=True,
                apply_robotic=robotic,
                speed_factor=speed
            )
            
            status = "Success" if result["success"] else "Failed"
            return [TextContent(
                type="text",
                text=f"TTS {status}: {result['message']}"
            )]
            
        except Exception as e:
            logger.error(f"TTS error: {e}")
            return [TextContent(
                type="text",
                text=f"TTS Error: {str(e)}"
            )]
    
    else:
        return [TextContent(
            type="text",
            text=f"Unknown tool: {name}"
        )]


async def main():
    """Main entry point."""
    # Create initialization options
    init_options = InitializationOptions(
        server_name="tts-mcp",
        server_version="0.1.0",
        capabilities=ServerCapabilities(
            tools=ToolsCapability(listChanged=False)
        )
    )
    
    # Run the MCP server with lifespan management
    async with lifespan():
        async with stdio_server() as (read_stream, write_stream):
            await app.run(read_stream, write_stream, init_options)


if __name__ == "__main__":
    asyncio.run(main())