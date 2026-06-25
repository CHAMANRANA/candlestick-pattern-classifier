# 📈 BullBearAI: Candlestick Pattern Predictor

A machine learning web app that treats stock chart analysis as a computer vision problem. 

### What it does:
* **Image-Based Prediction:** Upload a **30-day candlestick chart**, and a custom PyTorch model (trained from scratch) will predict if the trend is Bullish, Bearish, or Neutral.
* **Gemini AI Comparison:** If you paste your free Gemini API key into the sidebar, the app will send the image to Google's Gemini Vision LLM and compare the results side-by-side with the custom model.
* **Clean Data Pipeline:** Built with a custom dataset split chronologically to prevent the "look-ahead" data leaks common in standard stock prediction tutorials.

---

## 🕹️ How to Use

1. **Upload an Image:** The model specifically requires a **30-day candlestick chart**. *(I have included a sample image in the repository data folder so you can test it immediately).*
2. **(Optional) Add Gemini API Key:** Paste your key in the left sidebar to enable the Google AI comparison feature.
3. **Run Analysis:** Click the button to generate the predictions.

---

## 💻 Local Setup (One-Click Launch)

You can instantly deploy the entire project on your local machine using these automated scripts. Open your terminal and paste the command for your operating system:

**For Mac / Linux:**
```bash
curl -sSL [https://raw.githubusercontent.com/CHAMANRANA/candlestick-pattern-classifier/main/run.sh](https://raw.githubusercontent.com/CHAMANRANA/candlestick-pattern-classifier/main/run.sh) | bash 
```

**For Windows (PowerShell):**
```
irm [https://raw.githubusercontent.com/CHAMANRANA/candlestick-pattern-classifier/main/run.ps1](https://raw.githubusercontent.com/CHAMANRANA/candlestick-pattern-classifier/main/run.ps1) | iex
```

## 📊 Dataset & Custom Data Creation

If you want to train your own models, you don't need to start from scratch.

* **Get My Dataset:** You can download the exact 97,000+ image dataset I created for this project here: [Nifty50 Candlestick Pattern Dataset on Kaggle](https://www.kaggle.com/datasets/chamanrana/nifty50-candlestick-pattern-dataset-97k-images).
* **Make Your Own Data:** I have included my data engineering scripts inside the `data_creation/` folder. You can modify these Python scripts to scrape different stocks, change the timeframes, and generate your own custom candlestick image datasets.

---

## 📺 Video Explanation

*[Coming Soon ...]*

---

## ⚠️ Disclaimer

**For educational purposes only.** I am a student, and this is a software engineering and machine learning portfolio project. AI models hallucinate and make mistakes. **Do not** use this tool for actual financial trading, investing, or market decisions.