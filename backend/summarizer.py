# ============================================
# summarizer.py - YouTube Video Summarization
# Uses pytube to bypass YouTube IP blocks on cloud
# ============================================

import os
import re
import google.generativeai as genai

try:
    import streamlit as st
    GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", None)
except Exception:
    GEMINI_API_KEY = None

if not GEMINI_API_KEY:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


def fetch_transcript(video_id: str) -> str:
    """Fetch YouTube video transcript using pytube (bypasses IP blocks)."""
    try:
        from pytube import YouTube
    except ImportError:
        raise ValueError("pytube not installed")

    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        yt = YouTube(url)
        captions = yt.captions

        if not captions:
            raise ValueError("No captions available for this video")

        # Try English first
        caption = None
        for cap in captions:
            if cap.code.startswith('en'):
                caption = cap
                break

        # Try Hindi or Urdu
        if caption is None:
            for cap in captions:
                if cap.code.startswith('hi') or cap.code.startswith('ur'):
                    caption = cap
                    break

        # Any available
        if caption is None:
            caption = list(captions)[0]

        # Generate SRT and clean it
        srt = caption.generate_srt_captions()
        # Remove timestamps and numbers
        text = re.sub(r'\d+\n', '', srt)
        text = re.sub(r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}', '', text)
        text = re.sub(r'<[^>]+>', '', text)
        text = re.sub(r'\s+', ' ', text).strip()

        if not text:
            raise ValueError("Transcript is empty")

        # Note if non-English
        if not caption.code.startswith('en'):
            text = f"[Original language: {caption.code}]\n\n{text}"

        return text

    except Exception as e:
        error_msg = str(e)
        if "unavailable" in error_msg.lower():
            raise ValueError("Video is unavailable or private")
        if "age" in error_msg.lower():
            raise ValueError("Age-restricted video — cannot fetch transcript")
        raise ValueError(f"Could not fetch transcript: {error_msg}")


def generate_summary(transcript: str, video_title: str) -> dict:
    """Generate AI summary from transcript using Gemini."""
    if not GEMINI_API_KEY:
        raise ValueError("Gemini API key not configured.")

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        transcript_short = transcript[:20000]

        prompt = f"""
        Analyze this YouTube video transcript and provide a clear summary.

        IMPORTANT: If the transcript is in a language other than English,
        translate it internally and provide the summary in ENGLISH.

        1. **Video Type**: Lecture / Tutorial / Documentary / Interview / Review / News
        2. **Purpose**: What is this video about? (1 sentence)
        3. **Topic**: Main subject covered
        4. **Summary**: A clear 2-minute summary in simple English (3-4 paragraphs)
        5. **Key Points**: 5-7 main takeaways (bullet points)
        6. **Target Audience**: Beginner / Intermediate / Advanced

        Video Title: {video_title}

        Transcript:
        {transcript_short}

        Format your response as clear, structured text with the exact headings above.
        """

        response = model.generate_content(prompt)
        return {"summary": response.text}

    except Exception as e:
        raise ValueError(f"Failed to generate summary: {str(e)}")


def translate_to_urdu(text: str) -> str:
    """Translate English summary to Urdu."""
    try:
        from deep_translator import GoogleTranslator
        max_chunk = 4500
        chunks = [text[i:i+max_chunk] for i in range(0, len(text), max_chunk)]
        translated = []
        for chunk in chunks:
            result = GoogleTranslator(source='en', target='ur').translate(chunk)
            translated.append(result)
        return " ".join(translated)
    except Exception as e:
        return f"Translation unavailable: {str(e)}"
