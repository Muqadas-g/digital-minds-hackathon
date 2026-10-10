# ============================================
# main.py - FastAPI Backend with Advanced Features
# ============================================

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from collections import Counter
from datetime import datetime
import re
import os

from sentiment import predict_sentiment, detect_language
from youtube_api import fetch_comments

app = FastAPI(title="Digital Minds API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "frontend"
)


class AnalyzeRequest(BaseModel):
    video_url: str
    max_comments: int = 100


@app.get("/api/health")
def health():
    return {"status": "ok", "message": "Digital Minds API is running"}


# ============================================
# Helper Functions
# ============================================

STOPWORDS = {
    'the','a','an','is','are','was','were','be','been','to','of','and','in','on',
    'at','for','with','by','this','that','it','i','you','he','she','we','they',
    'my','your','his','her','its','our','their','so','but','or','if','not','no',
    'do','does','did','have','has','had','will','would','can','could','should',
    'am','as','from','up','out','just','now','like','get','got','one','all','also'
}


def get_top_words(texts, n=8):
    all_words = []
    for text in texts:
        words = re.findall(r'\b[a-z]{3,}\b', text.lower())
        all_words.extend([w for w in words if w not in STOPWORDS])
    return [{"word": w, "count": c} for w, c in Counter(all_words).most_common(n)]


def extract_keywords(text):
    words = re.findall(r'\b[a-z]{4,}\b', text.lower())
    filtered = [w for w in words if w not in STOPWORDS]
    return list(set(filtered))[:3]


def get_timeline(comments_data):
    timeline = {}
    for item in comments_data:
        date_str = item.get("published_at", "")
        if not date_str:
            continue
        try:
            date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            key = date.strftime("%Y-%m-%d")
            if key not in timeline:
                timeline[key] = {"Positive": 0, "Neutral": 0, "Negative": 0}
            timeline[key][item["label"]] += 1
        except Exception:
            continue
    sorted_dates = sorted(timeline.keys())
    return [
        {"date": d, **timeline[d], "total": sum(timeline[d].values())}
        for d in sorted_dates
    ][-10:]


# ============================================
# Main Analyze Endpoint
# ============================================

@app.post("/api/analyze")
def analyze(request: AnalyzeRequest):
    try:
        result = fetch_comments(request.video_url, request.max_comments)
        comments_raw = result["comments"]

        if not comments_raw:
            raise HTTPException(status_code=400, detail="No comments found.")

        predictions = []
        counts = {"Positive": 0, "Neutral": 0, "Negative": 0}
        languages = Counter()
        positive_comments = []
        negative_comments = []
        neutral_comments = []

        for c in comments_raw:
            text = c["text"]
            pred = predict_sentiment(text)
            lang = detect_language(text)
            languages[lang] += 1

            item = {
                "text": text[:250],
                "label": pred["label"],
                "confidence": pred["confidence"],
                "language": lang,
                "likes": c["likes"],
                "published_at": c["published_at"],
                "author": c["author"],
                "keywords": extract_keywords(text)
            }
            predictions.append(item)
            counts[pred["label"]] += 1

            if pred["label"] == "Positive":
                positive_comments.append(text)
            elif pred["label"] == "Negative":
                negative_comments.append(text)
            else:
                neutral_comments.append(text)

        total = len(comments_raw)
        percentages = {
            "Positive": round(counts["Positive"] / total * 100, 2),
            "Neutral":  round(counts["Neutral"]  / total * 100, 2),
            "Negative": round(counts["Negative"] / total * 100, 2),
        }

        top_liked = sorted(predictions, key=lambda x: x["likes"], reverse=True)[:5]

        samples = {
            "positive": [c for c in predictions if c["label"] == "Positive"][:3],
            "neutral":  [c for c in predictions if c["label"] == "Neutral"][:3],
            "negative": [c for c in predictions if c["label"] == "Negative"][:3],
        }

        timeline = get_timeline(predictions)

        return {
            "video_id": result["video_id"],
            "video_title": result["video_title"],
            "total_comments_available": result["total_comments_available"],
            "video_stats": result["video_stats"],
            "comments_analyzed": total,
            "counts": counts,
            "percentages": percentages,
            "languages": dict(languages.most_common(10)),
            "top_positive_words": get_top_words(positive_comments),
            "top_negative_words": get_top_words(negative_comments),
            "top_neutral_words": get_top_words(neutral_comments),
            "top_liked_comments": top_liked,
            "sample_comments": samples,
            "timeline": timeline,
            "sample_predictions": predictions[:10]
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


# Serve frontend
if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/")
def root():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)