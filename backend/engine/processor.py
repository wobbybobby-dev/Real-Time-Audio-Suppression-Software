import numpy as np
import torch
from backend.models.masking_net import AudioMaskingNet
from backend.engine.features import stft, istft

class MaskingEngine:
    def __init__(self, model_path=None):
        self.model = AudioMaskingNet()
        if model_path:
            self.model.load_state_dict(torch.load(model_path, map_location="cpu"))
        self.model.eval()
        
        # Stateful buffers for seamless transitions
        self.prev_overlap = None
        self.prev_mask = None
        self.overlap_size = 512 # Matches your FFT window context

    def _pad_to_multiple(self, x, multiple=8):
        f, t = x.shape
        new_f = ((f + multiple - 1) // multiple) * multiple
        new_t = ((t + multiple - 1) // multiple) * multiple
        pad_f = new_f - f
        pad_t = new_t - t
        x_padded = np.pad(x, ((0, pad_f), (0, pad_t)), mode='constant')
        return x_padded, f, t

    def process_chunk(self, audio_np, mode="focus_speech", strength=0.8):
        audio_np = audio_np.astype(np.float32)
        
        # 1. Context Stitching: Prepend previous overlap to current chunk
        if self.prev_overlap is not None:
            input_signal = np.concatenate([self.prev_overlap, audio_np])
        else:
            input_signal = audio_np

        # Normalize input_signal
        input_signal = input_signal / (np.max(np.abs(input_signal)) + 1e-8)

        # 2. STFT with windowing context
        mag, phase = stft(input_signal)


        # 3. Model Inference
        mag_padded, orig_f, orig_t = self._pad_to_multiple(mag)
        input_tensor = torch.from_numpy(mag_padded).unsqueeze(0).unsqueeze(0)

        with torch.no_grad():
            voice_mask = self.model(input_tensor).squeeze().numpy()

        # Crop back and clip
        voice_mask = voice_mask[:orig_f, :orig_t]
        voice_mask = np.clip(voice_mask, 0.0, 1.0)

        # 4. Mode Logic (Focus vs Block)
        if mode == "block_speech":
            mask = 1.0 - voice_mask
        else:
            mask = voice_mask

        # 5. Temporal Smoothing: Blend with previous mask to stop "warbling"
        if self.prev_mask is not None and self.prev_mask.shape == mask.shape:
            mask = 0.7 * mask + 0.3 * self.prev_mask
        self.prev_mask = mask

        # Apply strength and adaptive energy suppression
        mask = strength * mask + (1 - strength)
        energy = np.mean(mag, axis=1)
        adaptive = energy / (np.max(energy) + 1e-8)
        mask = mask * (1 - 0.5 * adaptive[:mask.shape[0], np.newaxis])
        # 6. Reconstruction
        enhanced_mag = mag * mask
        reconstructed = istft(enhanced_mag, phase)

        # 7. Extract the valid output chunk
        # We discard the 'context' part and only return the samples 
        # corresponding to the current input chunk.
        if self.prev_overlap is not None:
            output = reconstructed[-len(audio_np):]
        else:
            output = reconstructed[:len(audio_np)]

        # 8. Update Overlap Buffer for next frame
        self.prev_overlap = audio_np[-self.overlap_size:]

        output = np.clip(output, -1.0, 1.0)
        return output.astype(np.float32), mag, enhanced_mag
