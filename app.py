import streamlit as st
import openai
from openai import OpenAI
from PIL import Image
import base64
import io
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")
st.write("API key loaded?", bool(openai.api_key))
  # Loads from .env



# Setup
st.set_page_config(page_title="MagAIan", page_icon="🗺️", layout="centered")

# Styles
st.markdown("""
    <style>
        .big-font { font-size:32px !important; font-weight: bold; }
        .sub-font { font-size:18px !important; color: #6e6e6e; }
        .result-box {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 12px;
            margin-top: 20px;
        }
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<p class="big-font">🧭 MagAIan – Your AI-Powered Tour Guide</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-font">Upload a photo and let our AI give you a story, facts, and history from what it sees 🖼️</p>', unsafe_allow_html=True)

# Upload section
uploaded_file = st.file_uploader("📤 Upload or capture an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Display image
    image = Image.open(uploaded_file)
    st.image(image, caption="📸 Here's your image!", use_container_width=True)

    # Convert to base64
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    # OpenAI API
    with st.spinner("🧠 Thinking... just a sec!"):
        client = OpenAI(api_key=st.secrets["openai_api_key"])

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": "You are a world-class tour guide. Analyze the image below and describe everything you see — the location, landmarks, historical background, names, cultural or fun facts, and any other interesting info."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{image_base64}"
                        }
                    }
                ]
            }]
        )

        result = response.choices[0].message.content

    # Display result
    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    st.markdown("### 🗺️ Here's what I see:")
    st.markdown(result)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("🧠 Powered by OpenAI · 🚀 Built with Streamlit · 🖼️ Created by Joseph", unsafe_allow_html=True)

