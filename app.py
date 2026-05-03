
import os
from PIL import Image as PILImage
import streamlit as st

from utils import save_uploaded_file, generate_confidence
from models.gemini_model import load_model, analyze_image

# ==============================
# 🔑 SET YOUR API KEY
# ==============================
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")



# Load model from separate file ✅
model = load_model(GOOGLE_API_KEY)

# ==============================
# 🧠 MEDICAL PROMPT
# ==============================
query = """
You are a highly skilled medical imaging expert with extensive knowledge in radiology and diagnostic imaging. Analyze the medical image and structure your response as follows:

### 1. Image Type & Region
- Identify imaging modality (X-ray/MRI/CT/Ultrasound/etc.).
- Specify anatomical region and positioning.
- Evaluate image quality and technical adequacy.

### 2. Key Findings
- Highlight primary observations systematically.
- Identify potential abnormalities with detailed descriptions.

### 3. Diagnostic Assessment
- Provide possible diagnosis (NOT definitive).
- Mention uncertainty clearly.

### 4. Patient-Friendly Explanation
- Explain in simple language.

⚠️ Important:
- Do NOT give final medical diagnosis
- This is only AI-based analysis
"""

# ==============================
# 🎨 STREAMLIT UI
# ==============================
st.set_page_config(page_title="Medical Image Analyzer", layout="centered")

st.title("🩺 Medical Image Analysis Tool 🔬")
st.markdown("""
Upload a medical image and get AI-based insights.

⚠️ This is NOT a medical diagnosis tool.
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

    # Show image (centered look)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image(uploaded_file, caption="Uploaded Image", width=300)

    if st.sidebar.button("🔍 Analyze Image"):
        with st.spinner("Analyzing... Please wait"):

            # Save image using utils ✅
            image_path = save_uploaded_file(uploaded_file, "temp_image.png")

            try:
                # Open safely
                with PILImage.open(image_path) as image:
                    report = analyze_image(model, query, image)

                # Show result
                st.success("✅ Analysis Completed")
                


                st.subheader("📋 Analysis Report")
                st.markdown(report)

                st.warning("⚠️ This is an AI-generated analysis and may not be fully accurate.")


                # Download button
                st.download_button(
                    label="📄 Download Report",
                    data=report,
                    file_name="medical_report.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"🔥 Error: {e}")

            finally:
                # Safe delete
                if os.path.exists(image_path):
                    os.remove(image_path)
               
else:
    st.warning("Please upload an image")
