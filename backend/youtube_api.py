# ============================================
# youtube_api.py - Fetch YouTube Comments
# ============================================

import os
import re
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


def extract_video_id(url: str) -> str:
    """Extract video ID from various YouTube URL formats."""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/|youtube\.com\/shorts\/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError("Invalid YouTube URL. Please provide a valid video URL.")


def fetch_comments(video_url: str, max_comments: int = 100) -> dict:
    """Fetch comments from a YouTube video."""
    if not YOUTUBE_API_KEY:
        raise ValueError("YouTube API key not configured. Add it to backend/.env")

    video_id = extract_video_id(video_url)
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    # Video details
    try:
        video_response = youtube.videos().list(
            part="snippet,statistics",
            id=video_id
        ).execute()
    except Exception as e:
        raise ValueError(f"Failed to fetch video details: {str(e)}")

    if not video_response.get("items"):
        raise ValueError("Video not found. Please check the URL.")

    video_data = video_response["items"][0]
    video_title = video_data["snippet"]["title"]
    comment_count = int(video_data["statistics"].get("commentCount", 0))

    if comment_count == 0:
        raise ValueError("Comments are disabled or not available for this video.")

    # Fetch comments
    comments = []
    next_page_token = None

    try:
        while len(comments) < max_comments:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=min(100, max_comments - len(comments)),
                pageToken=next_page_token,
                textFormat="plainText"
            )
            response = request.execute()

            for item in response.get("items", []):
                comment = item["snippet"]["topLevelComment"]["snippet"]
                text = comment["textDisplay"]
                if text and len(text.strip()) > 0:
                    comments.append(text)

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break
    except Exception as e:
        if "commentsDisabled" in str(e):
            raise ValueError("Comments are disabled for this video.")
        raise ValueError(f"Failed to fetch comments: {str(e)}")

    return {
        "video_id": video_id,
        "video_title": video_title,
        "total_comments_available": comment_count,
        "comments_fetched": len(comments),
        "comments": comments
    }