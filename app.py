import os
from PIL import Image as PILImage
import streamlit as st
from dotenv import load_dotenv

from utils import save_uploaded_file
from models.genai_model import load_model, analyze_image

# ==============================
# 🔑 LOAD API KEY
# ==============================
<<<<<<< HEAD
load_dotenv()
=======
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
>>>>>>> 14d0c134cc2e3915cf759f9a102fef0796195c61

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("Gemini API Key not found! Check your .env file")
    st.stop()

# Load model
model = load_model(GEMINI_API_KEY)

# ==============================
# 🎨 STREAMLIT UI
# ==============================
st.set_page_config(page_title="Medical Image Analyzer", layout="centered")

st.title("🩺 Medical Image Analysis Tool 🔬")

st.markdown("""
Upload a medical image and get AI-based insights.

⚠️ This is NOT a medical diagnosis tool.  
This application is for educational purposes only. Always consult a doctor.
""")

# Sidebar upload
st.sidebar.header("Upload Image")
uploaded_file = st.sidebar.file_uploader(
    "Choose image", type=["jpg", "jpeg", "png"]
)

# ==============================
# 📸 MAIN LOGIC
# ==============================
if uploaded_file is not None:

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.image(uploaded_file, caption="Uploaded Image", width=300)

    if st.sidebar.button("🔍 Analyze Image"):

        with st.spinner("Analyzing... Please wait"):

            image_path = save_uploaded_file(
                uploaded_file,
                "temp_image.png"
            )

            try:

                # Gemini AI Analysis
                description = analyze_image(
                    model,
                    image_path
                )

                # 🧠 Structured Report
                report = f"""
### 1. Image Description
The AI model generated the following observation:

➡️ {description}

---

### 2. Image Type & Region
Based on the visual description, this appears to be a medical-related image. 
The structure and composition suggest it may belong to diagnostic imaging such as X-ray, CT scan, or similar modalities. 
However, exact identification requires professional evaluation.

---

### 3. Key Findings
From the AI-generated description, the following points can be interpreted:

- The image contains visible anatomical or structural elements.
- There may be areas of contrast or variation that indicate important regions.
- Patterns detected by AI may correspond to normal or abnormal structures.

⚠️ Note: These are inferred observations, not confirmed findings.

---

### 4. Diagnostic Assessment
This system provides a preliminary AI-based interpretation only.

- No confirmed diagnosis is made.
- The output is based on pattern recognition, not medical reasoning.
- Clinical validation is required.

---

### 5. Patient-Friendly Explanation
In simple terms:

The system looked at your image and tried to describe what it sees.  
It found some patterns and structures, but it cannot determine if something is medically wrong.

👉 You should always consult a doctor for proper diagnosis.

---

### 6. Confidence Note
AI-generated results depend on:
- Image quality  
- Model capability  
- Training limitations  

So accuracy may vary.

---

⚠️ FINAL DISCLAIMER:
This is an AI-generated report for educational purposes only and must NOT be used as a medical diagnosis.
"""

                st.success("✅ Analysis Completed")

                st.subheader("📋 Analysis Report")

                st.markdown(report)

                st.warning(
                    "⚠️ AI-generated results may not be fully accurate."
                )

                st.download_button(
                    label="📄 Download Report",
                    data=report,
                    file_name="medical_report.txt",
                    mime="text/plain"
                )

            except Exception as e:

                st.error(f"🔥 Error: {e}")

            finally:

                if os.path.exists(image_path):
                    os.remove(image_path)

else:
    st.warning("Please upload an image")