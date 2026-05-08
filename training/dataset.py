import os
import random
import numpy as np
import librosa
import torch
from torch.utils.data import Dataset
from .data_utils import mix_signals
from backend.engine.features import stft

def normalize_audio(x):
    return x / (np.sqrt(np.mean(x**2)) + 1e-8)

class SpeechNoiseDataset(Dataset):
    def __init__(self, speech_dir, noise_dir, sr=16000):
        self.speech_files = self._load_files(speech_dir)
        self.noise_files = self._load_files(noise_dir)
        self.sr = sr

    def _load_files(self, root):
        files = []
        for path, _, filenames in os.walk(root):
            for f in filenames:
                if f.endswith(".wav") or f.endswith(".flac"):
                    files.append(os.path.join(path, f))
        return files

    def __len__(self):
        return len(self.speech_files)

    def __getitem__(self, idx):
        speech_path = self.speech_files[idx]
        noise_path = random.choice(self.noise_files)

        speech, _ = librosa.load(speech_path, sr=self.sr)
        noise, _ = librosa.load(noise_path, sr=self.sr)

        # Random crop (important for training)
        length = 16000  # 1 second

        if len(speech) > length:
            start = random.randint(0, len(speech) - length)
            speech = speech[start:start + length]

        if len(noise) > length:
            start = random.randint(0, len(noise) - length)
            noise = noise[start:start + length]

        speech = normalize_audio(speech)
        noise = normalize_audio(noise)

        # Random SNR
        snr = random.uniform(-5, 10)

        mixed = mix_signals(speech, noise, snr)

        # STFT
        noisy_mag, _ = stft(mixed)
        clean_mag, _ = stft(speech)

        return (
            torch.from_numpy(noisy_mag).unsqueeze(0).float(),
            torch.from_numpy(clean_mag).unsqueeze(0).float()
        )