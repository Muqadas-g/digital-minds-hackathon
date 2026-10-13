# ============================================
# summarizer.py - YouTube Video Summarization
# ============================================

import os
import re
import google.generativeai as genai

# Try Streamlit secrets first, then fall back to .env
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
    """Fetch YouTube video transcript."""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([item["text"] for item in transcript_list])
        return transcript
    except Exception as e:
        raise ValueError(f"Could not fetch transcript: {str(e)}")


def generate_summary(transcript: str, video_title: str) -> dict:
    """Generate AI summary from transcript using Gemini."""
    if not GEMINI_API_KEY:
        raise ValueError("Gemini API key not configured. Add it to Streamlit Secrets.")

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Limit transcript length
        transcript_short = transcript[:15000]
        
        prompt = f"""
        Analyze this YouTube video transcript and provide:

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
        # Split into chunks if too long
        max_chunk = 4500
        chunks = [text[i:i+max_chunk] for i in range(0, len(text), max_chunk)]
        translated = []
        for chunk in chunks:
            result = GoogleTranslator(source='en', target='ur').translate(chunk)
            translated.append(result)
        return " ".join(translated)
    except Exception as e:
        return f"Translation unavailable: {str(e)}"
