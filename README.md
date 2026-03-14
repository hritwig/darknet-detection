# 🛡️ AI Network Sentinel (Edge Deployment)

An edge-optimized, privacy-preserving machine learning pipeline to classify encrypted network traffic (Benign, VPN, and Tor) without relying on Deep Packet Inspection (DPI).

## 📌 Project Overview
As encryption protocols like TLS 1.3 and DoH become standard, traditional payload-based inspection methods fail. This project utilizes flow-based statistical analysis (metadata such as Inter-Arrival Time and Packet Length Variance) to detect and classify anonymizer tunnels. 

The core inference engine is powered by **XGBoost**, specifically tuned to run on resource-constrained Single Board Computers (SBCs) like the **Nano Banana**, ensuring real-time, localized threat detection with millisecond latency.

### Key Features
* **Zero-Payload Inspection:** Guarantees user privacy by analyzing only flow kinetics and spatial distribution.
* **Edge-Optimized AI:** Replaces heavy Deep Learning models with a lightweight, highly interpretable gradient boosting ensemble.
* **Class Imbalance Handling:** Integrates SMOTE to accurately detect rare Tor traffic anomalies without excessive false positives.
* **Decoupled Architecture:** Inference runs locally on the Nano Banana, while telemetry is pushed to an external, real-time Streamlit dashboard.

---

## ⚙️ Hardware & Environment Requirements
* **Primary Compute Node:** Nano Banana SBC (or any ARM/x86 device with limited RAM).
* **OS:** Linux (Ubuntu/Debian recommended).
* **Python:** Version 3.8 or higher.

## 🚀 Installation & Setup

**1. Clone the repository**
```bash
git clone [https://github.com/YourUsername/AI-Network-Sentinel-Edge.git](https://github.com/YourUsername/AI-Network-Sentinel-Edge.git)
cd AI-Network-Sentinel-Edge
