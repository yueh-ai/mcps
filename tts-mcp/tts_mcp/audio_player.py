"""Platform-specific audio playback utilities."""

import os
import platform
import subprocess
import tempfile
import logging
from typing import Optional, Tuple
import numpy as np
import soundfile as sf

logger = logging.getLogger(__name__)


class AudioPlaybackError(Exception):
    """Raised when audio playback fails."""
    pass


def save_to_temp_file(audio: np.ndarray, sample_rate: int = 24000) -> str:
    """
    Save audio array to a temporary WAV file.
    
    Args:
        audio: Audio data as numpy array
        sample_rate: Sample rate in Hz
        
    Returns:
        Path to the temporary file
    """
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
        tmp_path = tmp_file.name
        sf.write(tmp_path, audio, sample_rate, format="WAV")
    return tmp_path


def play_macos(audio_path: str) -> Tuple[bool, str]:
    """
    Play audio on macOS using afplay.
    
    Args:
        audio_path: Path to audio file
        
    Returns:
        Tuple of (success, message)
    """
    try:
        subprocess.run(["afplay", audio_path], check=True, capture_output=True)
        return True, "Audio played successfully on macOS"
    except subprocess.CalledProcessError as e:
        return False, f"macOS playback failed: {e.stderr.decode() if e.stderr else str(e)}"
    except FileNotFoundError:
        return False, "afplay command not found on macOS"


def play_linux(audio_path: str) -> Tuple[bool, str]:
    """
    Play audio on Linux using available audio players.
    
    Args:
        audio_path: Path to audio file
        
    Returns:
        Tuple of (success, message)
    """
    players = ["aplay", "paplay", "play", "cvlc --play-and-exit"]
    
    for player_cmd in players:
        try:
            player_parts = player_cmd.split()
            player_parts.append(audio_path)
            subprocess.run(player_parts, check=True, capture_output=True)
            return True, f"Audio played successfully on Linux using {player_parts[0]}"
        except (FileNotFoundError, subprocess.CalledProcessError):
            continue
    
    return False, "No suitable audio player found on Linux (tried aplay, paplay, play, cvlc)"


def play_windows(audio_path: str) -> Tuple[bool, str]:
    """
    Play audio on Windows using PowerShell.
    
    Args:
        audio_path: Path to audio file
        
    Returns:
        Tuple of (success, message)
    """
    try:
        cmd = [
            "powershell", "-c",
            f"(New-Object Media.SoundPlayer '{audio_path}').PlaySync()"
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return True, "Audio played successfully on Windows"
    except subprocess.CalledProcessError as e:
        return False, f"Windows playback failed: {e.stderr.decode() if e.stderr else str(e)}"


async def play_audio(
    audio: np.ndarray,
    sample_rate: int = 24000,
    cleanup: bool = True
) -> dict:
    """
    Play audio on the current platform.
    
    Args:
        audio: Audio data as numpy array
        sample_rate: Sample rate in Hz
        cleanup: Whether to delete temp file after playback
        
    Returns:
        Dictionary with success status and message
    """
    tmp_path = None
    
    try:
        tmp_path = save_to_temp_file(audio, sample_rate)
        
        system = platform.system()
        logger.info(f"Playing audio on {system}...")
        
        if system == "Darwin":
            success, message = play_macos(tmp_path)
        elif system == "Linux":
            success, message = play_linux(tmp_path)
        elif system == "Windows":
            success, message = play_windows(tmp_path)
        else:
            success = False
            message = f"Unsupported operating system: {system}"
        
        if success:
            logger.info(message)
            return {"success": True, "message": message}
        else:
            logger.error(message)
            return {"success": False, "message": message}
            
    except Exception as e:
        logger.error(f"Audio playback error: {e}")
        return {"success": False, "message": f"Audio playback error: {str(e)}"}
        
    finally:
        if cleanup and tmp_path and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
                logger.debug(f"Cleaned up temp file: {tmp_path}")
            except Exception as e:
                logger.warning(f"Failed to cleanup temp file {tmp_path}: {e}")


def test_audio_system() -> bool:
    """
    Test if audio playback is available on this system.
    
    Returns:
        True if audio can be played, False otherwise
    """
    try:
        test_audio = np.zeros(24000, dtype=np.float32)
        tmp_path = save_to_temp_file(test_audio, 24000)
        
        system = platform.system()
        if system == "Darwin":
            success, _ = play_macos(tmp_path)
        elif system == "Linux":
            success, _ = play_linux(tmp_path)
        elif system == "Windows":
            success, _ = play_windows(tmp_path)
        else:
            success = False
        
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
            
        return success
        
    except Exception:
        return False