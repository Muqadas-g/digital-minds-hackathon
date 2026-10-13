# ============================================
# summarizer.py - YouTube Video Summarization
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
        
        # Try multiple languages: English first, then Hindi, then Urdu, then any
        try:
            # Try listing all available transcripts
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            # Priority: manual English, auto English, Hindi, Urdu, or any available
            transcript = None
            try:
                transcript = transcript_list.find_transcript(['en', 'en-US', 'en-GB'])
            except Exception:
                try:
                    transcript = transcript_list.find_transcript(['hi', 'ur'])
                except Exception:
                    # Get any available transcript (first one)
                    for t in transcript_list:
                        transcript = t
                        break
            
            if transcript is None:
                raise ValueError("No transcript available for this video")
            
            # Fetch the transcript data
            data = transcript.fetch()
            text = " ".join([item["text"] for item in data])
            
            # If transcript is not English, note the language
            if transcript.language_code not in ['en', 'en-US', 'en-GB']:
                text = f"[Original language: {transcript.language}]\n\n{text}"
            
            return text
            
        except Exception as e:
            # Fallback: try direct get_transcript with common languages
            for lang in [['en'], ['hi'], ['ur'], ['en', 'hi']]:
                try:
                    transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=lang)
                    return " ".join([item["text"] for item in transcript_list])
                except Exception:
                    continue
            raise ValueError(f"No transcript available: {str(e)}")
            
    except Exception as e:
        raise ValueError(f"Could not fetch transcript: {str(e)}")


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
