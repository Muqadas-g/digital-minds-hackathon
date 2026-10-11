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
    page_title="Digital Minds — YouTube Sentiment Analysis",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS (purple theme)
st.markdown("""
<style>
    .stApp {
        background-color: #0f0f12;
        color: #ececf1;
    }
    h1, h2, h3 {
        color: #c4b5fd !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #8b5cf6, #a855f7);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
    }
    .metric-card {
        background: #1e1e26;
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🧠 Digital Minds")
    st.markdown("*YouTube Sentiment Analysis*")
    st.markdown("---")
    st.markdown("### 📖 About Project")
    st.markdown("""
    **Digital Minds** is a Machine Learning project that analyzes the sentiment of YouTube comments.
    
    **Features:**
    - Real-time sentiment analysis
    - Language detection
    - Top liked comments
    - Sentiment timeline
    - Keyword highlighting
    """)
    st.markdown("---")
    st.markdown("### 🤖 ML Model")
    st.markdown("""
    - **Algorithm:** Logistic Regression
    - **Accuracy:** 81.17%
    - **F1-Score:** 0.8117
    - **Dataset:** Sentiment140
    """)
    st.markdown("---")
    st.markdown("### 👥 Team")
    st.markdown("""
    **Faculty Lead:**
    Muqaddas Imtiaz
    
    **Members:**
    - Sonia Kumari
    - Khadija Mahar
    
    **Hackathon 2026**
    """)

# Main content
st.title("🧠 Digital Minds")
st.markdown("### YouTube Comment Sentiment Analysis")
st.markdown("Paste any YouTube video URL to analyze the sentiment of its comments.")
st.markdown("---")

# Input
col1, col2 = st.columns([4, 1])
with col1:
    video_url = st.text_input(
        "YouTube URL",
        placeholder="https://youtu.be/...",
        label_visibility="collapsed"
    )
with col2:
    analyze_btn = st.button("🔍 Analyze", use_container_width=True)

# Analyze
if analyze_btn and video_url:
    with st.spinner("Fetching comments and analyzing sentiment..."):
        try:
            result = fetch_comments(video_url, max_comments=100)
            comments_raw = result["comments"]

            if not comments_raw:
                st.error("No comments found for this video.")
            else:
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
                        "keywords": self_extract_keywords(text) if False else []
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
                    "Neutral": round(counts["Neutral"] / total * 100, 2),
                    "Negative": round(counts["Negative"] / total * 100, 2),
                }

                # Video info
                st.success("✅ Analysis Complete!")
                st.markdown(f"**🎥 Video:** {result['video_title']}")
                st.markdown(f"**📊 Analyzed:** {total} comments (out of {result['total_comments_available']} available)")
                
                stats = result.get("video_stats", {})
                st.markdown(f"**👁️ Views:** {stats.get('views', 0):,} · **👍 Likes:** {stats.get('likes', 0):,}")

                st.markdown("---")

                # Metric cards
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric("😊 Positive", f"{percentages['Positive']}%", f"{counts['Positive']} comments")
                with c2:
                    st.metric("😐 Neutral", f"{percentages['Neutral']}%", f"{counts['Neutral']} comments")
                with c3:
                    st.metric("😞 Negative", f"{percentages['Negative']}%", f"{counts['Negative']} comments")

                # Chart
                fig = go.Figure(data=[go.Pie(
                    labels=["Positive", "Neutral", "Negative"],
                    values=[percentages["Positive"], percentages["Neutral"], percentages["Negative"]],
                    hole=0.6,
                    marker=dict(colors=["#10b981", "#f59e0b", "#ef4444"])
                )])
                fig.update_layout(
                    title="Sentiment Distribution",
                    paper_bgcolor="#0f0f12",
                    plot_bgcolor="#0f0f12",
                    font=dict(color="#ececf1"),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)

                # Languages
                st.markdown("### 🌐 Languages Detected")
                lang_cols = st.columns(min(len(languages), 5))
                for i, (lang, count) in enumerate(languages.most_common(5)):
                    with lang_cols[i]:
                        st.metric(lang, count)

                # Top liked comments
                st.markdown("### 🔥 Top Liked Comments")
                top_liked = sorted(predictions, key=lambda x: x["likes"], reverse=True)[:5]
                for i, c in enumerate(top_liked, 1):
                    emoji = "😊" if c["label"] == "Positive" else "😞" if c["label"] == "Negative" else "😐"
                    st.markdown(f"**#{i}** · 👍 {c['likes']} · {emoji} {c['label']}")
                    st.caption(c["text"])

                # Sample comments
                st.markdown("### 💬 Sample Comments")
                tab1, tab2, tab3 = st.tabs(["😊 Positive", "😐 Neutral", "😞 Negative"])
                with tab1:
                    for c in predictions:
                        if c["label"] == "Positive":
                            st.markdown(f"- {c['text']}")
                            if len([x for x in predictions if x['label'] == 'Positive'][:5]) <= 5:
                                break
                with tab2:
                    for c in predictions:
                        if c["label"] == "Neutral":
                            st.markdown(f"- {c['text']}")
                with tab3:
                    for c in predictions:
                        if c["label"] == "Negative":
                            st.markdown(f"- {c['text']}")

        except ValueError as e:
            st.error(f"❌ {str(e)}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

elif analyze_btn and not video_url:
    st.warning("⚠️ Please enter a YouTube URL.")

# Footer
st.markdown("---")
st.caption("Digital Minds AI may produce inaccurate results. Always verify important insights.")
