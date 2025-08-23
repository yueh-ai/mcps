# TTS MCP Server

An MCP (Model Context Protocol) server that provides text-to-speech functionality by connecting to a TTS service.

## Features

- Accepts text input from calling agents (max 100 words)
- Connects to TTS service at `http://host.docker.internal:8000/tts`
- Supports voice selection
- Returns success/failure status

## Installation

```bash
pip install -e .
```

## Usage

### Running the MCP Server

```bash
python tts_mcp.py
```

### Available Tools

#### `speak`
Send text to the TTS service for speech synthesis.

**Parameters:**
- `text` (required): The text to speak (maximum 100 words)
- `voice` (optional): Voice to use (default: "expr-voice-2-f")

**Example:**
```json
{
  "tool": "speak",
  "arguments": {
    "text": "Hello, this is a test message for the text to speech service.",
    "voice": "expr-voice-2-f"
  }
}
```

## Configuration

The MCP server connects to the TTS service at:
- URL: `http://host.docker.internal:8000/tts`
- Timeout: 10 seconds

## Error Handling

The server handles various error cases:
- Text exceeding 100 words limit
- Empty text input
- TTS service connection errors
- TTS service timeouts

## Requirements

- Python 3.11+
- MCP SDK
- requests library
- Running TTS service on port 8000