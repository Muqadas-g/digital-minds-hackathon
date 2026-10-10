// ============================================
// Digital Minds — Chatbot Logic (Dark + Light)
// ============================================

const API_URL = "http://localhost:8000/api/analyze";

const chat = document.getElementById("chat");
const input = document.getElementById("videoUrl");
const sendBtn = document.getElementById("sendBtn");
const sidebar = document.getElementById("sidebar");
const overlay = document.getElementById("overlay");
const menuBtn = document.getElementById("menuBtn");
const clearBtn = document.getElementById("clearBtn");
const themeBtn = document.getElementById("themeBtn");
const themeIcon = document.getElementById("themeIcon");

let chartInstance = null;

// ============================================
// THEME TOGGLE
// ============================================
const SUN_ICON = `
    <circle cx="12" cy="12" r="5"/>
    <line x1="12" y1="1" x2="12" y2="3"/>
    <line x1="12" y1="21" x2="12" y2="23"/>
    <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
    <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
    <line x1="1" y1="12" x2="3" y2="12"/>
    <line x1="21" y1="12" x2="23" y2="12"/>
    <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
    <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
`;

const MOON_ICON = `
    <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
`;

function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    themeIcon.innerHTML = theme === "dark" ? SUN_ICON : MOON_ICON;
    localStorage.setItem("dm-theme", theme);
    if (chartInstance) refreshChartTheme();
}

function toggleTheme() {
    const current = document.documentElement.getAttribute("data-theme");
    applyTheme(current === "dark" ? "light" : "dark");
}

const savedTheme = localStorage.getItem("dm-theme") || "dark";
applyTheme(savedTheme);

themeBtn.addEventListener("click", toggleTheme);

// ============================================
// EVENT LISTENERS
// ============================================
sendBtn.addEventListener("click", handleSend);
input.addEventListener("keypress", (e) => {
    if (e.key === "Enter") handleSend();
});

menuBtn.addEventListener("click", () => {
    sidebar.classList.add("open");
    overlay.classList.remove("hidden");
});

overlay.addEventListener("click", () => {
    sidebar.classList.remove("open");
    overlay.classList.add("hidden");
});

clearBtn.addEventListener("click", clearChat);

document.querySelectorAll(".cat-item").forEach(btn => {
    btn.addEventListener("click", () => {
        document.querySelectorAll(".cat-item").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        showCategoryInfo(btn.dataset.cat);
    });
});

// ============================================
// SEND HANDLER
// ============================================
async function handleSend() {
    const url = input.value.trim();

    if (!url) {
        input.parentElement.style.animation = "shake 0.4s";
        setTimeout(() => input.parentElement.style.animation = "", 400);
        return;
    }

    addUserMessage(url);
    input.value = "";
    sendBtn.disabled = true;

    const typingId = addTypingIndicator();

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ video_url: url, max_comments: 100 })
        });

        const data = await response.json();
        removeTypingIndicator(typingId);

        if (!response.ok) throw new Error(data.detail || "Something went wrong.");

        addBotResult(data);
    } catch (err) {
        removeTypingIndicator(typingId);
        addBotError(err.message || "Failed to analyze. Is the backend running?");
    } finally {
        sendBtn.disabled = false;
        input.focus();
    }
}

// ============================================
// MESSAGE BUILDERS
// ============================================
const BOT_AVATAR_SVG = `
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
        <path d="M12 2L4 6V12C4 16.5 7.5 20.5 12 22C16.5 20.5 20 16.5 20 12V6L12 2Z"
              stroke="white" stroke-width="2" stroke-linejoin="round"/>
    </svg>
`;

function addUserMessage(text) {
    const div = document.createElement("div");
    div.className = "msg msg-user";
    div.innerHTML = `
        <div class="avatar">👤</div>
        <div class="bubble">${escapeHtml(text)}</div>
    `;
    chat.appendChild(div);
    scrollBottom();
}

function addTypingIndicator() {
    const id = "typing-" + Date.now();
    const div = document.createElement("div");
    div.className = "msg msg-bot";
    div.id = id;
    div.innerHTML = `
        <div class="avatar bot-avatar">${BOT_AVATAR_SVG}</div>
        <div class="bubble">
            <div class="typing">
                <span></span><span></span><span></span>
            </div>
        </div>
    `;
    chat.appendChild(div);
    scrollBottom();
    return id;
}

function removeTypingIndicator(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

// ============================================
// MAIN RESULT RENDERER (with new features)
// ============================================
function addBotResult(data) {
    const div = document.createElement("div");
    div.className = "msg msg-bot";
    const chartId = "chart-" + Date.now();

    let langHtml = "";
    for (const [lang, count] of Object.entries(data.languages || {})) {
        const pct = ((count / data.comments_analyzed) * 100).toFixed(1);
        langHtml += `<span class="hint">🌐 ${lang}: ${count} (${pct}%)</span>`;
    }

    function wordsHtml(words) {
        if (!words || words.length === 0) return '<span class="hint">No data</span>';
        return words.map(w => `<span class="hint">${w.word} (${w.count})</span>`).join("");
    }

    let likedHtml = "";
    (data.top_liked_comments || []).forEach((c, i) => {
        const emoji = c.label === "Positive" ? "😊" : c.label === "Negative" ? "😞" : "😐";
        likedHtml += `
            <div class="liked-item">
                <span class="liked-rank">#${i + 1}</span>
                <span class="liked-likes">👍 ${c.likes.toLocaleString()}</span>
                <span class="liked-emoji">${emoji}</span>
                <div class="liked-text">${highlightKeywords(escapeHtml(c.text), c.keywords)}</div>
            </div>
        `;
    });

    function samplesHtml(samples, emoji) {
        if (!samples || samples.length === 0) return "";
        return samples.map(s => `
            <div class="sample-item">
                <span class="sample-emoji">${emoji}</span>
                <div class="sample-text">${highlightKeywords(escapeHtml(s.text), s.keywords)}</div>
            </div>
        `).join("");
    }

    let timelineHtml = "";
    if (data.timeline && data.timeline.length > 0) {
        timelineHtml = data.timeline.map(t => `
            <div class="timeline-row">
                <span class="timeline-date">${t.date}</span>
                <div class="timeline-bar">
                    <div class="timeline-pos" style="width:${(t.Positive / t.total) * 100}%"></div>
                    <div class="timeline-neu" style="width:${(t.Neutral / t.total) * 100}%"></div>
                    <div class="timeline-neg" style="width:${(t.Negative / t.total) * 100}%"></div>
                </div>
                <span class="timeline-count">${t.total}</span>
            </div>
        `).join("");
    }

    div.innerHTML = `
        <div class="avatar bot-avatar">${BOT_AVATAR_SVG}</div>
        <div class="bubble">
            <p>✅ <strong>Analysis complete!</strong></p>
            <p><strong>Video:</strong> ${escapeHtml(data.video_title)}</p>
            <p><strong>Analyzed:</strong> ${data.comments_analyzed} comments (out of ${data.total_comments_available} available)</p>
            <p><strong>Video Stats:</strong> 👁️ ${(data.video_stats?.views || 0).toLocaleString()} views · 👍 ${(data.video_stats?.likes || 0).toLocaleString()} likes</p>

            <div class="result-cards">
                <div class="result-card positive">
                    <div class="rc-icon">😊</div>
                    <div class="rc-label">Positive</div>
                    <div class="rc-value">${data.percentages.Positive}%</div>
                    <div class="rc-count">${data.counts.Positive} comments</div>
                </div>
                <div class="result-card neutral">
                    <div class="rc-icon">😐</div>
                    <div class="rc-label">Neutral</div>
                    <div class="rc-value">${data.percentages.Neutral}%</div>
                    <div class="rc-count">${data.counts.Neutral} comments</div>
                </div>
                <div class="result-card negative">
                    <div class="rc-icon">😞</div>
                    <div class="rc-label">Negative</div>
                    <div class="rc-value">${data.percentages.Negative}%</div>
                    <div class="rc-count">${data.counts.Negative} comments</div>
                </div>
            </div>

            <div class="chat-chart">
                <canvas id="${chartId}"></canvas>
            </div>

            ${timelineHtml ? `
                <p style="margin-top: 20px;"><strong>📅 Sentiment Timeline:</strong></p>
                <div class="timeline-container">${timelineHtml}</div>
            ` : ""}

            ${likedHtml ? `
                <p style="margin-top: 20px;"><strong>🔥 Top Liked Comments:</strong></p>
                <div class="liked-container">${likedHtml}</div>
            ` : ""}

            <p style="margin-top: 20px;"><strong>💬 Sample Comments:</strong></p>
            <div class="samples-container">
                ${samplesHtml(data.sample_comments?.positive, "😊")}
                ${samplesHtml(data.sample_comments?.neutral, "😐")}
                ${samplesHtml(data.sample_comments?.negative, "😞")}
            </div>

            <p style="margin-top: 20px;"><strong>🌐 Languages Detected:</strong></p>
            <div class="quick-hints">${langHtml}</div>

            <p style="margin-top: 16px;"><strong>😊 Top Positive Words:</strong></p>
            <div class="quick-hints">${wordsHtml(data.top_positive_words)}</div>

            <p style="margin-top: 12px;"><strong>😞 Top Negative Words:</strong></p>
            <div class="quick-hints">${wordsHtml(data.top_negative_words)}</div>

            <p style="margin-top: 12px;"><strong>😐 Top Neutral Words:</strong></p>
            <div class="quick-hints">${wordsHtml(data.top_neutral_words)}</div>
        </div>
    `;

    chat.appendChild(div);
    scrollBottom();
    setTimeout(() => renderChart(chartId, data), 100);
}

function highlightKeywords(text, keywords) {
    if (!keywords || keywords.length === 0) return text;
    let result = text;
    keywords.forEach(kw => {
        const regex = new RegExp(`\\b${kw}\\b`, 'gi');
        result = result.replace(regex, `<mark class="kw-highlight">$&</mark>`);
    });
    return result;
}

function addBotError(msg) {
    const div = document.createElement("div");
    div.className = "msg msg-bot";
    div.innerHTML = `
        <div class="avatar bot-avatar">${BOT_AVATAR_SVG}</div>
        <div class="bubble" style="border: 1px solid rgba(239,68,68,0.4); background: rgba(239,68,68,0.08); padding: 14px 18px; border-radius: 12px;">
            <p>⚠️ <strong>Error:</strong> ${escapeHtml(msg)}</p>
            <p style="font-size: 13px; opacity: 0.8;">Please check the URL and make sure the backend is running.</p>
        </div>
    `;
    chat.appendChild(div);
    scrollBottom();
}

// ============================================
// CHART
// ============================================
function getChartTextColor() {
    const theme = document.documentElement.getAttribute("data-theme");
    return theme === "dark" ? "#cbd5e1" : "#52525b";
}

function getChartBorderColor() {
    const theme = document.documentElement.getAttribute("data-theme");
    return theme === "dark" ? "rgba(0,0,0,0.3)" : "rgba(255,255,255,0.8)";
}

function renderChart(canvasId, data) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (chartInstance) chartInstance.destroy();

    chartInstance = new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: ["Positive", "Neutral", "Negative"],
            datasets: [{
                data: [
                    data.percentages.Positive,
                    data.percentages.Neutral,
                    data.percentages.Negative
                ],
                backgroundColor: ["#10b981", "#f59e0b", "#ef4444"],
                borderColor: getChartBorderColor(),
                borderWidth: 3,
                hoverOffset: 10
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: "65%",
            plugins: {
                legend: {
                    position: "bottom",
                    labels: {
                        color: getChartTextColor(),
                        font: { size: 12, family: "Inter", weight: "500" },
                        padding: 16,
                        usePointStyle: true,
                        pointStyle: "circle"
                    }
                },
                tooltip: {
                    backgroundColor: "rgba(15,15,20,0.95)",
                    titleColor: "#f1f5f9",
                    bodyColor: "#cbd5e1",
                    borderColor: "rgba(139,92,246,0.5)",
                    borderWidth: 1,
                    padding: 10,
                    cornerRadius: 8
                }
            },
            animation: { animateScale: true, animateRotate: true, duration: 900 }
        }
    });
}

function refreshChartTheme() {
    if (!chartInstance) return;
    chartInstance.options.plugins.legend.labels.color = getChartTextColor();
    chartInstance.data.datasets[0].borderColor = getChartBorderColor();
    chartInstance.update();
}

// ============================================
// SIDEBAR CATEGORIES
// ============================================
function showCategoryInfo(cat) {
    const info = {
        about: {
            icon: "ℹ️",
            title: "About Digital Minds",
            body: `
                <p><strong>Digital Minds</strong> is a Machine Learning & NLP project that analyzes the sentiment of YouTube comments.</p>
                <p>Users paste a YouTube video URL, and our system:</p>
                <p>1️⃣ Fetches comments via the YouTube Data API<br>
                   2️⃣ Cleans & preprocesses the text<br>
                   3️⃣ Runs a trained ML model<br>
                   4️⃣ Classifies each comment as Positive, Neutral, or Negative<br>
                   5️⃣ Displays results with charts and stats</p>
                <p>🎯 <strong>Goal:</strong> Give content creators and viewers a quick pulse-check of audience sentiment.</p>
            `
        },
        how: {
            icon: "⚙️",
            title: "How It Works",
            body: `
                <p><strong>Step-by-step pipeline:</strong></p>
                <p>🔗 <strong>1. Input</strong> — User provides a YouTube video URL</p>
                <p>📡 <strong>2. Fetch</strong> — YouTube Data API v3 fetches up to 100 top-level comments</p>
                <p>🧹 <strong>3. Clean</strong> — Lowercasing, removing URLs, mentions, punctuation, numbers</p>
                <p>🔢 <strong>4. Vectorize</strong> — TF-IDF converts text into numerical features (50K features, 1-2 grams)</p>
                <p>🤖 <strong>5. Predict</strong> — Logistic Regression classifies each comment</p>
                <p>🎚️ <strong>6. Neutral detection</strong> — If confidence is 40%–60%, comment is labeled Neutral</p>
                <p>📊 <strong>7. Display</strong> — Results shown as cards and a doughnut chart</p>
            `
        },
        tech: {
            icon: "🛠️",
            title: "Tech Stack",
            body: `
                <p><strong>Frontend</strong> — HTML5, CSS3 (Glassmorphism), Vanilla JavaScript, Chart.js</p>
                <p><strong>Backend</strong> — Python, FastAPI, Uvicorn</p>
                <p><strong>ML / NLP</strong> — Scikit-learn, Joblib, TF-IDF, Logistic Regression</p>
                <p><strong>Data source</strong> — YouTube Data API v3 (Google Cloud)</p>
                <p><strong>Development</strong> — VS Code, Kaggle Notebooks</p>
                <p><strong>Version control</strong> — Git, GitHub</p>
            `
        },
        model: {
            icon: "🤖",
            title: "ML Model Details",
            body: `
                <p><strong>Algorithm:</strong> Logistic Regression (baseline winner)</p>
                <p><strong>Vectorizer:</strong> TF-IDF with 50,000 features, ngram_range=(1,2)</p>
                <p><strong>Test Accuracy:</strong> 81.17%</p>
                <p><strong>Macro F1-Score:</strong> 0.8117</p>
                <p><strong>Training samples:</strong> 396,883</p>
                <p><strong>Test samples:</strong> 99,221</p>
                <p><strong>Models compared:</strong> Logistic Regression, Multinomial Naive Bayes, Linear SVC</p>
                <p><strong>Why Logistic Regression?</strong> Highest accuracy, fast training, interpretable coefficients.</p>
            `
        },
        dataset: {
            icon: "📊",
            title: "Dataset",
            body: `
                <p><strong>Source:</strong> Sentiment140 (Kaggle)</p>
                <p><strong>Original size:</strong> 1.6 million labeled tweets</p>
                <p><strong>Used in training:</strong> 497,152 balanced samples (248,576 Positive + 248,576 Negative)</p>
                <p><strong>Labels:</strong> 0 = Negative, 4 = Positive (mapped to 0/1)</p>
                <p><strong>Preprocessing:</strong> Lowercasing, URL removal, mention removal, punctuation removal, number removal</p>
                <p><strong>Limitation:</strong> Dataset has no Neutral class — we use a probability threshold (40%–60%) to detect Neutral comments at prediction time.</p>
            `
        },
        team: {
            icon: "👥",
            title: "Digital Minds Team",
            body: `
                <p><strong>Team:</strong> Digital Minds</p>
                <p><strong>Event:</strong> Hackathon 2026</p>
                <p><strong>Roles:</strong></p>
                <p>🧑‍💻 <strong>ML/NLP Engineer</strong> — Dataset, model training, evaluation, deployment</p>
                <p>🎨 <strong>Frontend Developer</strong> — UI/UX design, chatbot interface</p>
                <p>🔌 <strong>Backend Developer</strong> — FastAPI, YouTube API integration</p>
                <p>🎤 <strong>Presenter</strong> — Demo, slides, judges' Q&A</p>
                <p>🙏 Thank you for exploring our project!</p>
            `
        }
    };

    const data = info[cat];
    if (!data) return;

    const div = document.createElement("div");
    div.className = "msg msg-bot";
    div.innerHTML = `
        <div class="avatar bot-avatar">${BOT_AVATAR_SVG}</div>
        <div class="bubble">
            <p><strong>${data.icon} ${data.title}</strong></p>
            ${data.body}
        </div>
    `;
    chat.appendChild(div);
    scrollBottom();

    if (window.innerWidth <= 800) {
        sidebar.classList.remove("open");
        overlay.classList.add("hidden");
    }
}

// ============================================
// CLEAR CHAT
// ============================================
function clearChat() {
    if (!confirm("Clear the current chat?")) return;

    chartInstance = null;

    chat.innerHTML = `
        <div class="msg msg-bot">
            <div class="avatar bot-avatar">${BOT_AVATAR_SVG}</div>
            <div class="bubble">
                <p class="bubble-title">Welcome to Digital Minds 👋</p>
                <p>I'm an AI trained to analyze the sentiment of YouTube comments using Machine Learning & Natural Language Processing.</p>
                <p>Paste any YouTube video URL below and I'll break down the audience's mood into <strong>Positive</strong>, <strong>Neutral</strong>, and <strong>Negative</strong> categories.</p>
                <div class="quick-hints">
                    <span class="hint">📎 Paste a YouTube URL to begin</span>
                    <span class="hint">📊 Get instant sentiment charts</span>
                </div>
            </div>
        </div>
    `;

    document.querySelectorAll(".cat-item").forEach(b => b.classList.remove("active"));
    input.focus();
}

// ============================================
// HELPERS
// ============================================
function scrollBottom() {
    setTimeout(() => {
        chat.scrollTop = chat.scrollHeight;
    }, 50);
}

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}