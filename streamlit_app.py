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
from youtube_api import fetch_comments

# Page config
st.set_page_config(
    page_title="AI-Powered YouTube Video Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS — ChatGPT-style layout
st.markdown("""
<style>
    .stApp {
        background-color: #0d0d0f;
        color: #ececf1;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    [data-testid="stSidebar"] {
        background-color: #16161c;
        border-right: 1px solid rgba(255,255,255,0.06);
    }
    
    h1, h2, h3 {
        color: #ffffff !important;
        font-weight: 600 !important;
        letter-spacing: -0.5px;
    }
    
    .stChatMessage {
        background-color: #1a1a24 !important;
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 12px;
    }
    
    .stTextInput > div > div > input {
        background-color: #1a1a24 !important;
        color: #ececf1 !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 12px !important;
        padding: 14px 18px !important;
        font-size: 15px !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #8b5cf6 !important;
        box-shadow: 0 0 0 3px rgba(139,92,246,0.15) !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #8b5cf6, #a855f7) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 28px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        transition: all 0.2s !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 20px rgba(139,92,246,0.4) !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 32px !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #a1a1aa !important;
        font-size: 13px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    hr {
        border-color: rgba(255,255,255,0.08) !important;
        margin: 24px 0 !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #1a1a24;
        border-radius: 8px;
        padding: 10px 20px;
        color: #a1a1aa;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: rgba(139,92,246,0.15) !important;
        color: #c4b5fd !important;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar — Technical Info Only
with st.sidebar:
    st.markdown("""
    <div style="padding: 8px 0 20px 0;">
        <h2 style="color: #ffffff; font-size: 18px; margin: 0; line-height: 1.3;">
            AI-Powered YouTube Video Analyzer
        </h2>
        <p style="color: #71717a; font-size: 13px; margin: 6px 0 0 0;">
            Sentiment Analysis System
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### System Overview")
    st.markdown("""
    <p style="color: #a1a1aa; font-size: 13px; line-height: 1.7;">
    An AI-powered tool that analyzes YouTube video comments 
    using Machine Learning and Natural Language Processing.
    </p>
    """, unsafe_allow_html=True)
    
    st.markdown("### Capabilities")
    st.markdown("""
    <div style="color: #d4d4d8; font-size: 13px; line-height: 2;">
    • Real-time sentiment analysis<br>
    • Language detection<br>
    • Sentiment timeline<br>
    • Top liked comments<br>
    • Keyword extraction<br>
    • Interactive charts
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Model Information")
    st.markdown("""
    <div style="color: #d4d4d8; font-size: 13px; line-height: 2;">
    <b style="color: #a1a1aa;">Algorithm:</b> Logistic Regression<br>
    <b style="color: #a1a1aa;">Vectorizer:</b> TF-IDF (50K features)<br>
    <b style="color: #a1a1aa;">Accuracy:</b> 81.17%<br>
    <b style="color: #a1a1aa;">F1-Score:</b> 0.8117<br>
    <b style="color: #a1a1aa;">Dataset:</b> Sentiment140
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <div style="text-align: center; padding: 12px 0;">
        <span style="background: rgba(139,92,246,0.15); color: #c4b5fd; 
        font-size: 11px; font-weight: 600; padding: 6px 14px; 
        border-radius: 100px; border: 1px solid rgba(139,92,246,0.3);">
        Hackathon 2026
        </span>
    </div>
    """, unsafe_allow_html=True)


# Main content
st.markdown("""
<div style="text-align: center; padding: 40px 0 20px 0;">
    <h1 style="font-size: 32px; color: #ffffff; margin-bottom: 8px;">
        AI-Powered YouTube Video Analyzer
    </h1>
    <p style="color: #71717a; font-size: 15px;">
        Paste any YouTube video URL below to analyze comment sentiment
    </p>
</div>
""", unsafe_allow_html=True)

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome message
if len(st.session_state.messages) == 0:
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown("""
        **Welcome!**
        
        I can analyze the sentiment of comments on any YouTube video. 
        Just paste a video URL below and I'll break down the audience's 
        mood into **Positive**, **Neutral**, and **Negative** categories 
        with interactive charts.
        
        **Try it:** Paste a YouTube URL to get started.
        """)

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message.get("avatar", "👤")):
        st.markdown(message["content"])

# Chat input
video_url = st.chat_input("Paste a YouTube video URL here...")

if video_url:
    st.session_state.messages.append({
        "role": "user",
        "content": video_url,
        "avatar": "👤"
    })
    
    with st.chat_message("user", avatar="👤"):
        st.markdown(video_url)
    
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Analyzing comments..."):
            try:
                result = fetch_comments(video_url, max_comments=100)
                comments_raw = result["comments"]

                if not comments_raw:
                    st.error("No comments found for this video.")
                else:
                    predictions = []
                    counts = {"Positive": 0, "Neutral": 0, "Negative": 0}
                    languages = Counter()

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
                        }
                        predictions.append(item)
                        counts[pred["label"]] += 1

                    total = len(comments_raw)
                    percentages = {
                        "Positive": round(counts["Positive"] / total * 100, 2),
                        "Neutral": round(counts["Neutral"] / total * 100, 2),
                        "Negative": round(counts["Negative"] / total * 100, 2),
                    }

                    st.markdown(f"**Analysis Complete**")
                    st.markdown(f"**Video:** {result['video_title']}")
                    st.markdown(f"**Analyzed:** {total} comments (out of {result['total_comments_available']} available)")
                    
                    stats = result.get("video_stats", {})
                    st.markdown(f"**Views:** {stats.get('views', 0):,} · **Likes:** {stats.get('likes', 0):,}")

                    st.markdown("---")

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
                        paper_bgcolor="#0d0d0f",
                        plot_bgcolor="#0d0d0f",
                        font=dict(color="#ececf1"),
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)

                    st.markdown("### Languages Detected")
                    lang_cols = st.columns(min(len(languages), 5))
                    for i, (lang, count) in enumerate(languages.most_common(5)):
                        with lang_cols[i]:
                            st.metric(lang, count)

                    st.markdown("### Top Liked Comments")
                    top_liked = sorted(predictions, key=lambda x: x["likes"], reverse=True)[:5]
                    for i, c in enumerate(top_liked, 1):
                        st.markdown(f"**#{i}** · {c['likes']} likes · {c['label']}")
                        st.caption(c["text"])

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

            except ValueError as e:
                st.error(f"{str(e)}")
            except Exception as e:
                st.error(f"Error: {str(e)}")

st.markdown("---")
st.caption("Analysis results are generated by an ML model and may not be 100% accurate.")
