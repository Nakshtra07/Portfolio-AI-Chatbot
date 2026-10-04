# Portfolio AI Chatbot 🤖📄

> **An AI-powered, recruiter-first candidate portfolio portal.**
> Built with **FastAPI**, **Groq LLM**, **PyPDF**, and an **Editorial Brutalism** design aesthetic.

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Groq](https://img.shields.io/badge/Groq-Cloud%20AI-orange?style=flat-square)](https://groq.com)
[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

---

## 📌 How It Works

Traditional developer portfolios are filled with static skill bars, generic icons, and lengthy text walls that recruiters rarely read in full.

**Portfolio AI Chatbot** flips that experience on its head:
1. **Recruiter Intelligence Portal**: Displays only verified candidate credentials (Name, Title, and Direct Actions) up top. No fake skill percentages or cluttered cards.
2. **Instant PDF Parsing**: PyPDF and FastAPI parse `backend/resume.pdf` to construct a structured Pydantic `Resume` dossier containing education, experience, technical proficiencies, and contact details.
3. **Conversational Recruiter AI**: An embedded dark terminal chatbot powered by **Groq** lets hiring managers, engineering leads, and HR interrogate the candidate's actual background in real time.
4. **Job Description (JD) Fit Matching**: Recruiters can paste an entire job description to ask: *"Is Nakshatra a good match for this role?"*. The AI evaluates strengths, overlap, experience gaps, and culture fit instantly.
5. **Direct Actions**:
   - **Connect via Email**: Auto-extracts the candidate's email from the PDF and opens Gmail compose with `To:` pre-filled.
   - **View Resume [PDF] ↗**: Directly downloads or previews `backend/resume.pdf` in the browser at `/resume.pdf`.

---

## 🎯 Key Features

- **⚡ Editorial Brutalism Design**: Crisp architectural layout inspired by high-end design broadsheets, featuring Inter 900 typography, Space Mono technical accents, zero-radius borders, and subtle SVG radar sweep animation.
- **🌓 Light / Dark Mode Toggle**: Smooth theme switching between daytime editorial stone (`#EBEBEB`) and dark room terminal mode (`#0D0D0D`).
- **💬 Real-Time Streaming & Animations**:
  - Live character typewriter effect for AI answers.
  - Pulsing orange 3-dot loading state while the model evaluates the candidate dossier.
  - Interactive quick-prompt chips for one-click querying.
- **🛠️ Recruiter Utilities**:
  - One-click **Copy response** button for each message bubble.
  - **Clear Chat (`[ESC]`)** keyboard shortcut.
  - **Auto-expanding textarea** with `[Enter]` to send and `[Shift + Enter]` for new lines.
- **📱 Fully Responsive**: Flawless layout adaptation across desktop, tablet, and mobile displays.

---

## 🚀 Getting Started

Follow the steps below to set up, activate, and run the project using a standard Python Virtual Environment (`venv`).

### 1. Prerequisites
- Python **3.11+** installed on your system.
- A **Groq API Key** (Free tier available at [console.groq.com](https://console.groq.com/keys)).
- Git installed.

---

### 2. Clone the Repository

```bash
git clone https://github.com/Nakshtra07/Portfolio-AI-Chatbot.git
cd Portfolio-AI-Chatbot
```

---

### 3. Set Up & Activate Virtual Environment (`venv`)

#### On Windows (PowerShell):
```powershell
# Create the virtual environment named .venv
python -m venv .venv

# Activate the virtual environment
.venv\Scripts\Activate.ps1
```

> **Note for Windows:** If you encounter an execution policy error running `Activate.ps1`, run:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

#### On Windows (Command Prompt `cmd`):
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

#### On macOS / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

*(Once activated, your terminal prompt will be prefixed with `(.venv)`).*

---

### 4. Install Dependencies

You can install the required packages using `pip`:

```bash
pip install -r requirements.txt
```

*(Alternatively, if you use [uv](https://github.com/astral-sh/uv), you can simply run `uv sync`).*

---

### 5. Configure Environment Variables

Create a `.env` file in the root directory (you can copy the provided template):

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

Open `.env` and add your Groq API Key:
```env
GROQ_API_KEY=gsk_your_actual_groq_api_key_here
```

---

### 6. Add Your Resume

Place your own resume PDF into the `backend/` directory named `resume.pdf`:
```
backend/
└── resume.pdf
```
*(The system will automatically read your name, title, email, and experience from this PDF).*

---

### 7. Run the Application

Start the unified server from the `frontend/` directory:

```bash
cd frontend
python serve.py
```

Now open your web browser and navigate to:
```
http://localhost:8000
```
*(or `http://127.0.0.1:8000`)*

---

## 🏗️ Architecture & Project Structure

```
Portfolio-AI-Chatbot/
├── .env.example         # Template for environment variables (GROQ_API_KEY)
├── .gitignore            # Excludes .venv, .env, __pycache__, and build artifacts
├── pyproject.toml        # Modern Python package metadata and dependencies
├── requirements.txt      # Pip-compatible package dependencies
├── README.md             # Project documentation and guides
├── frontend/
│   ├── index.html        # Single-page Editorial Brutalism portfolio + AI chat UI
│   └── serve.py          # Unified FastAPI server (serves UI, resume PDF & mounts API)
└── backend/
    ├── main.py           # Core FastAPI application with PDF parser & Groq agent
    └── resume.pdf        # Candidate resume parsed at runtime
```

---

## 📡 API Endpoints

The unified server runs at `http://localhost:8000` and exposes the following endpoints:

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Serves the single-page portfolio & AI chat interface (`frontend/index.html`) |
| `GET` | `/resume.pdf` | Streams and serves `backend/resume.pdf` for in-browser view or download |
| `GET` | `/resume-info` | Returns cached JSON with candidate `{ name, email, title, resume_url }` |
| `POST` | `/chat` | Accepts `{ "question": "..." }` and returns `{ "answer": "..." }` via Groq LLM |

---

## 💡 Example Recruiter Prompts

Try asking the chatbot:
- *"What are Nakshatra's strongest technical skills?"*
- *"Summarize Nakshatra's experience and degree background."*
- *"We are looking for a Full-Stack AI Engineer with FastAPI and React experience. How does this candidate match?"*
- *"Paste a Job Description: [paste JD here] — Is Nakshatra a fit for this role?"*

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
