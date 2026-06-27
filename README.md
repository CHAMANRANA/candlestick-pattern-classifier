# 📈 BullBearAI: Candlestick Pattern Predictor

A machine learning web app that treats stock chart analysis as a computer vision problem.

## ✨ Features

- **Image-Based Prediction:** Upload a **30-day candlestick chart**, and a custom PyTorch model (trained from scratch) predicts whether the trend is **Bullish**, **Bearish**, or **Neutral**.
- **Gemini AI Comparison:** Optionally paste your Gemini API key into the sidebar to compare your model's prediction with Google's Gemini Vision model.
- **Leak-Free Dataset:** Uses a custom chronological train/validation/test split to prevent look-ahead bias, a common issue in stock prediction projects.

---

## 🕹️ How to Use

1. Upload a **30-day candlestick chart**.
2. *(Optional)* Paste your Gemini API key into the sidebar.
3. Click **Run Analysis** to compare predictions.

> **Note:** A sample candlestick chart is included in the `data/` folder so you can test the application immediately.

---

## 📋 Prerequisites

Before running the project, make sure you have the following installed:

- 🐍 **Python 3.10 or later**
- 🌿 **Git**

You can verify your installation by running:

```bash
python --version
git --version
```

If either command is not recognized, install them first:

- **Python:** https://www.python.org/downloads/
- **Git:** https://git-scm.com/downloads

# 💻 Local Setup (One-Click Launch)

### macOS / Linux

```bash
curl -sSL https://raw.githubusercontent.com/CHAMANRANA/candlestick-pattern-classifier/main/run.sh | bash
```

### Windows (PowerShell)

```powershell
irm https://raw.githubusercontent.com/CHAMANRANA/candlestick-pattern-classifier/main/run.ps1 | iex
```

---

# 📊 Dataset & Custom Data Creation

Want to train your own model? You don't need to start from scratch.

### 📥 Download the Dataset

Download the complete **97,000+ image dataset** used in this project:

**Kaggle:** https://www.kaggle.com/datasets/chamanrana/nifty50-candlestick-pattern-dataset-97k-images

### 🛠️ Create Your Own Dataset

The repository also includes the complete data generation pipeline inside the `data_creation/` folder.

You can modify the scripts to:

- Scrape different stocks
- Generate different timeframes
- Customize labeling rules
- Build entirely new candlestick datasets

---

# 📺 Video Explanation

[Can a ResNet-18 Model Predict Stock Candlestick Patterns?](https://youtu.be/GnieOqMdxVg)

---

# ⚠️ Disclaimer

This project is intended **for educational purposes only**.

It is a software engineering and machine learning portfolio project created by a student. AI models can make incorrect predictions and should **not** be used for financial trading, investment decisions, or financial advice.

Always perform your own research before making investment decisions.