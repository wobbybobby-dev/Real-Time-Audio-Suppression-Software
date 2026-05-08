#  Real-Time Audio Suppression System

A real-time audio processing application that selectively enhances or suppresses speech using deep learning.
This system allows users to dynamically filter live microphone input to either:
* **Focus on speech** in noisy environments
* **Suppress speech** to isolate ambient background sounds

Designed for noise sensitivity assistance, focus enhancement, and intelligent audio filtering. 

---

#  Features

###  Focus Speech Mode

Enhances human voice, while suppressing background noise.

###  Block Speech Mode

Removes human voices while preserving environmental sounds.

Users can control suppression strength using a slider. Real-time Frequency Graph Visualisation.

###  Real-Time Processing Pipeline

Streaming pipeline:

Microphone → WebSocket → STFT → U-Net Masking → ISTFT → Playback


###  Deep Learning-Based Masking

* Model: U-Net (spectrogram domain)
* Training target: **Ideal Ratio Mask (IRM)**
* Input: Noisy magnitude spectrogram
* Output: Speech mask

###  Dynamic Dataset Mixing

* Clean speech (LibriSpeech) + noise (!WHAM)
* Mixed **on-the-fly using random SNR**
* Improves generalization and reduces dataset size

---

#  Tech Stack

**Frontend**

* React (Web Audio API)
* Real-time visualization (Frequency bar graphs)

**Backend**

* FastAPI + WebSockets
* ONNX Runtime inference pipeline
* ONNX

**Audio Processing**

* STFT / ISTFT (librosa)
* Spectral masking

---

#  Challenges Overcome

* Real-Time Latency Stabilization -- Used ONNX Runtime to make the system usable in real-time, significantly decreasing latency and preventing long-term latency accumulation.
* Training Optimization -- Huge GPU power required, so training done on Google Colab.
* Dataset Optimization -- Used Lean Dataset Strategy with dynamic dataset mixing.
* Frontend-Backend Synchronization -- Stabilized live audio streaming and playback between frontend and backend in real-time.
* ONNX Deployment Issues -- Resolved tensor shape mismatches, dynamic padding issues, and inference instability during ONNX Runtime migration.
* Real-Time Resource Constraints -- Optimized the system to maintain stable realtime responsiveness under normal usage despite browser and CPU contention.

#  Current Challenges

### 1. Audio Quality Issues

* Audio quality improvement needs to be done carefully, as to not disturb the existing stable real-time latency stabilization.
* Current bottleneck has shifted from latency engineering to model quality and perceptual speech enhancement.
* Exploring different methods like Soft-Knee Limiting, AGC, AEC, soft masking, spectral smoothing, temporal smoothing, etc.

### Dataset and Model Improvements

* Working on expanding dataset diversity, longer training, and improving the current U-Net architecture.
* Exploring more advanced architectures inspired by modern speech enhancement systems (CRN, recurrent bottlenecks, temporal modeling).
* Improvement in this area will directly improve speech intelligibility and overall audio quality.

---

#  Current Status

 Model Training    :  Completed          
 Backend Pipeline  : Working            
 Audio Quality     : Improving           
 Real-Time Latency : Stable low-latency realtime streaming achieved using ONNX Runtime

---

#  Key Insight

> This project has evolved from a machine learning problem into a **real-time systems engineering challenge**, where timing, buffering, synchronization, and compute efficiency are critical.

---

#  Future Work

* Lightweight / quantized model
* Better temporal speech modeling
* Multi-class sound separation (beyond speech vs noise)
* Mobile / browser-native deployment
* Improved perceptual audio quality while preserving realtime responsiveness

I am looking forward to turning this into a functional, user-friendly software, which is easily accessible to all.

---

#  Datasets

* LibriSpeech (clean speech)
* !WHAM Noise Dataset (lite version)
* Mixed dynamically during training (no precomputed mixtures)

---

# Video Demo

Video recorded on my phone, due to:
* Screen recording causing latency spikes because of realtime system resource starvation
* Wanting to preserve the system's stable realtime responsiveness during demonstration
* Audio quality currently still being improved
* Real-time latency stabilization achieved via ONNX Runtime

Please excuse the times the video gets blurry and I get shown in the PC screen due to the lighting, sorry about that!

Since the video quality is poor (apologies for the inconvenience, I only have my smartphone at the moment), here are some screenshots of the app so you can see the UI clearly:
(images)

---

#  Acknowledgements

* LibriSpeech dev-clean Dataset
* !WHAM Noise Dataset
* PyTorch, ONNX Runtime & librosa ecosystem
