# ============================================
# summarizer.py - YouTube Video Summarization
# Compatible with youtube-transcript-api 1.0.3+
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
    """Fetch YouTube video transcript in any available language."""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        raise ValueError("youtube-transcript-api not installed")

    # Try new API (v1.0.3+)
    try:
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)

        # Try English first
        transcript = None
        try:
            transcript = transcript_list.find_transcript(['en', 'en-US', 'en-GB'])
        except Exception:
            try:
                transcript = transcript_list.find_transcript(['hi', 'ur'])
            except Exception:
                # Get any available transcript
                for t in transcript_list:
                    transcript = t
                    break

        if transcript is None:
            raise ValueError("No transcript available for this video")

        # Fetch data
        data = transcript.fetch()

        # Handle both dict and object formats
        parts = []
        for item in data:
            if hasattr(item, 'text'):
                parts.append(item.text)
            elif isinstance(item, dict) and 'text' in item:
                parts.append(item['text'])
            elif hasattr(item, 'content'):
                parts.append(item.content)

        text = " ".join(parts)

        if not text.strip():
            raise ValueError("Transcript is empty")

        # Note language if not English
        lang_code = getattr(transcript, 'language_code', 'unknown')
        if lang_code not in ['en', 'en-US', 'en-GB']:
            lang_name = getattr(transcript, 'language', lang_code)
            text = f"[Original language: {lang_name}]\n\n{text}"

        return text

    except Exception as e:
        error_msg = str(e)

        # Try older API fallback
        try:
            for langs in [['en'], ['en-US'], ['hi'], ['ur'], ['en', 'hi', 'ur']]:
                try:
                    data = YouTubeTranscriptApi.get_transcript(video_id, languages=langs)
                    return " ".join([item["text"] for item in data])
                except Exception:
                    continue
        except Exception:
            pass

        # Friendly error messages
        if "disabled" in error_msg.lower():
            raise ValueError("Subtitles are disabled for this video")
        if "no transcript" in error_msg.lower() or "not found" in error_msg.lower():
            raise ValueError("No transcript available for this video")
        if "no element found" in error_msg.lower():
            raise ValueError("YouTube API returned empty response. Try another video.")

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
