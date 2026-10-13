# AI-Powered YouTube Video Analyzer

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40-FF4B4B?logo=streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.5-F7931E?logo=scikit-learn&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini-AI-4285F4?logo=google&logoColor=white)
![Hackathon](https://img.shields.io/badge/OpenHack-2026-purple)

> An AI-powered web application that analyzes YouTube video comments and generates smart video summaries for students.

**Team:** Digital Minds | **Event:** OpenHack 2026 | **Category:** EdTech

---

## 🔗 Links

- **Live App:** https://digital-minds-hackathon-4wjbxer5rhssflkv2xibut.streamlit.app/
- **GitHub Repo:** https://github.com/Muqadas-g/digital-minds-hackathon
- **Kaggle Notebook:** https://www.kaggle.com/code/muqaddasimtiaz/hackathon-project
- **Presentation (PPT):** https://docs.google.com/presentation/d/1inWlLFgFTFHU_QFGusOSvhzsP6gFH_um/edit?usp=sharing

---

## 🧠 Machine Learning Model

The sentiment classification model was **trained on Kaggle Notebooks** using the **Sentiment140 dataset** (1.6 million labeled tweets).

- **Algorithm:** Logistic Regression
- **Vectorizer:** TF-IDF (50,000 features, n-grams 1-2)
- **Training Samples:** 396,883
- **Test Samples:** 99,221
- **Dataset Used:** 497,152 balanced samples (248,576 Positive + 248,576 Negative)

**Evaluation Metrics:**

| Metric | Value |
|--------|-------|
| Accuracy | **81.17%** |
| Precision | 0.8118 |
| Recall | 0.8117 |
| F1-Score | 0.8117 |

📓 **Kaggle Notebook:** https://www.kaggle.com/code/muqaddasimtiaz/hackathon-project

---

## ✨ Features

- **Comment Sentiment Analysis** — Classifies up to 100 YouTube comments as Positive, Neutral, or Negative
- **Sentiment Distribution Chart** — Interactive doughnut chart with percentages
- **Language Detection** — Detects English, Urdu, Hindi, Turkish, and more
- **Top Liked Comments** — Shows the most engaged comments with sentiment labels
- **Sample Comments** — Real examples per sentiment category
- **Video Statistics** — Views, likes, and total comment count
- **Video Summarization** — AI-generated 2-minute summary with video type, purpose, and key points
- **Urdu Translation** — اردو خلاصہ of the video summary for Pakistani students
- **Dark / Light Theme** — Toggle between themes
- **Clean Chatbot UI** — Modern and mobile-responsive

---

## 🎯 Benefits

- **For Students** — Quickly understand a 2-hour lecture in 2 minutes
- **For Content Creators** — Measure audience sentiment without reading thousands of comments
- **For Researchers** — Free baseline for YouTube sentiment analysis
- **For Everyone** — Completely free, no subscription required
- **Multilingual Access** — Urdu summaries for non-English speakers

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit, Plotly |
| Backend | Python 3.11 |
| ML / NLP | Scikit-learn, TF-IDF, Logistic Regression |
| AI Summarization | Google Gemini API |
| YouTube Data | YouTube Data API v3 |
| Transcript | pytube |
| Translation | deep-translator |
| Deployment | Streamlit Cloud |

---

## ⚙️ How It Works

1. User pastes a YouTube video URL
2. YouTube Data API fetches up to 100 comments
3. Comments are cleaned and vectorized with TF-IDF
4. Logistic Regression classifies each comment (Positive / Neutral / Negative)
5. Results are displayed as cards, doughnut chart, and statistics
6. For summarization, transcript is fetched and sent to Gemini API for AI-generated summary

---

## ⚠️ Limitations

- **Videos Without Captions (CC)** — Videos without subtitles enabled cannot be summarized
- **YouTube Cloud IP Restrictions** — YouTube may block transcript requests from cloud provider IPs; summarization works in the local version
- **Domain Mismatch** — Model trained on Twitter data, so accuracy on YouTube comments may vary
- **Sarcasm and Negation** — Complex sentence structures may be difficult for the model
- **API Quotas** — YouTube Data API has a daily quota limit (10,000 units/day on free tier)

---

## 🔮 Future Work

- Full multilingual sentiment analysis (Urdu, Hindi, Sindhi)
- Transformer models (BERT, RoBERTa) for higher accuracy
- Emotion detection beyond sentiment
- Q&A feature for video content
- Quiz generator for students
- PDF notes download
- Mobile app version

---

## 👥 Team

**Team Name:** Digital Minds | **Event:** OpenHack 2026 | **Category:** EdTech

| Role | Member |
|------|--------|
| Faculty Lead / ML Engineer | Muqaddas Imtiaz — Final Year BS Data Science, QUEST University Nawabshah |
| Team Member | Sonia Kumari — 25SW, 2nd Year, MUET SZAB Campus |
| Team Member | Khadija Mahar — 25SW, 2nd Year, MUET SZAB Campus |

---

## 🤖 AI & Open-Source Disclosure

**AI Tools Used:**
- Google Gemini API (gemini-1.5-flash) — Video summarization
- ChatGPT / Claude — Development assistance

**Open-Source Technologies:**
- Streamlit, Plotly, scikit-learn, pytube, deep-translator, langdetect, FastAPI

**Dataset:**
- Sentiment140 (Kaggle) — 1.6 million labeled tweets

---

<p align="center">
  <strong>Built with ❤️ by Team Digital Minds</strong><br>
  <em>OpenHack 2026 — Build. Solve. Demonstrate.</em>
</p>
