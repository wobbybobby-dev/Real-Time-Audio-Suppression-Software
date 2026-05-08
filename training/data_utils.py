import numpy as np

def mix_signals(speech, noise, snr_db):
    # Ensure same length
    if len(noise) < len(speech):
        repeat = int(np.ceil(len(speech) / len(noise)))
        noise = np.tile(noise, repeat)

    noise = noise[:len(speech)]

    # Power
    p_speech = np.mean(speech**2) + 1e-8
    p_noise = np.mean(noise**2) + 1e-8

    # Scale noise for target SNR
    weight = np.sqrt(p_speech / (p_noise * (10**(snr_db / 10))))

    mixed = speech + weight * noise

    return np.clip(mixed, -1.0, 1.0)