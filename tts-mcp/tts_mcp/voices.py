"""Voice configuration for TTS MCP server."""

from typing import TypedDict, List


class Voice(TypedDict):
    id: str
    gender: str
    description: str


DEFAULT_VOICE = "expr-voice-2-f"

AVAILABLE_VOICES: List[Voice] = [
    {
        "id": "expr-voice-2-m",
        "gender": "male",
        "description": "Expression voice 2 - Male",
    },
    {
        "id": "expr-voice-2-f",
        "gender": "female",
        "description": "Expression voice 2 - Female",
    },
    {
        "id": "expr-voice-3-m",
        "gender": "male",
        "description": "Expression voice 3 - Male",
    },
    {
        "id": "expr-voice-3-f",
        "gender": "female",
        "description": "Expression voice 3 - Female",
    },
    {
        "id": "expr-voice-4-m",
        "gender": "male",
        "description": "Expression voice 4 - Male",
    },
    {
        "id": "expr-voice-4-f",
        "gender": "female",
        "description": "Expression voice 4 - Female",
    },
    {
        "id": "expr-voice-5-m",
        "gender": "male",
        "description": "Expression voice 5 - Male",
    },
    {
        "id": "expr-voice-5-f",
        "gender": "female",
        "description": "Expression voice 5 - Female",
    },
]


def get_voice_ids() -> List[str]:
    """Get list of available voice IDs."""
    return [voice["id"] for voice in AVAILABLE_VOICES]


def is_valid_voice(voice_id: str) -> bool:
    """Check if a voice ID is valid."""
    return voice_id in get_voice_ids()