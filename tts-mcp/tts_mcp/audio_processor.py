"""Audio processing utilities for TTS output."""

import numpy as np
from typing import Optional


def smooth_audio(audio: np.ndarray, sample_rate: int = 24000) -> np.ndarray:
    """
    Apply fade-in, fade-out and padding to smooth audio transitions.
    
    Args:
        audio: Input audio array
        sample_rate: Sample rate in Hz
        
    Returns:
        Processed audio with smooth transitions
    """
    audio = audio.astype(np.float32)
    
    fade_in_samples = int(0.02 * sample_rate)  
    if len(audio) > fade_in_samples:
        fade_in = np.linspace(0, 1, fade_in_samples)
        audio[:fade_in_samples] *= fade_in
    
    fade_out_samples = int(0.05 * sample_rate)  
    if len(audio) > fade_out_samples:
        fade_out = np.linspace(1, 0, fade_out_samples)
        audio[-fade_out_samples:] *= fade_out
    
    silence_samples = int(0.1 * sample_rate)  
    silence = np.zeros(silence_samples, dtype=np.float32)
    audio = np.concatenate([audio, silence])
    
    return audio


def speed_up_audio(audio: np.ndarray, speed_factor: float = 1.3) -> np.ndarray:
    """
    Speed up audio playback by resampling.
    
    Args:
        audio: Input audio array
        speed_factor: Speed multiplier (1.3 = 30% faster)
        
    Returns:
        Speed-adjusted audio
    """
    indices = np.arange(0, len(audio), speed_factor)
    indices = indices[indices < len(audio)].astype(int)
    return audio[indices]




def process_audio(
    audio: np.ndarray,
    sample_rate: int = 24000,
    apply_smoothing: bool = True,
    speed_factor: float = 1.3
) -> np.ndarray:
    """
    Apply full audio processing pipeline.
    
    Args:
        audio: Input audio array
        sample_rate: Sample rate in Hz
        apply_smoothing: Whether to apply fade and padding
        apply_robotic: Whether to apply robotic voice effect
        speed_factor: Speed multiplier for playback
        
    Returns:
        Fully processed audio
    """
    if not isinstance(audio, np.ndarray):
        audio = np.array(audio)
    
    if audio.ndim > 1:
        audio = audio.flatten()
    
    if apply_smoothing:
        audio = smooth_audio(audio, sample_rate)
    
    
    if speed_factor != 1.0:
        audio = speed_up_audio(audio, speed_factor)
    
    return audio