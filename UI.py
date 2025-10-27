import streamlit as st
import requests
from PIL import Image

st.set_page_config(layout="wide", page_title="Smart Plant Care")

API_URL = "https://indoorplantwateringpredicto-949564736819.europe-west1.run.app/predict"

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
        font-size: 60px;
        font-weight: 600;
        margin-bottom: 20px;
        color: white;
        text-shadow: 1px 2px 8px rgba(0,0,0,0.3);
    }

    .highlight { color: #355931; }
    .subtitle { font-size: 25px; opacity: .85; margin-bottom: 3rem; }


    .stFileUploader [data-testid="stFileUploaderButton"] {
        background-color: #f1f1f1 !important;
        color: #234d2c !important;
        border-radius: 10px !important;
        border: 2px solid #234d2c !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.15);
    }

    .stFileUploader [data-testid="stFileUploaderButton"]:hover {
        background-color: #d9ead3 !important;
        color: #1f3c25 !important;
        border-color: #1f3c25 !important;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.25);
    }

    .stFileUploader {
        border: 2px dashed white;
        padding: 1.5rem;
        border-radius: 20px;
        background-color: rgba(255, 255, 255, 0.1);
        width: 90%;
        max-width: 600px;
        margin: 0 auto;
    }

    .stFileUploader label {
        color: white !important;
        font-size: 1.1rem;
    }


    .stAlert {
        border-radius: 12px;
        width: 90%;
        max-width: 600px;
        margin: 1rem auto 0 auto !important;
        padding: 1rem;
        box-shadow: 0 6px 20px rgba(0,0,0,.20);
    }


    .stAlert div {
        font-size: 1.4rem !important;
        font-weight: 800 !important;
        text-align: center;
    }

    /* Healthy */
    .stSuccess div { color: #c7ffd0 !important; }

    /* Struggling */
    .stWarning div { color: #fff2b2 !important; }

    /*  Withered */
    .stError {
        background-color: #b30000 !important;
        border: 2px solid #ff4d4d !important;
        border-radius: 10px !important;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.4);
    }

    .stError div {
        color: #ffffff !important;
        font-weight: 900 !important;
        font-size: 1.6rem !important;
        text-align: center;
        text-shadow: 0px 0px 6px rgba(0,0,0,0.6);
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

st.markdown("<div class='title'>Plant Health <span class='highlight'>Predictor</span></div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Smart Way to Check Plant Health</div>", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload an image to check your plant's status...",
    type=["jpg", "png", "jpeg"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(image, caption="Uploaded Image", use_container_width=True)

    with st.spinner("Analyzing plant..."):
        try:
            files = {'file': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            response = requests.post(API_URL, files=files, timeout=30)

            if response.status_code == 200:
                data = response.json()
                label = data.get("prediction")
                confidence = data.get("confidence")

                st.subheader("Prediction Results")

                if label == "Healthy":
                    st.success(f"Status: {label}")
                elif label == "Struggling":
                    st.warning(f"Status: {label}")
                else:
                    st.error(f"Status: {label}")

                st.metric(label="Confidence", value=f"{float(confidence) * 100:.1f}%")

            else:
                st.error(f"Error from API: {response.status_code} - {response.text}")

        except requests.exceptions.ConnectionError:
            st.error("Connection Error: Could not connect to the API.")
            st.info(f"Please make sure the FastAPI server is running at: {API_URL}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
