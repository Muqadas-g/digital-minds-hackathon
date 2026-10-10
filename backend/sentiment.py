# ============================================
# sentiment.py - Model Loading & Prediction
# ============================================

import joblib
import json
import os
import re
from langdetect import detect, LangDetectException

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "sentiment_pipeline.joblib")
LABEL_PATH = os.path.join(BASE_DIR, "models", "label_mapping.json")

# Load model once
print("Loading sentiment model...")
model = joblib.load(MODEL_PATH)

with open(LABEL_PATH, "r") as f:
    LABEL_MAP = json.load(f)

print("Model loaded successfully!")


def clean_text(text: str) -> str:
    """Same cleaning as training."""
    text = str(text).lower()
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'#', '', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def predict_sentiment(text: str) -> dict:
    """Predict sentiment for a single comment."""
    cleaned = clean_text(text)

    if not cleaned:
        return {
            "label": "Neutral",
            "confidence": 0.0,
            "probabilities": {"Negative": 0.0, "Neutral": 1.0, "Positive": 0.0}
        }

    pred = model.predict([cleaned])[0]
    proba = model.predict_proba([cleaned])[0]

    neg_prob = float(proba[0])
    pos_prob = float(proba[1])
    max_prob = max(neg_prob, pos_prob)

    # Neutral handling: confidence between 40% and 60%
    if 0.40 <= max_prob <= 0.60:
        label = "Neutral"
        confidence = max_prob
    else:
        label = LABEL_MAP[str(pred)]
        confidence = max_prob

    return {
        "label": label,
        "confidence": round(confidence * 100, 2),
        "probabilities": {
            "Negative": round(neg_prob, 4),
            "Positive": round(pos_prob, 4),
            "Neutral": round(1 - max_prob, 4) if label == "Neutral" else 0.0
        }
    }


def detect_language(text: str) -> str:
    """Detect language of a comment."""
    try:
        lang_code = detect(text)
        lang_map = {
            'en': 'English', 'ur': 'Urdu', 'hi': 'Hindi',
            'es': 'Spanish', 'fr': 'French', 'ar': 'Arabic',
            'pt': 'Portuguese', 'ru': 'Russian', 'de': 'German',
            'ja': 'Japanese', 'ko': 'Korean', 'zh-cn': 'Chinese',
            'id': 'Indonesian', 'tr': 'Turkish', 'fa': 'Persian',
            'bn': 'Bengali', 'pa': 'Punjabi', 'ta': 'Tamil',
            'it': 'Italian', 'nl': 'Dutch', 'pl': 'Polish',
        }
        return lang_map.get(lang_code, f"Other ({lang_code})")
    except LangDetectException:
        return "Unknown"
    except Exception:
        return "Unknown"