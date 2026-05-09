
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
* ONNX Runtime inference pipeline

**Audio Processing**

* STFT / ISTFT (librosa)
* Spectral masking

---
#  Challenges Overcomed

* Real-Time Latency Stabilization -- Used ONNX Runtime to make system usable in real-time, preventing long-term latency accumulation.
* Training Optimization -- Huge GPU power required, so training done on Google Colabs
* Dataset Optimization -- Used Lean Dataset Strategy
* Frontend-Backend Synchronization -- Stabilized live audio streaming and playback between frontend and backend in real-time.
* ONNX Deployment Issues -- Resolved tensor shape mismatches, dynamic padding issues, and inference instability during ONNX Runtime migration.


#  Current Challenges

### 1. Audio Quality issues

* Audio quality improvement needs to be done carefully, as to not disturn the existing stable real-time stabilization.
* Exploring different methods like Soft-Knee Limitation, AGC, AEC, soft masking, etc.
* Current bottleneck has shifted from latency engineering to model quality and perceptual speech enhancement.

### 2. Dataset and Model Improvements
* Working on expanding dataset, and making a better model than the current U-Net one.
* Exploring more advanced architectures inspired by modern speech enhancement systems (CRN, recurrent bottlenecks, temporal modeling).
* Improvement in this area will directly improve speech intelligibility and overall audio quality.

### 3. Improving Model Architecture
* Currently, ONNX inference model is too big for my CPU.
* This adds to latency.
<img width="930" height="925" alt="image" src="https://github.com/user-attachments/assets/8e242a2f-3320-4eb3-9ef5-9c0d2d3afbff" />
Attached are some process logs to show what I mean. Here we see ISFT and STFT take very less time, while ONNX itself is taking more time.
* Working on finding ways to build a lightweight, quantized model, with better and larger dataset training.
--

#  Current Status

 Model Training    :  Completed          
 Backend Pipeline  : Working            
 Audio Quality     :  Improving           
 Real-Time Latency :  Achieved stable low latency real-time, using ONNX

---

#  Key Insight

> This project has evolved from a machine learning problem into a **real-time systems engineering challenge**, where timing, buffering, and compute efficiency are critical.

---

#  Future Work

* Lightweight / quantized model
* Improved perceptual audio quality while preserving realtime responsiveness
* Multi-class sound separation (beyond speech vs noise)
* Mobile / browser-native deployment
* Better temporal speech modeling

I am looking forward to turn this into a functional, user-friendly software, which is easily accessible to all.

---

#  Datasets

* LibriSpeech (clean speech)
* !WHAM Noise Dataset (lite version)
* Mixed dynamically during training (no precomputed mixtures)

---

# Video Demo



https://github.com/user-attachments/assets/5cb7b3da-7488-4729-bab1-4b4437c29bb6






Video recorded on my phone, due to:
* Latency issues(abnormal spikes) when I use a pc screen recorder, due to realtime system resource starvation.
* Audio quality being improved now.

Please excuse the times video gets blurry and I get shown in the PC screen due to the lighting, sorry about that!

Since the video quality is poor (apologise for the inconvenience, I only have my smartphone at the moment), here are some screenshots of the app so you can see the UI clearly:


<img width="1600" height="738" alt="WhatsApp Image 2026-05-09 at 2 18 24 AM" src="https://github.com/user-attachments/assets/192c9b88-b741-4cb7-852d-940110fcab7f" />
<img width="1600" height="742" alt="WhatsApp Image 2026-05-09 at 2 18 06 AM" src="https://github.com/user-attachments/assets/8d6f410d-c14b-4db9-a910-62a243af58fb" />
<img width="1600" height="738" alt="WhatsApp Image 2026-05-09 at 2 17 48 AM" src="https://github.com/user-attachments/assets/38e4de43-46b3-43f0-bab6-47ae6c1678db" />

Here is a short snapshot of the performance log during development:
<img width="391" height="418" alt="image" src="https://github.com/user-attachments/assets/47adeed3-b54e-4bbd-b7fb-778bf60c8d39" />

Typical steady-state realtime processing latency after ONNX Runtime optimization. 

---

#  Acknowledgements

* LibriSpeech dev-clean Dataset
* !WHAM Noise Dataset
* PyTorch, ONNX Runtime & librosa ecosystem
