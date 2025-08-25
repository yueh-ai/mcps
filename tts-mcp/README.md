# TTS MCP Server

An MCP (Model Context Protocol) server that provides text-to-speech functionality using KittenTTS for local speech synthesis.

## Features

- Local text-to-speech synthesis using KittenTTS
- Multiple voice options with different characteristics
- Adjustable playback speed
- Optional robotic voice effect
- Audio smoothing for better quality
- Maximum 100 words per request for optimal performance

## Installation

Install using uv:
```bash
uv tool install .
```

Or install in development mode:
```bash
pip install -e .
```

## Usage

### Running the MCP Server

```bash
tts-mcp
```

The server communicates via stdio and should be configured in your MCP client.

### Available Tools

#### `speak`
Convert text to speech and play it through the system audio.

**Parameters:**
- `text` (required): The text to speak (maximum 100 words)
- `voice` (optional): Voice to use (default: "expr-voice-2-f")
- `robotic` (optional): Apply robotic voice effect (default: false)
- `speed` (optional): Playback speed factor - 1.0 = normal, 1.3 = 30% faster (default: 1.3, range: 0.5-2.0)

**Example:**
```json
{
  "tool": "speak",
  "arguments": {
    "text": "Hello, this is a test message for the text to speech service.",
    "voice": "expr-voice-2-f",
    "robotic": false,
    "speed": 1.3
  }
}
```

#### `list_voices`
List all available TTS voices with their descriptions.

**Example:**
```json
{
  "tool": "list_voices",
  "arguments": {}
}
```

### Available Voices

- **expr-voice-2-m**: Expression voice 2 - Male (Male)
- **expr-voice-2-f**: Expression voice 2 - Female (Female) *(default)*
- **expr-voice-3-m**: Expression voice 3 - Male (Male)
- **expr-voice-3-f**: Expression voice 3 - Female (Female)
- **expr-voice-4-m**: Expression voice 4 - Male (Male)
- **expr-voice-4-f**: Expression voice 4 - Female (Female)
- **expr-voice-5-m**: Expression voice 5 - Male (Male)
- **expr-voice-5-f**: Expression voice 5 - Female (Female)

## Configuration

The TTS engine uses KittenTTS for local synthesis with the following features:
- Audio smoothing for improved quality
- Support for multiple expression voices
- Real-time audio playback
- Configurable speed and robotic effects

## Error Handling

The server handles various error cases:
- Text exceeding 100 words limit
- Empty text input
- TTS engine initialization errors
- Audio playback errors

## Requirements

- Python 3.11+
- MCP SDK (>=1.0.0)
- KittenTTS (>=0.1.0)
- soundfile (>=0.12.0)
- numpy (>=1.24.0)
- scipy (>=1.10.0)

## Development

The project structure:
```
tts-mcp/
├── tts_mcp/
│   ├── __init__.py
│   ├── server.py          # Main MCP server
│   ├── tts_engine.py      # KittenTTS engine wrapper
│   ├── audio_processor.py # Audio processing utilities
│   ├── audio_player.py    # Audio playback handling
│   └── voices.py          # Voice configurations
├── pyproject.toml
└── README.md
```
