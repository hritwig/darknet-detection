# 🛡️ Darknet Edge Classifier

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![XGBoost](https://img.shields.io/badge/XGBoost-1.7+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-production-brightgreen.svg)

A **production-ready**, **edge-optimized** machine learning classifier for detecting anonymized traffic (Tor, VPN) from benign network flows using the **CIC-Darknet-2020** dataset. Designed specifically for deployment on resource-constrained devices like the **Banana Pi** and **Nvidia Jetson Nano**.

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage](#-usage)
- [Configuration](#-configuration)
- [Dataset](#-dataset)
- [Model Details](#-model-details)
- [Performance](#-performance)
- [Edge Deployment](#-edge-deployment)
- [Project Structure](#-project-structure)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [Citation](#-citation)
- [License](#-license)

---

## ✨ Features

### Core Capabilities
- ✅ **Multi-class Classification**: Benign, Tor, and VPN traffic detection
- ✅ **Edge-Optimized**: Lightweight model (<10MB) for embedded devices
- ✅ **Production-Ready**: Comprehensive logging, error handling, and validation
- ✅ **Modular Design**: Clean separation of concerns for easy maintenance
- ✅ **Automated Pipeline**: End-to-end workflow from data loading to evaluation

### Advanced Features
- 🔧 **Hyperparameter Optimization**: Built-in RandomizedSearchCV/GridSearchCV
- 📊 **Rich Evaluation Metrics**: Per-class metrics, confusion matrix, ROC-AUC
- 📈 **Visualization**: Auto-generated plots for model interpretation
- ⚖️ **Class Balancing**: SMOTE integration for imbalanced datasets
- 🎯 **Feature Selection**: Optimized minimal feature set (6 features)
- 🔄 **Reproducibility**: Seed control and metadata tracking
- 📝 **YAML Configuration**: Easy experimentation without code changes

### Edge Deployment
- 🚀 **Low Latency**: <5ms inference time on Jetson Nano
- 💾 **Minimal Footprint**: ~5MB model size
- 🔌 **Export Formats**: Pickle, JSON, ONNX-ready
- 📱 **Platform Support**: ARM, x86, CUDA

---

## 🏗️ Architecture
