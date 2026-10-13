# Bhai, Yeh Lo — Professional README (Markdown File Ke Liye)

**Copy-paste ready. GitHub pe `README.md` mein paste karo.**

---

```markdown
# AI-Powered YouTube Video Analyzer

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40-FF4B4B?logo=streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.5-F7931E?logo=scikit-learn&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini-AI-4285F4?logo=google&logoColor=white)
![Hackathon](https://img.shields.io/badge/OpenHack-2026-purple)

> An AI-powered web application that analyzes YouTube video comments and generates smart video summaries for students.

**Team:** Digital Minds  
**Event:** OpenHack 2026  
**Category:** EdTech

---

## 🌐 Live Demo

**Live App:** https://digital-minds-hackathon-4wjbxer5rhssflkv2xibut.streamlit.app/

**Kaggle Notebook:** https://www.kaggle.com/code/muqaddasimtiaz/hackathon-project

---

## ✨ Features

### Comment Sentiment Analysis
- Paste any YouTube video URL
- Fetches up to 100 top-level comments via YouTube Data API v3
- Classifies each comment as **Positive**, **Neutral**, or **Negative**
- Interactive doughnut chart with sentiment distribution

### Sentiment Insights
- **Languages Detected** — English, Urdu, Hindi, Turkish, and more
- **Top Liked Comments** — Most engaged comments with sentiment labels
- **Sample Comments** — Real examples per sentiment category
- **Video Stats** — Views, likes, and comment count

### Video Summarization (EdTech Feature)
- 2-minute AI-powered summary of the entire video
- **Video Type Detection** — Lecture, Tutorial, Documentary, etc.
- **Purpose and Topic** — What the video covers
- **Key Points** — Top takeaways for quick revision
- **Target Audience** — Beginner / Intermediate / Advanced
- **Urdu Translation** — اردو خلاصہ for Pakistani students

### Modern UI
- Dark and Light theme toggle
- Clean chatbot-style interface
- Real-time progress indicators
- Mobile responsive

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Streamlit, Plotly |
| **Backend** | Python 3.11 |
| **ML / NLP** | Scikit-learn, TF-IDF, Logistic Regression |
| **AI Summarization** | Google Gemini API |
| **YouTube Data** | YouTube Data API v3 |
| **Transcript** | pytube |
| **Translation** | deep-translator |
| **Deployment** | Streamlit Cloud |

---

## 🧠 ML Model Details

| Metric | Value |
|--------|-------|
| **Algorithm** | Logistic Regression |
| **Vectorizer** | TF-IDF (50,000 features, n-grams 1-2) |
| **Training Samples** | 396,883 |
| **Test Samples** | 99,221 |
| **Accuracy** | **81.17%** |
| **Precision** | 0.8118 |
| **Recall** | 0.8117 |
| **F1-Score** | 0.8117 |

**Dataset:** Sentiment140 (Kaggle) — 1.6 million labeled tweets  
**Used:** 497,152 balanced samples (248,576 Positive + 248,576 Negative)

---

## ⚙️ How It Works

### Comment Sentiment Pipeline
1. User pastes a YouTube video URL
2. YouTube Data API fetches up to 100 comments
3. Text preprocessing — lowercasing, URL / mention / punctuation removal
4. TF-IDF vectorization (50K features)
5. Logistic Regression classifies each comment
6. Neutral detection via probability threshold (40%–60%)
7. Results displayed as cards and interactive doughnut chart

### Video Summarization Pipeline
1. Extract video ID from URL
2. Fetch transcript via pytube
3. Send transcript to Gemini API for summarization
4. Generate structured summary with type, purpose, and key points
5. Optional Urdu translation via deep-translator

---

## 📁 Project Structure

```
digital-minds-hackathon/
│
├── backend/
│   ├── sentiment.py           # ML model loading and prediction
│   ├── youtube_api.py         # YouTube Data API integration
│   ├── summarizer.py          # Gemini-powered video summarization
│   └── requirements.txt
│
├── frontend/
│   ├── index.html             # Original chatbot UI
│   ├── style.css
│   └── script.js
│
├── models/
│   ├── sentiment_pipeline.joblib
│   ├── label_mapping.json
│   └── model_info.json
│
├── streamlit_app.py           # Main Streamlit application
├── requirements.txt           # Root dependencies
├── runtime.txt
├── README.md
└── .gitignore
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.11+
- YouTube Data API v3 key
- Google Gemini API key

### Steps

**1. Clone the repository**
```bash
git clone https://github.com/Muqadas-g/digital-minds-hackathon.git
cd digital-minds-hackathon
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure API keys**

Create `backend/.env`:
```env
YOUTUBE_API_KEY=your_youtube_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

**4. Run the app**
```bash
streamlit run streamlit_app.py
```

---

## 📓 Kaggle Notebook

The complete ML pipeline — data loading, EDA, preprocessing, model training, evaluation, and saving — was developed in a Kaggle Notebook.

🔗 **View Notebook:** https://www.kaggle.com/code/muqaddasimtiaz/hackathon-project

---

## ⚠️ Known Limitations

1. **Videos Without Captions (CC)** — Videos that do not have subtitles / CC enabled cannot be summarized. The app displays a clear message: *"Subtitles (CC) are not available for this video."*

2. **YouTube Cloud IP Restrictions** — YouTube may block transcript requests from cloud provider IPs (Streamlit Cloud, AWS, etc.). Video summarization works fully in the **local version** but may be unavailable in the cloud deployment.

3. **Domain Mismatch** — The ML model was trained on Twitter data (Sentiment140), so accuracy on YouTube comments may vary.

4. **Sarcasm and Negation** — Complex sentence structures and sarcasm may be difficult for the model.

5. **API Quotas** — YouTube Data API has a daily quota limit (10,000 units/day on free tier).

---

## 🔮 Future Work

- **Multilingual Support** — Full Urdu, Hindi, and Sindhi sentiment analysis
- **Transformer Models** — BERT / RoBERTa for higher accuracy
- **Emotion Detection** — Joy, anger, sadness, fear, surprise
- **Q&A Feature** — Ask questions about the video content
- **Quiz Generator** — Auto-generate quizzes for students
- **PDF Notes** — Download structured notes
- **Mobile App** — React Native version
- **Video Comparison** — Compare multiple videos on the same topic

---

## 👥 Team

**Team Name:** Digital Minds  
**Event:** OpenHack 2026  
**Category:** EdTech

| Role | Member |
|------|--------|
| **Faculty Lead / ML Engineer** | Muqaddas Imtiaz — Final Year BS Data Science, QUEST University Nawabshah |
| **Team Member** | Sonia Kumari — 25SW, 2nd Year, MUET SZAB Campus |
| **Team Member** | Khadija Mahar — 25SW, 2nd Year, MUET SZAB Campus |

---

## 🤖 AI & Open-Source Disclosure

### AI Tools Used
- **Google Gemini API** (gemini-1.5-flash) — Video summarization
- **ChatGPT / Claude** — Development assistance and debugging

### Open-Source Technologies
- **Streamlit** — Web app framework
- **Plotly** — Interactive charts
- **scikit-learn** — ML model (TF-IDF + Logistic Regression)
- **pytube** — YouTube transcript fetching
- **deep-translator** — Urdu translation
- **langdetect** — Language detection
- **FastAPI** — Backend API framework

### Dataset
- **Sentiment140** (Kaggle) — 1.6 million labeled tweets

---

## 📄 License

This project is licensed under the **MIT License**.

---

<p align="center">
  <strong>Built with ❤️ by Team Digital Minds</strong>
  <br>
  <em>OpenHack 2026 — Build. Solve. Demonstrate.</em>
</p>
```

---

