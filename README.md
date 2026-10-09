# 🧠 Digital Minds — YouTube Sentiment Analysis

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.5-F7931E?logo=scikit-learn&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-F7DF1E?logo=javascript&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Hackathon](https://img.shields.io/badge/Hackathon-2026-purple)

> **AI-powered YouTube comment sentiment analyzer** — Paste any YouTube URL and get instant **Positive / Neutral / Negative** breakdown with interactive charts.

Built with ❤️ by **Team Digital Minds** for **Hackathon 2026**

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Demo](#-demo)
- [Tech Stack](#-tech-stack)
- [How It Works](#-how-it-works)
- [ML Model Details](#-ml-model-details)
- [Dataset](#-dataset)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Endpoints](#-api-endpoints)
- [Limitations](#-limitations)
- [Future Improvements](#-future-improvements)
- [Team](#-team)
- [License](#-license)

---

## 🎯 Overview

**Digital Minds** is a full-stack Machine Learning application that analyzes the sentiment of YouTube video comments in real time.

Users paste a YouTube video URL, and the system:
1. Fetches comments via the **YouTube Data API v3**
2. Cleans and preprocesses the text
3. Runs a trained **Logistic Regression** model
4. Classifies each comment as **Positive**, **Neutral**, or **Negative**
5. Displays results as summary cards and an interactive doughnut chart

---

## ✨ Features

- 🎥 **YouTube URL input** — Works with `youtube.com/watch`, `youtu.be`, and `shorts` URLs
- 📡 **Live comment fetching** — Up to 100 top-level comments per video
- 🧹 **Text preprocessing** — URL, mention, hashtag, punctuation, and number removal
- 🤖 **ML classification** — TF-IDF + Logistic Regression (81.17% accuracy)
- 🎚️ **Smart Neutral detection** — Probability threshold (40%–60%) for Neutral class
- 📊 **Interactive charts** — Powered by Chart.js
- 🌗 **Dark / Light theme** — Toggle with a single click
- 💬 **Chatbot-style UI** — Modern, intuitive interface
- 🧭 **Sidebar categories** — About, How It Works, Tech Stack, ML Model, Dataset, Team

---

## 🎬 Demo

> Add a screenshot or GIF here after deployment.

```
https://digital-minds-youtube-sentiment.onrender.com
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | HTML5, CSS3, Vanilla JavaScript, Chart.js |
| **Backend** | Python 3.11, FastAPI, Uvicorn |
| **ML / NLP** | Scikit-learn, Joblib, TF-IDF, Logistic Regression |
| **Data Source** | YouTube Data API v3 (Google Cloud) |
| **Development** | VS Code, Kaggle Notebooks |
| **Version Control** | Git, GitHub |

---

## ⚙️ How It Works

```
┌─────────────┐    ┌──────────────┐    ┌─────────────────┐
│   User      │───▶│   Frontend   │───▶│    Backend      │
│ (YouTube    │    │  (HTML/CSS/  │    │   (FastAPI)     │
│   URL)      │    │      JS)     │    │                 │
└─────────────┘    └──────────────┘    └────────┬────────┘
                                                 │
                                                 ▼
                                       ┌──────────────────┐
                                       │  YouTube Data    │
                                       │  API v3          │
                                       └────────┬─────────┘
                                                 │
                                                 ▼
                                       ┌──────────────────┐
                                       │ Text Cleaning &  │
                                       │  TF-IDF          │
                                       └────────┬─────────┘
                                                 │
                                                 ▼
                                       ┌──────────────────┐
                                       │ Logistic         │
                                       │ Regression       │
                                       │ (Positive /      │
                                       │  Neutral /       │
                                       │  Negative)       │
                                       └────────┬─────────┘
                                                 │
                                                 ▼
                                       ┌──────────────────┐
                                       │  Charts + Stats  │
                                       └──────────────────┘
```

---

## 🤖 ML Model Details

| Metric | Value |
|--------|-------|
| **Algorithm** | Logistic Regression |
| **Vectorizer** | TF-IDF (50,000 features, ngram_range=(1,2)) |
| **Training Samples** | 396,883 |
| **Test Samples** | 99,221 |
| **Accuracy** | **81.17%** |
| **Precision (macro)** | 0.8118 |
| **Recall (macro)** | 0.8117 |
| **F1-Score (macro)** | 0.8117 |

**Models compared:**
- ✅ **Logistic Regression** — 81.17% (selected)
- Multinomial Naive Bayes — 79.63%
- Linear SVC — 80.44%

**Why Logistic Regression?**
Highest accuracy, fast training, and interpretable coefficients.

---

## 📊 Dataset

- **Source:** [Sentiment140](https://www.kaggle.com/code/muqaddasimtiaz/hackathon-project) (Kaggle)
- **Original size:** 1.6 million labeled tweets
- **Used in training:** 497,152 balanced samples (248,576 Positive + 248,576 Negative)
- **Labels:** `0 = Negative`, `4 = Positive` (mapped to `0` and `1`)
- **Preprocessing:** Lowercasing, URL removal, mention removal, punctuation removal, number removal

**⚠️ Limitation:** Sentiment140 has **no Neutral class**. We use a **probability threshold (40%–60%)** at prediction time to detect Neutral comments.

---

## 📁 Project Structure

```
digital-minds-hackathon/
│
├── backend/                    # FastAPI backend
│   ├── .env                    # API keys (gitignored)
│   ├── .env.example            # Template
│   ├── main.py                 # FastAPI app + endpoints
│   ├── sentiment.py            # Model loading + prediction
│   ├── youtube_api.py          # YouTube Data API integration
│   └── requirements.txt        # Python dependencies
│
├── frontend/                   # HTML/CSS/JS frontend
│   ├── index.html              # Chatbot UI
│   ├── style.css               # Dark/Light theme
│   └── script.js               # Frontend logic + charts
│
├── models/                     # Trained ML artifacts
│   ├── sentiment_pipeline.joblib
│   ├── label_mapping.json
│   └── model_info.json
│
├── notebook/                   # Kaggle notebook (optional)
│   └── hackathon-project.ipynb
│
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🚀 Installation

### Prerequisites

- Python 3.11+
- YouTube Data API v3 key
- Git

### Steps

**1. Clone the repository**

```bash
git clone https://github.com/Muqadas-g/digital-minds-hackathon.git
cd digital-minds-hackathon
```

**2. Create a virtual environment**

```bash
python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate  # macOS/Linux
```

**3. Install dependencies**

```bash
cd backend
pip install -r requirements.txt
```

**4. Get a YouTube API Key**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable **YouTube Data API v3**
4. Create an **API Key** under Credentials
5. Copy the key

**5. Configure environment variables**

Create `backend/.env`:

```env
YOUTUBE_API_KEY=your_youtube_api_key_here
```

---

## ▶️ Usage

### Run Backend

```bash
cd backend
python main.py
```

Backend runs at `http://localhost:8000`

### Run Frontend

Open a new terminal:

```bash
cd frontend
python -m http.server 5500
```

Open `http://localhost:5500` in your browser.

### Test It

1. Paste any YouTube video URL
2. Click **Send**
3. View sentiment breakdown + chart

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Health check |
| `POST` | `/api/analyze` | Analyze a YouTube video |

**POST `/api/analyze` — Request**

```json
{
  "video_url": "https://youtu.be/RmagWIWOM4w",
  "max_comments": 100
}
```

**Response**

```json
{
  "video_id": "RmagWIWOM4w",
  "video_title": "KR CVS FOOD CHALLENGE | RED FOOD ONLY",
  "total_comments_available": 19827,
  "comments_analyzed": 100,
  "counts": { "Positive": 72, "Neutral": 18, "Negative": 10 },
  "percentages": { "Positive": 72.0, "Neutral": 18.0, "Negative": 10.0 }
}
```

---

## ⚠️ Limitations

- **No Neutral class in training data** — Handled via probability threshold
- **Domain mismatch** — Model trained on Twitter data, not YouTube comments
- **Sarcasm & negation** — Difficult cases (e.g., "not bad at all")
- **API quota** — YouTube Data API has a daily limit (10,000 units)
- **Language** — Optimized for English comments only

---

## 🚀 Future Improvements

- 🔤 **Multilingual support** — Add Urdu, Hindi, Spanish
- 🧠 **Transformer models** — BERT / RoBERTa for better accuracy
- 💬 **Reply analysis** — Include nested comments
- 📈 **Trend analysis** — Sentiment over time
- 🎯 **Emoji analysis** — Sentiment from emojis
- 🔐 **User authentication** — Save analysis history
- 📱 **Mobile app** — React Native / Flutter

---

## 👥 Team

**Team Digital Minds** — Hackathon 2026

| Role | Responsibility |
|------|---------------|
| 🧑‍💻 **ML / NLP Engineer** | Dataset, model training, evaluation, deployment |
| 🎨 **Frontend Developer** | UI/UX design, chatbot interface |
| 🔌 **Backend Developer** | FastAPI, YouTube API integration |
| 🎤 **Presenter** | Demo, slides, judges' Q&A |

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Sentiment140](https://www.kaggle.com/datasets/kazanova/sentiment140) — Kaggle dataset
- [Scikit-learn](https://scikit-learn.org/) — ML library
- [FastAPI](https://fastapi.tiangolo.com/) — Backend framework
- [Chart.js](https://www.chartjs.org/) — Interactive charts
- [YouTube Data API v3](https://developers.google.com/youtube/v3) — Comment source

---

<p align="center">
  <strong>⭐ If you found this project useful, please give it a star! ⭐</strong>
  <br><br>
  Made with ❤️ by <strong>Team Digital Minds</strong>
</p>
