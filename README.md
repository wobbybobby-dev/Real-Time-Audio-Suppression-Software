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

Users can control suppression strenth using a slider. Real-time  Frequency Graph Visualisation.

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
* PyTorch inference pipeline

**Audio Processing**

* STFT / ISTFT (librosa)
* Spectral masking

---
#  Challenges Overcomed

* Audio Quality -- Used fading, look_ahead, and other buffer-queue strategies to eliminate crackling audio
* Training Optimization -- Huge GPU power required, so training done on Google Colabs
* Dataset Optimization -- Used Lean Dataset Strategy
* Syncing frontend and backend together


#  Current Challenges

### 1. Real-Time Latency (Primary Focus)

* Processing pipeline introduces delay accumulation of about ~300ms at the moment
* Working on:

  * Frame dropping strategies
  * AudioWorklet integration
  * Compute optimization

### 2. Streaming Stability

* Ensuring consistent playback without drift or buffering buildup

### 3. Frontend Optimization

* Migrating from ScriptProcessor → AudioWorklet, which will also lead to reduced latency

### 4. Deployment

* Exploring ONNX / AWS deployment for scalable inference

---

#  Current Status

 Model Training    :  Completed          
 Backend Pipeline  : Working            
 Audio Quality     :  Good               
 Real-Time Latency :  Needs optimization 

---

#  Key Insight

> This project has evolved from a machine learning problem into a **real-time systems engineering challenge**, where timing, buffering, and compute efficiency are critical.

---

#  Future Work

* Reduce latency to true real-time (<100 ms)
* Lightweight / quantized model
* Multi-class sound separation (beyond speech vs noise)
* Mobile / browser-native deployment

I am looking forward to turn this into a functional, user-friendly software, which is easily accessible to all.

---

#  Datasets

* LibriSpeech (clean speech)
* !WHAM Noise Dataset (lite version)
* Mixed dynamically during training (no precomputed mixtures)

---

#  Acknowledgements

* LibriSpeech dev-clean Dataset
* !WHAM Noise Dataset
* PyTorch & librosa ecosystem
