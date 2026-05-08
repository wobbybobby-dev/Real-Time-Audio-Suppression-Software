
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
* ONNX 

**Audio Processing**

* STFT / ISTFT (librosa)
* Spectral masking

---
#  Challenges Overcomed

* Real-Time Latency Stabilization -- Used ONNX Runtime to make system usable in real-time, highly decreased latency
* Training Optimization -- Huge GPU power required, so training done on Google Colabs
* Dataset Optimization -- Used Lean Dataset Strategy
* Syncing frontend and backend together


#  Current Challenges

### 1. Audio Quality issues

* Audio quality improvement needs to be done carefully, as to not disturn the existing stable real-time stabilization.
* Exploring different methods like Soft-Knee Limitation, AGC, AEC, soft masking, etc.

### Dataset and Model Improvements
* Working on expanding dataset, and making a better model than the current U-Net one.
* Improvement in this area will also lead to better audio quality.
--

#  Current Status

 Model Training    :  Completed          
 Backend Pipeline  : Working            
 Audio Quality     :  Improving           
 Real-Time Latency :  Achieved stable real-time latency, using ONNX

---

#  Key Insight

> This project has evolved from a machine learning problem into a **real-time systems engineering challenge**, where timing, buffering, and compute efficiency are critical.

---

#  Future Work

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

# Video Demo



https://github.com/user-attachments/assets/5cb7b3da-7488-4729-bab1-4b4437c29bb6






Video recorded on my phone, due to:
* Latency issues when I use a pc screen recorder, due to system resource starvation
* Audio quality being improved now.
* Real-time latency stabilization achieved via ONNX runtime.

Please excuse the times video gets blurry and I get shown in the PC screen due to the lighting, sorry about that!

Since the video quality is poor (apologise for the inconvenience, I only have my smartphone at the moment), here are some screenshots of the app so you can see the UI clearly:


<img width="1600" height="738" alt="WhatsApp Image 2026-05-09 at 2 18 24 AM" src="https://github.com/user-attachments/assets/192c9b88-b741-4cb7-852d-940110fcab7f" />
<img width="1600" height="742" alt="WhatsApp Image 2026-05-09 at 2 18 06 AM" src="https://github.com/user-attachments/assets/8d6f410d-c14b-4db9-a910-62a243af58fb" />
<img width="1600" height="738" alt="WhatsApp Image 2026-05-09 at 2 17 48 AM" src="https://github.com/user-attachments/assets/38e4de43-46b3-43f0-bab6-47ae6c1678db" />



---

#  Acknowledgements

* LibriSpeech dev-clean Dataset
* !WHAM Noise Dataset
* PyTorch & librosa ecosystem
