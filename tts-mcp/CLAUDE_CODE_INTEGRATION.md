# Claude Code TTS MCP Integration Guide

## Prerequisites

1. Install the TTS MCP globally:
```bash
uv tool install /workspace/mcps/tts-mcp
```

2. Verify installation:
```bash
which tts-mcp
# Should output: /home/node/.local/bin/tts-mcp
```

## Integration Methods

### Method 1: Using MCP Configuration File

1. Create an MCP configuration file (e.g., `tts-config.json`):
```json
{
  "mcpServers": {
    "tts-mcp": {
      "command": "tts-mcp",
      "args": [],
      "env": {}
    }
  }
}
```

2. Launch Claude Code with the MCP configuration:
```bash
claude --mcp-config tts-config.json
```

### Method 2: Direct Configuration in Claude Code

1. Edit your Claude Code settings file (`~/.claude/settings.json`):
```json
{
  "mcpServers": {
    "tts-mcp": {
      "command": "tts-mcp",
      "args": [],
      "env": {}
    }
  }
}
```

2. Restart Claude Code to apply the changes.

### Method 3: Project-Specific Configuration

1. In your project directory, create `.claude/mcp.json`:
```json
{
  "mcpServers": {
    "tts-mcp": {
      "command": "tts-mcp",
      "args": [],
      "env": {}
    }
  }
}
```

2. Claude Code will automatically detect and use this configuration when working in the project.

## Using the TTS MCP in Claude Code

Once integrated, you can use the TTS tools in Claude Code:

### Available Tools

1. **speak** - Convert text to speech
   - Parameters:
     - `text` (required): Text to speak (max 100 words)
     - `voice` (optional): Voice ID (default: "expr-voice-2-f")
     - `robotic` (optional): Apply robotic effect (default: false)
     - `speed` (optional): Playback speed (default: 1.3, range: 0.5-2.0)

2. **list_voices** - List all available voices

### Example Usage in Claude Code

```
Claude: I can now use text-to-speech to read text aloud. Let me demonstrate:

[Uses speak tool with text="Hello, this is a test of the text to speech system"]

The TTS system supports multiple voices. Let me list them:

[Uses list_voices tool]
```

## Troubleshooting

### MCP Not Detected
- Ensure `tts-mcp` is in your PATH
- Check that the command runs without errors: `tts-mcp`
- Verify the MCP configuration syntax is correct

### Audio Not Playing
- Check system audio output is configured
- Ensure required audio players are installed:
  - macOS: `afplay` (built-in)
  - Linux: `aplay`, `paplay`, or `play`
  - Windows: PowerShell Media.SoundPlayer

### Python Dependencies
- If you see import errors, reinstall with dependencies:
```bash
uv tool install --force /workspace/mcps/tts-mcp
```

## Advanced Configuration

### Custom Voice Settings
You can set default voice parameters in the environment:
```json
{
  "mcpServers": {
    "tts-mcp": {
      "command": "tts-mcp",
      "args": [],
      "env": {
        "TTS_DEFAULT_VOICE": "expr-voice-5-m",
        "TTS_DEFAULT_SPEED": "1.0"
      }
    }
  }
}
```

### Running Multiple MCP Servers
You can run multiple MCP servers simultaneously:
```json
{
  "mcpServers": {
    "tts-mcp": {
      "command": "tts-mcp",
      "args": [],
      "env": {}
    },
    "another-mcp": {
      "command": "another-mcp",
      "args": [],
      "env": {}
    }
  }
}
```

## Security Considerations

- The TTS MCP runs with the same permissions as Claude Code
- Text is processed locally using KittenTTS
- No data is sent to external services
- Audio files are temporarily created and immediately deleted after playback

## Support

For issues or questions:
- Check the README.md for general TTS MCP information
- Review the server logs for error messages
- Ensure all Python dependencies are correctly installed