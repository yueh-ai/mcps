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


def make_robotic(audio: np.ndarray, sample_rate: int = 24000) -> np.ndarray:
    """
    Apply robotic voice effect with subtle pitch shift and ring modulation.
    
    Args:
        audio: Input audio array
        sample_rate: Sample rate in Hz
        
    Returns:
        Audio with robotic effect
    """
    audio = audio.astype(np.float32)
    
    pitch_factor = 0.92
    indices = np.arange(0, len(audio), pitch_factor)
    indices = indices[indices < len(audio)].astype(int)
    pitched = audio[indices]
    
    pitched = np.tanh(pitched * 1.2) * 0.8
    
    t = np.arange(len(pitched)) / sample_rate
    carrier = np.sin(2 * np.pi * 600 * t)
    modulated = pitched * (0.85 + 0.1 * carrier)
    
    original_resized = np.interp(
        np.linspace(0, len(audio) - 1, len(modulated)), 
        np.arange(len(audio)), 
        audio
    )
    final = 0.5 * original_resized + 0.5 * modulated
    
    max_val = np.max(np.abs(final))
    if max_val > 0:
        final = final / max_val * 0.95
    
    return final


def process_audio(
    audio: np.ndarray,
    sample_rate: int = 24000,
    apply_smoothing: bool = True,
    apply_robotic: bool = False,
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
    
    if apply_robotic:
        audio = make_robotic(audio, sample_rate)
    
    if speed_factor != 1.0:
        audio = speed_up_audio(audio, speed_factor)
    
    return audio