import google.generativeai as genai
import os
import PyPDF2 as pdf
import cv2
import numpy as np
from PIL import Image
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer, util
import gender_guesser.detector as gender
from colorthief import ColorThief

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load AI models
sentence_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
gender_detector = gender.Detector()

def extract_text_from_pdf(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = "".join([page.extract_text() or "" for page in reader.pages])
    return text

def extract_dominant_color(image):
    color_thief = ColorThief(image)
    dominant_color = color_thief.get_color(quality=1)
    return dominant_color

def detect_gender_from_name(name):
    return gender_detector.get_gender(name.split()[0])

def classify_face_shape(image):
    # Placeholder function for face shape classification
    return "Oval"  # To be replaced with an actual ML model

def analyze_image(image_file):
    image = Image.open(image_file)
    image_np = np.array(image)
    face_shape = classify_face_shape(image_np)
    dominant_color = extract_dominant_color(image_file)
    return face_shape, dominant_color

def process_uploaded_file(uploaded_file, name):
    if uploaded_file.type == "application/pdf":
        user_text = extract_text_from_pdf(uploaded_file)
        return None  # PDF processing not returning face details
    else:
        face_shape, skin_color = analyze_image(uploaded_file)
        user_gender = detect_gender_from_name(name) if name else "Unknown"
        return face_shape, skin_color, user_gender

def get_fashion_recommendations(face_shape, skin_color, gender, occasion):
    recommendations = {
        "Oval": {
            "Casual": ("Slim-fit jeans, V-neck shirts, sneakers, and a leather jacket.",
                       "Messy textured haircut or medium-length waves.",
                       "White sneakers or casual loafers."),
            "Formal": ("Tailored suit, solid-color shirt, classic tie, and dress shoes.",
                       "Slicked-back style or classic side-part.",
                       "Oxford shoes or polished leather loafers.")
        },
        "Round": {
            "Casual": ("Straight-leg pants, vertical stripe shirts, and open jackets.",
                       "Pompadour or high-volume quiff.",
                       "Chunky sneakers or desert boots."),
            "Formal": ("Single-breasted blazers, structured suits, and subtle patterns.",
                       "Side-swept undercut or comb-over.",
                       "Monk strap shoes or classic derbies.")
        },
        "Square": {
            "Casual": ("Fitted T-shirts, slim jeans, and bomber jackets.",
                       "Textured crop or spiked hairstyle.",
                       "Combat boots or stylish sneakers."),
            "Formal": ("Double-breasted blazers, structured suits, and bold patterns.",
                       "Side-part or slicked-back undercut.",
                       "Chelsea boots or classic loafers.")
        },
        "Diamond": {
            "Casual": ("Layered outfits, open collars, and fitted joggers.",
                       "Fringe cut or side-swept bangs.",
                       "High-top sneakers or leather sandals."),
            "Formal": ("Tailored tuxedos, deep V-neck shirts, and statement accessories.",
                       "Wavy textured style or slicked-back look.",
                       "Oxford shoes or pointed dress shoes.")
        },
        "Triangle": {
            "Casual": ("Wide-neck shirts, straight-cut pants, and oversized hoodies.",
                       "Quiff or faux hawk.",
                       "Sneakers or casual loafers."),
            "Formal": ("Structured blazers, patterned ties, and fitted trousers.",
                       "Classic short back and sides.",
                       "Monk strap shoes or brogues.")
        },
        "Circle": {
            "Casual": ("Vertical stripe shirts, dark jeans, and fitted jackets.",
                       "High-volume top or comb-over.",
                       "Casual sneakers or slip-ons."),
            "Formal": ("Single-button suits, slim ties, and structured outfits.",
                       "Classic side-part or pompadour.",
                       "Formal derbies or monk straps.")
        }
    }
    
    outfit = recommendations.get(face_shape, {}).get(occasion, 
                ("No recommendation available.", "No hairstyle recommendation available.", "No footwear recommendation available."))
    return outfit
