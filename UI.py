import streamlit as st
import requests
from PIL import Image
import time

st.set_page_config(layout="wide", page_title="Smart Plant Care")

API_URL = "https://indoorplantwateringpredicto-949564736819.europe-west1.run.app/predict"

# ================== STYLE ==================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

    html, body, [class*="stApp"] {
        height: 100%;
        margin: 0;
        padding: 0;
        background: linear-gradient(to bottom, #a8c686, #355e3b);
        font-family: 'Poppins';
    }

    .block-container {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }

    header, .stAppHeader, .css-18ni7ap {
        display: none !important;
        height: 0 !important;
    }

    [data-testid="stAppViewContainer"] {
        background: linear-gradient(to bottom, #a8c686, #355e3b);
        min-height: 100vh;
        width: 100vw;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
        text-align: center;
        color: white;
        padding: 3rem 1rem;
    }

    .title {
        font-size: clamp(2.2rem, 6vw, 3.5rem);
        font-weight: 700;
        margin-bottom: 10px;
        color: #ffffff;
        text-shadow: 1px 2px 8px rgba(0,0,0,0.4);
    }

    .highlight { color: #2d472b; }

    .subtitle {
        font-size: clamp(1rem, 3vw, 1.5rem);
        opacity: .9;
        margin-bottom: 2.5rem;
        color: #f2f2f2;
    }

    .stFileUploader {
        border: 2px dashed white;
        padding: 1.5rem;
        border-radius: 20px;
        background-color: rgba(255, 255, 255, 0.15);
        width: 90%;
        max-width: 600px;
        margin: 0 auto;
        transition: all 0.3s ease-in-out;
    }

    .stFileUploader:hover {
        background-color: rgba(255, 255, 255, 0.25);
        transform: scale(1.02);
    }

    .stFileUploader label {
        color: white !important;
        font-size: 1.1rem;
    }

    .uploaded-img {
        border-radius: 15px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.4);
        border: 2px solid rgba(255,255,255,0.2);
        max-width: 90%;
    }

    .custom-tip {
        background-color: rgba(80, 160, 255, 0.3);
        color: white;
        border-radius: 12px;
        padding: 1rem;
        width: 90%;
        max-width: 600px;
        margin: 1rem auto;
        font-size: 1.1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }

    .status-bold {
        font-weight: 900 !important;
    }

    [data-testid="stMetric"] {
        background-color: rgba(255,255,255,.1);
        border-radius: 12px;
        padding: 1rem;
        width: 90%;
        max-width: 600px;
        margin: 1rem auto 0 auto;
        box-shadow: 0 4px 12px rgba(0,0,0,0.20);
    }

    [data-testid="stMetricLabel"] {
        color: rgba(255,255,255,.85);
        font-size: 0.9rem;
    }

    [data-testid="stMetricValue"] {
        color: white;
        font-size: 2rem;
        font-weight: bold;
    }

    footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True
)

# ================== HEADER ==================
st.markdown("<div class='title'>Plant Health <span class='highlight'>Predictor</span></div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Smart Way to Check Your Plant's Health 🌿</div>", unsafe_allow_html=True)

# ================== FILE UPLOAD ==================
uploaded_file = st.file_uploader(
    "Drag & drop or click to upload your plant image 🌱",
    type=["jpg", "png", "jpeg"]
)

# ================== IMAGE & PREDICTION ==================
if uploaded_file is not None:
    image = Image.open(uploaded_file)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        resized_image = image.resize((550, 400))  
        st.image(resized_image, caption="Uploaded Image", output_format="auto")
        st.markdown("<style>img {border-radius:15px; box-shadow:0 6px 20px rgba(0,0,0,0.4);}</style>", unsafe_allow_html=True)

    # ================== Progress Bar ==================
    status_text = st.empty()  
    status_text.markdown("### Analyzing your plant's health ...")
    progress_bar = st.progress(0)

    for percent in range(100):
        time.sleep(0.02)
        progress_bar.progress(percent + 1)

    progress_bar.empty()
    status_text.empty() 

    # ================== Prediction ==================
    try:
        files = {'file': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        response = requests.post(API_URL, files=files, timeout=30)

        if response.status_code == 200:
            data = response.json()
            label = data.get("prediction")
            confidence = data.get("confidence")

           
            st.markdown("##### Your Plant’s Health Status")

            if label == "Healthy":
                st.markdown("<div style='color:#00ff99; font-weight:900; font-size:1.2rem;'> Status: Healthy ✅</div>", unsafe_allow_html=True)
                st.markdown("<div class='custom-tip'> Your plant looks great! Keep giving it the same care 💚</div>", unsafe_allow_html=True)

            elif label == "Struggling":
                st.markdown("<div style='color:#fff2b2; font-weight:900; font-size:1.2rem;'> Status: Struggling ⚠️</div>", unsafe_allow_html=True)
                st.markdown("<div class='custom-tip'> Your plant might need a bit more water or indirect sunlight 🌤️</div>", unsafe_allow_html=True)

            else:
                st.markdown("<div style='color:#ffb2b2; font-weight:900; font-size:1.2rem;'> Status: Withered ❌</div>", unsafe_allow_html=True)
                st.markdown("<div class='custom-tip'> It seems your plant is dehydrated. Try watering and trimming dead leaves 🪴</div>", unsafe_allow_html=True)

            if confidence is not None:
                st.metric(label="Confidence", value=f"{float(confidence) * 100:.1f}%")
            else:
                st.warning("Confidence data unavailable.")

        else:
            st.error(f"Error from API: {response.status_code} - {response.text}")

    except requests.exceptions.ConnectionError:
        st.error("Connection Error: Could not connect to the API.")
        st.info(f"Please make sure the FastAPI server is running at: {API_URL}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
