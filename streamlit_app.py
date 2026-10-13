import streamlit as st
import sys
import os
import plotly.graph_objects as go
from collections import Counter
from datetime import datetime
import re

# Add backend path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from sentiment import predict_sentiment, detect_language
from youtube_api import fetch_comments, extract_video_id
from summarizer import fetch_transcript, generate_summary, translate_to_urdu

# Page config
st.set_page_config(
    page_title="AI-Powered YouTube Video Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# Theme colors
if st.session_state.theme == "dark":
    bg_main = "#0d0d0f"
    bg_sidebar = "#16161c"
    bg_card = "#1a1a24"
    text_primary = "#ececf1"
    text_secondary = "#a1a1aa"
    text_muted = "#71717a"
    border = "rgba(255,255,255,0.06)"
    border_strong = "rgba(255,255,255,0.1)"
else:
    bg_main = "#f7f7f8"
    bg_sidebar = "#ffffff"
    bg_card = "#f3f4f6"
    text_primary = "#18181b"
    text_secondary = "#52525b"
    text_muted = "#a1a1aa"
    border = "rgba(0,0,0,0.06)"
    border_strong = "rgba(0,0,0,0.1)"

# Custom CSS
st.markdown(f"""
<style>
    .stApp {{ background-color: {bg_main}; color: {text_primary}; }}
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    [data-testid="stSidebar"] {{ background-color: {bg_sidebar}; border-right: 1px solid {border}; }}
    h1, h2, h3 {{ color: {text_primary} !important; font-weight: 600 !important; letter-spacing: -0.5px; }}
    .stChatMessage {{ background-color: {bg_card} !important; border: 1px solid {border}; border-radius: 12px; }}
    .stButton > button {{
        background: linear-gradient(135deg, #8b5cf6, #a855f7) !important;
        color: white !important; border: none !important;
        border-radius: 12px !important; padding: 12px 24px !important;
        font-weight: 600 !important; font-size: 14px !important;
        width: 100% !important; transition: all 0.2s !important;
    }}
    .stButton > button:hover {{ transform: translateY(-1px); box-shadow: 0 8px 20px rgba(139,92,246,0.4) !important; }}
    [data-testid="stMetricValue"] {{ color: {text_primary} !important; font-size: 32px !important; font-weight: 700 !important; }}
    [data-testid="stMetricLabel"] {{ color: {text_secondary} !important; font-size: 13px !important; text-transform: uppercase; letter-spacing: 0.5px; }}
    hr {{ border-color: {border} !important; margin: 24px 0 !important; }}
    .stTabs [data-baseweb="tab-list"] {{ gap: 8px; background-color: transparent; }}
    .stTabs [data-baseweb="tab"] {{ background-color: {bg_card}; border-radius: 8px; padding: 10px 20px; color: {text_secondary}; font-weight: 500; }}
    .stTabs [aria-selected="true"] {{ background-color: rgba(139,92,246,0.15) !important; color: #c4b5fd !important; }}
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown(f"""
    <div style="padding: 8px 0 20px 0;">
        <h2 style="color: {text_primary}; font-size: 17px; margin: 0; line-height: 1.3;">
            AI-Powered YouTube Video Analyzer
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    theme_icon = "Light Mode" if st.session_state.theme == "dark" else "Dark Mode"
    if st.button(theme_icon, use_container_width=True):
        st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
        st.rerun()

# Main title
st.markdown(f"""
<div style="text-align: center; padding: 40px 0 20px 0;">
    <h1 style="font-size: 32px; color: {text_primary}; margin-bottom: 8px;">
        AI-Powered YouTube Video Analyzer
    </h1>
    <p style="color: {text_muted}; font-size: 15px;">
        Paste any YouTube video URL to analyze comments and get a quick summary
    </p>
</div>
""", unsafe_allow_html=True)

# Welcome
if len(st.session_state.messages) == 0:
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown("""
        **Welcome!**
        
        I can analyze any YouTube video:
        - **Comment Sentiment** — Positive / Neutral / Negative breakdown
        - **Video Summary** — 2-minute read of the whole video
        - **Key Points** — Main takeaways for students
        - **Urdu Translation** — اردو خلاصہ
        
        **Try it:** Paste a YouTube URL below.
        """)

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message.get("avatar", "👤")):
        st.markdown(message["content"])

video_url = st.chat_input("Paste a YouTube video URL here...")

if video_url:
    st.session_state.messages.append({"role": "user", "content": video_url, "avatar": "👤"})
    
    with st.chat_message("user", avatar="👤"):
        st.markdown(video_url)
    
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Analyzing video..."):
            try:
                # Try to fetch comments (may fail)
                comments_raw = []
                result = {}
                try:
                    result = fetch_comments(video_url, max_comments=100)
                    comments_raw = result["comments"]
                except Exception as e:
                    st.warning(f"Comments unavailable: {str(e)}")
                    # Try to get video ID for summary
                    try:
                        video_id = extract_video_id(video_url)
                        result = {"video_id": video_id, "video_title": "Video", "total_comments_available": 0, "video_stats": {}}
                    except Exception:
                        raise ValueError("Invalid YouTube URL.")

                # Sentiment analysis (if comments available)
                if comments_raw:
                    predictions = []
                    counts = {"Positive": 0, "Neutral": 0, "Negative": 0}
                    languages = Counter()

                    for c in comments_raw:
                        text = c["text"]
                        pred = predict_sentiment(text)
                        lang = detect_language(text)
                        languages[lang] += 1

                        item = {
                            "text": text[:250], "label": pred["label"],
                            "confidence": pred["confidence"], "language": lang,
                            "likes": c["likes"], "published_at": c["published_at"],
                        }
                        predictions.append(item)
                        counts[pred["label"]] += 1

                    total = len(comments_raw)
                    percentages = {
                        "Positive": round(counts["Positive"] / total * 100, 2),
                        "Neutral": round(counts["Neutral"] / total * 100, 2),
                        "Negative": round(counts["Negative"] / total * 100, 2),
                    }

                    st.markdown(f"**Video:** {result.get('video_title', 'N/A')}")
                    st.markdown(f"**Analyzed:** {total} comments (out of {result.get('total_comments_available', 0)} available)")
                    
                    stats = result.get("video_stats", {})
                    if stats:
                        st.markdown(f"**Views:** {stats.get('views', 0):,} · **Likes:** {stats.get('likes', 0):,}")

                    st.markdown("---")
                    st.markdown("### Comment Sentiment")

                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.metric("Positive", f"{percentages['Positive']}%", f"{counts['Positive']} comments")
                    with c2:
                        st.metric("Neutral", f"{percentages['Neutral']}%", f"{counts['Neutral']} comments")
                    with c3:
                        st.metric("Negative", f"{percentages['Negative']}%", f"{counts['Negative']} comments")

                    fig = go.Figure(data=[go.Pie(
                        labels=["Positive", "Neutral", "Negative"],
                        values=[percentages["Positive"], percentages["Neutral"], percentages["Negative"]],
                        hole=0.6,
                        marker=dict(colors=["#10b981", "#f59e0b", "#ef4444"])
                    )])
                    fig.update_layout(
                        title="Sentiment Distribution",
                        paper_bgcolor=bg_main, plot_bgcolor=bg_main,
                        font=dict(color=text_primary), height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)

                    # Languages
                    st.markdown("### Languages Detected")
                    lang_cols = st.columns(min(len(languages), 5))
                    for i, (lang, count) in enumerate(languages.most_common(5)):
                        with lang_cols[i]:
                            st.metric(lang, count)

                    # Top Liked
                    st.markdown("### Top Liked Comments")
                    top_liked = sorted(predictions, key=lambda x: x["likes"], reverse=True)[:5]
                    for i, c in enumerate(top_liked, 1):
                        st.markdown(f"**#{i}** · {c['likes']} likes · {c['label']}")
                        st.caption(c["text"])

                    # Samples
                    st.markdown("### Sample Comments")
                    tab1, tab2, tab3 = st.tabs(["Positive", "Neutral", "Negative"])
                    with tab1:
                        for c in [x for x in predictions if x["label"] == "Positive"][:5]:
                            st.markdown(f"- {c['text']}")
                    with tab2:
                        for c in [x for x in predictions if x["label"] == "Neutral"][:5]:
                            st.markdown(f"- {c['text']}")
                    with tab3:
                        for c in [x for x in predictions if x["label"] == "Negative"][:5]:
                            st.markdown(f"- {c['text']}")

                # ==================
                # VIDEO SUMMARY SECTION
                # ==================
                st.markdown("---")
                st.markdown("### Video Summary")
                st.markdown("*Get a 2-minute read of the whole video — perfect for students.*")
                
                with st.spinner("Generating AI summary..."):
                    try:
                        video_id = result.get("video_id")
                        if not video_id:
                            raise ValueError("Video ID not found")
                        
                        transcript = fetch_transcript(video_id)
                        video_title = result.get("video_title", "Video")
                        summary_data = generate_summary(transcript, video_title)
                        
                        st.markdown(summary_data["summary"])
                        
                        if st.button("Translate to Urdu"):
                            with st.spinner("Translating to Urdu..."):
                                urdu_summary = translate_to_urdu(summary_data["summary"])
                                st.markdown("### اردو خلاصہ")
                                st.markdown(urdu_summary)
                    
                    except ValueError as e:
                        st.info(f"Summary not available: {str(e)}")

            except ValueError as e:
                st.error(f"{str(e)}")
            except Exception as e:
                st.error(f"Error: {str(e)}")

st.markdown("---")
st.caption("AI-generated analysis. Results may not be 100% accurate.")
