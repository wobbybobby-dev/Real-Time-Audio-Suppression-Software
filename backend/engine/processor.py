import numpy as np
import onnxruntime as ort
from backend.engine.features import stft, istft

class MaskingEngine:
    def __init__(self, model_path=None):
        self.session = ort.InferenceSession(
            "checkpoints/model.onnx",
            providers=["CPUExecutionProvider"]
        )
        self.running_peak = 1e-3     # Slow adaptive normalization state
        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name
                
        # Stateful buffers for seamless transitions
        self.prev_overlap = None
        self.prev_mask = None
        self.overlap_size = 256 

    def reset_state(self):
        self.prev_overlap = None
        self.prev_mask = None

    def _pad_to_multiple(self, x, multiple=8):
        f, t = x.shape

        # Keep frequency dimension fixed
        new_t = ((t + multiple - 1) // multiple) * multiple

        pad_t = new_t - t

        x_padded = np.pad(
            x,
            ((0, 0), (0, pad_t)),
            mode='constant'
        )

        return x_padded, f, t

    def process_chunk(self, audio_np, mode="focus_speech", strength=0.8):
        audio_np = audio_np.astype(np.float32)
        
        # 1. Context Stitching: Prepend previous overlap to current chunk
        if self.prev_overlap is not None:
            input_signal = np.concatenate([self.prev_overlap, audio_np])
        else:
            input_signal = audio_np

        # Slow adaptive normalization
        current_peak = np.max(np.abs(input_signal))

        self.running_peak = (
            0.995 * self.running_peak
            + 0.005 * current_peak
        )

        input_signal = input_signal / (
            self.running_peak + 1e-8
        )
    
        # 2. STFT with windowing context
        mag, phase = stft(input_signal)

        # 3. Model Inference
        mag_padded, orig_f, orig_t = self._pad_to_multiple(mag)
        input_tensor = (
            mag_padded[np.newaxis, np.newaxis, :, :]
        ).astype(np.float32)

        voice_mask = self.session.run(
            [self.output_name],
            {self.input_name: input_tensor}
        )[0]

        voice_mask = np.squeeze(voice_mask)
        # Ensure mask matches STFT dimensions
        min_f = min(voice_mask.shape[0], mag.shape[0])
        min_t = min(voice_mask.shape[1], mag.shape[1])

        voice_mask = voice_mask[:min_f, :min_t]
        mag = mag[:min_f, :min_t]
        phase = phase[:min_f, :min_t]

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
        mask = mask * (1 - 0.08 * adaptive[:mask.shape[0], np.newaxis])
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
