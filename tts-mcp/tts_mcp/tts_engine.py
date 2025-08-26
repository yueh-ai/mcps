"""TTS Engine using KittenTTS model with lifecycle management."""

import asyncio
import logging
from typing import Optional, Any
import numpy as np

from .voices import DEFAULT_VOICE, is_valid_voice
from .audio_processor import process_audio
from .audio_player import play_audio

logger = logging.getLogger(__name__)


class TTSEngine:
    """
    Singleton TTS engine that manages the KittenTTS model lifecycle.
    """
    
    _instance: Optional['TTSEngine'] = None
    _model: Optional[Any] = None
    _lock: asyncio.Lock = asyncio.Lock()
    _initialized: bool = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    async def initialize(self) -> None:
        """
        Initialize the TTS model. Safe to call multiple times.
        """
        async with self._lock:
            if self._initialized:
                logger.debug("TTS engine already initialized")
                return
            
            try:
                logger.info("Initializing KittenTTS model...")
                from kittentts import KittenTTS
                
                self._model = await asyncio.get_event_loop().run_in_executor(
                    None, KittenTTS, "KittenML/kitten-tts-nano-0.1"
                )
                self._initialized = True
                logger.info("KittenTTS model initialized successfully")
                
            except ImportError as e:
                logger.error(f"Failed to import KittenTTS: {e}")
                logger.warning("TTS functionality will be disabled")
                self._initialized = False
            except Exception as e:
                logger.error(f"Failed to initialize TTS model: {e}")
                logger.warning("TTS functionality will be disabled")
                self._initialized = False
    
    async def cleanup(self) -> None:
        """
        Clean up resources. Safe to call multiple times.
        """
        async with self._lock:
            if not self._initialized:
                return
            
            logger.info("Cleaning up TTS engine...")
            self._model = None
            self._initialized = False
            logger.info("TTS engine cleaned up")
    
    async def generate_speech(
        self,
        text: str,
        voice: str = DEFAULT_VOICE,
        apply_smoothing: bool = True,
        apply_robotic: bool = False,
        speed_factor: float = 1.3
    ) -> np.ndarray:
        """
        Generate speech from text.
        
        Args:
            text: Text to convert to speech
            voice: Voice ID to use
            apply_smoothing: Whether to apply audio smoothing
            apply_robotic: Whether to apply robotic voice effect
            speed_factor: Speed multiplier for playback
            
        Returns:
            Processed audio as numpy array
            
        Raises:
            RuntimeError: If engine not initialized
            ValueError: If voice is invalid
        """
        if not self._initialized:
            await self.initialize()
        
        if not is_valid_voice(voice):
            raise ValueError(f"Invalid voice: {voice}")
        
        if not text.strip():
            raise ValueError("Text cannot be empty")
        
        async with self._lock:
            if not self._model:
                raise RuntimeError("TTS model not initialized")
            
            logger.info(f"Generating speech with voice: {voice}")
            
            audio = await asyncio.get_event_loop().run_in_executor(
                None, self._model.generate, text, voice
            )
            
            audio = process_audio(
                audio,
                sample_rate=24000,
                apply_smoothing=apply_smoothing,
                apply_robotic=apply_robotic,
                speed_factor=speed_factor
            )
            
            return audio
    
    async def speak(
        self,
        text: str,
        voice: str = DEFAULT_VOICE,
        play: bool = True,
        apply_smoothing: bool = True,
        apply_robotic: bool = False,
        speed_factor: float = 1.3
    ) -> dict:
        """
        Generate and optionally play speech.
        
        Args:
            text: Text to convert to speech
            voice: Voice ID to use
            play: Whether to play the audio
            apply_smoothing: Whether to apply audio smoothing
            apply_robotic: Whether to apply robotic voice effect
            speed_factor: Speed multiplier for playback
            
        Returns:
            Dictionary with success status and message
        """
        try:
            audio = await self.generate_speech(
                text=text,
                voice=voice,
                apply_smoothing=apply_smoothing,
                apply_robotic=apply_robotic,
                speed_factor=speed_factor
            )
            
            if play:
                result = await play_audio(audio, sample_rate=24000)
                return result
            else:
                return {
                    "success": True,
                    "message": "Speech generated successfully (playback disabled)",
                    "audio_length": len(audio) / 24000  
                }
                
        except Exception as e:
            logger.error(f"Speech generation failed: {e}")
            return {
                "success": False,
                "message": f"Speech generation failed: {str(e)}"
            }


_engine_instance: Optional[TTSEngine] = None


def get_engine() -> TTSEngine:
    """
    Get the singleton TTS engine instance.
    
    Returns:
        The TTS engine instance
    """
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = TTSEngine()
    return _engine_instance