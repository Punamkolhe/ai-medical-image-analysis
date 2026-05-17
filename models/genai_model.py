from google import genai
from PIL import Image


# ==============================
# LOAD GEMINI MODEL
# ==============================
def load_model(api_key):

    client = genai.Client(
        api_key=api_key
    )

    return client


# ==============================
# ANALYZE IMAGE
# ==============================
def analyze_image(client, image_path):

    # Open image
    image = Image.open(image_path)

    # Prompt for medical-style explanation
    prompt = """
    Analyze this medical image carefully.

    Explain:
    - Type of image
    - Visible anatomical structures
    - Important observations
    - Any noticeable patterns or abnormalities

    Keep the explanation clear, professional, and easy to understand.
    """

    # Generate response
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            prompt,
            image
        ]
    )

    return response.text