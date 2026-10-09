# ============================================
# main.py - FastAPI Backend
# ============================================

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os

from sentiment import predict_sentiment
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


@app.post("/api/analyze")
def analyze(request: AnalyzeRequest):
    try:
        result = fetch_comments(request.video_url, request.max_comments)
        comments = result["comments"]

        if not comments:
            raise HTTPException(status_code=400, detail="No comments found.")

        predictions = []
        counts = {"Positive": 0, "Neutral": 0, "Negative": 0}

        for comment in comments:
            pred = predict_sentiment(comment)
            predictions.append({
                "text": comment[:200],
                "label": pred["label"],
                "confidence": pred["confidence"]
            })
            counts[pred["label"]] += 1

        total = len(comments)
        percentages = {
            "Positive": round(counts["Positive"] / total * 100, 2),
            "Neutral":  round(counts["Neutral"]  / total * 100, 2),
            "Negative": round(counts["Negative"] / total * 100, 2),
        }

        return {
            "video_id": result["video_id"],
            "video_title": result["video_title"],
            "total_comments_available": result["total_comments_available"],
            "comments_analyzed": total,
            "counts": counts,
            "percentages": percentages,
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