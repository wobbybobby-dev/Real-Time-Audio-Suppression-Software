from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # ── Server ──────────────────────────────────────────────
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ALLOWED_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    # ── Audio capture ────────────────────────────────────────
    SAMPLE_RATE: int = 16000        # Hz
    CHANNELS: int = 1               # Mono
    CHUNK_DURATION_MS: int = 8     # ms per WebSocket frame
    CHUNK_SIZE: int = 128           # = SAMPLE_RATE * CHUNK_DURATION_MS / 1000

    # ── STFT / spectral ──────────────────────────────────────
    FFT_SIZE: int = 512
    HOP_LENGTH: int = 128
    WINDOW: str = "hann"

    # ── Mel spectrogram ──────────────────────────────────────
    N_MELS: int = 64
    F_MIN: float = 50.0
    F_MAX: float = 8000.0

    # ── MFCC ─────────────────────────────────────────────────
    N_MFCC: int = 13

    # ── Classifier ───────────────────────────────────────────
    CLASSIFIER_WINDOW_MS: int = 500
    CLASSIFIER_STRIDE_MS: int = 250
    CLASSIFIER_CONFIDENCE_THRESHOLD: float = 0.55

    # ── Suppression ──────────────────────────────────────────
    WIENER_ALPHA: float = 0.95
    OVER_SUBTRACTION: float = 0.5
    SPECTRAL_FLOOR: float = 0.05

    NOISE_CLASSES: list[str] = [
        "speech", "non-speech"
    ]

   

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
