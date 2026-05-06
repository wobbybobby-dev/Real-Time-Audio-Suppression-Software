import numpy as np
import librosa
from typing import Tuple
from backend.config import settings


def _to_float32(audio):
    if audio.dtype != np.float32:
        audio = audio.astype(np.float32)
    return audio


def stft(audio: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    audio = _to_float32(audio)

    D = librosa.stft(
        audio,
        n_fft=settings.FFT_SIZE,
        hop_length=settings.HOP_LENGTH,
        window=settings.WINDOW,
        center=True,
    )

    magnitude = np.abs(D).astype(np.float32)
    phase = np.exp(1j * np.angle(D))

    return magnitude, phase


def istft(magnitude: np.ndarray, phase: np.ndarray) -> np.ndarray:
    D = magnitude * phase

    audio = librosa.istft(
        D,
        hop_length=settings.HOP_LENGTH,
        window=settings.WINDOW,
        center=True,
    )

    return audio.astype(np.float32)

def get_frequency_bins(n_fft: int, sample_rate: int):
    return np.linspace(0, sample_rate / 2, n_fft // 2 + 1)

def normalize(audio: np.ndarray):
    max_val = np.max(np.abs(audio)) + 1e-8
    return audio / max_val

def compute_energy(magnitude: np.ndarray):
    return np.mean(magnitude, axis=1)