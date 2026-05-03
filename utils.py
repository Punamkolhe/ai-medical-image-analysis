from PIL import Image
import random

def load_image(path):
    return Image.open(path)

def save_uploaded_file(uploaded_file, path="temp.png"):
    with open(path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return path

def generate_confidence():
    return random.randint(75, 95)