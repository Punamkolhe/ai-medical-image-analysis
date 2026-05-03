import google.generativeai as genai

def load_model(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash")

def analyze_image(model, query, image):
    response = model.generate_content([query, image])
    return response.text
