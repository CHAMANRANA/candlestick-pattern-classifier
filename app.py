import streamlit as st
import torch
import torch.nn as nn
from torchvision.models import resnet18
from torchvision import transforms
from PIL import Image
from google import genai
from google.genai import types
from google.genai.errors import APIError
from pydantic import BaseModel, Field
from typing import Literal
import json


class Probabilities(BaseModel):
    bullish: float = Field(description="Probability of bullish trend")
    bearish: float = Field(description="Probability of bearish trend")
    neutral: float = Field(description="Probability of neutral trend")

class MarketPrediction(BaseModel):
    signal: Literal['bullish', 'bearish', 'neutral']
    proba: Probabilities


st.set_page_config(
    page_title="BullBearAI: 3-Class Candlestick Classifier",
    layout="wide",
    initial_sidebar_state="auto",
    page_icon="src/assets/icon.png"
)

# Initialize Session States to prevent layout collapse
if "key_valid" not in st.session_state:
    st.session_state.key_valid = False
if "run_analysis" not in st.session_state:
    st.session_state.run_analysis = False

client = None

# --- Sidebar Management ---
with st.sidebar:
    gemini_api_key = st.text_input("Gemini API Key", key="api_key", type="password")
    
    if gemini_api_key:
        client = genai.Client(api_key=gemini_api_key)
        try:
            client.models.list()
            st.session_state.key_valid = True
            st.success("API key is valid")
        except APIError as e:
            st.session_state.key_valid = False
            st.error(f"{e.message}")
            client = None

# --- Main Page Layout ---
st.header("BullBearAI: Candlestick Pattern Predictor", divider="red",text_alignment="center")

# Center columns for image upload
_, centre_co, _ = st.columns(spec=[1, 2, 1], gap="medium")

with centre_co:
    uploaded_image = st.file_uploader("Drop your 30-day chart here", type=["png", "jpeg", "jpg"])

# --- Processing Framework ---
if uploaded_image:
    # If a new image is uploaded, reset the analysis state so old results hide
    if "last_uploaded" not in st.session_state or st.session_state.last_uploaded != uploaded_image.name:
        st.session_state.run_analysis = False
        st.session_state.last_uploaded = uploaded_image.name

    with centre_co:
        img = Image.open(uploaded_image).convert('RGB')
        st.image(img, width="stretch")
        
        # Model Selector
        available_models = ["Local ResNet-18 Model"]
        if st.session_state.key_valid and client:
            available_models.append("Gemini 2.5 Flash API")
            
        selected_engines = st.multiselect(
            "Select Evaluation Engine(s)", 
            options=available_models,
            default=["Local ResNet-18 Model"]
        )
        
        # The Button sets the session state to True
        if st.button("Run Prediction Analysis", width="stretch"):
            st.session_state.run_analysis = True

    # --- Results Rendering Block ---
    # Because we use session_state, this block won't disappear!
    if st.session_state.run_analysis and selected_engines:
        
        st.markdown("---") # Visual separator
        
        # Layout Logic: Split into 2 columns if both are selected, else use full width
        if len(selected_engines) == 2:
            col_left, col_right = st.columns(2, gap="large")
        else:
            col_left = st.container()
            col_right = col_left

        # 1. LOCAL RESNET-18 INFERENCE
        if "Local ResNet-18 Model" in selected_engines:
            with col_left:
                st.subheader("Local ResNet-18 Model")
                with st.spinner("Calculating ResNet vectors..."):
                    try:
                        # Architecture Setup
                        model = resnet18(weights=None)
                        model.fc = nn.Sequential(
                            nn.Dropout(p=0.5),
                            nn.Linear(512, 3, bias=True)
                        )
                        model.load_state_dict(torch.load("models/resnet18.pth", map_location=torch.device('cpu'), weights_only=True))
                        model.eval()

                        # Image Preprocessing (Match your training!)
                        preprocess = transforms.Compose([
                            transforms.Resize((224, 224)),
                            transforms.ToTensor(),
                        ])
                        
                        img_tensor = preprocess(img).unsqueeze(0)
                        
                        # Get Probabilities
                        with torch.no_grad():
                            outputs = model(img_tensor)
                            probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
                            
                        # Extract exact percentages
                        # IMPORTANT: Ensure this list matches your PyTorch training class index!
                        class_names = ['Bearish', 'Bullish', 'Neutral'] # Alphabetical order is standard
                        
                        probs_dict = {class_names[i]: probabilities[i].item() * 100 for i in range(3)}
                        pred_class = max(probs_dict, key=probs_dict.get)

                        # Professional UI Rendering
                        st.markdown(f"#### Prediction — **{pred_class.upper()}**")
                        st.write("")
                        
                        c1, c2, c3 = st.columns(3)
                        c1.metric(label="🟢 Bullish", value=f"{probs_dict['Bullish']:.1f}%")
                        c2.metric(label="🔴 Bearish", value=f"{probs_dict['Bearish']:.1f}%")
                        c3.metric(label="⚪ Neutral", value=f"{probs_dict['Neutral']:.1f}%")
                        
                        st.write("")
                        st.caption("Probability Distribution Balance")
                        st.progress(probs_dict['Bullish']/100, text=f"Bullish weight: {probs_dict['Bullish']:.1f}%")
                        st.progress(probs_dict['Bearish']/100, text=f"Bearish weight: {probs_dict['Bearish']:.1f}%")
                        st.progress(probs_dict['Neutral']/100, text=f"Neutral weight: {probs_dict['Neutral']:.1f}%")
                    
                    except Exception as e:
                        st.error(f"ResNet Error: {e}. Please ensure models/resnet18.pth exists.")

        # 2. GEMINI 2.5 FLASH INFERENCE
        if "Gemini 2.5 Flash API" in selected_engines:
            target_container = col_right if len(selected_engines) == 2 else col_left
            
            with target_container:
                st.subheader("🌐 Gemini 2.5 Flash API")
                with st.spinner("Processing structural geometry with Gemini..."):
                    try:
                        response = client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=[
                                img,
                                "Analyze this financial candlestick chart image for educational purposes and evaluate the current trend signal structure."
                            ],
                            config=types.GenerateContentConfig(
                                response_mime_type="application/json",
                                response_schema=MarketPrediction,
                                temperature=0.1,
                            )
                        )
                        
                        data = json.loads(response.text)
                        p_bull = data['proba']['bullish'] * 100
                        p_bear = data['proba']['bearish'] * 100
                        p_neu = data['proba']['neutral'] * 100
                        
                        st.markdown(f"#### Prediction — **{data['signal'].upper()}**")
                        st.write("")
                        
                        c1, c2, c3 = st.columns(3)
                        c1.metric(label="🟢 Bullish", value=f"{p_bull:.1f}%")
                        c2.metric(label="🔴 Bearish", value=f"{p_bear:.1f}%")
                        c3.metric(label="⚪ Neutral", value=f"{p_neu:.1f}%")
                        
                        st.write("")
                        st.caption("Probability Distribution Balance")
                        st.progress(data['proba']['bullish'], text=f"Bullish weight: {p_bull:.1f}%")
                        st.progress(data['proba']['bearish'], text=f"Bearish weight: {p_bear:.1f}%")
                        st.progress(data['proba']['neutral'], text=f"Neutral weight: {p_neu:.1f}%")
                        
                    except APIError as e:
                        st.error(f"Gemini API Error: {e.message}")