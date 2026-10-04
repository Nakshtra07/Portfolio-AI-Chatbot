"""
serve.py — unified dev server
──────────────────────────────────────────────────────────────────
Serves index.html for GET / and mounts the /chat route from the
backend FastAPI app at the same origin, so fetch('/chat') works
without any CORS issues.

Run from the frontend/ folder:
    python serve.py

Then open: http://localhost:8000
──────────────────────────────────────────────────────────────────
"""
import sys
import os
from dotenv import load_dotenv

# ── Paths ────────────────────────────────────────────────────────
# This file lives in frontend/; the project root is one level up.
FRONTEND_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(FRONTEND_DIR)
BACKEND_DIR  = os.path.join(PROJECT_ROOT, "backend")
INDEX_HTML   = os.path.join(FRONTEND_DIR, "index.html")

# Load .env from project root BEFORE changing CWD
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

# Add backend/ to sys.path so `import main` finds backend/main.py
sys.path.insert(0, BACKEND_DIR)

# Change CWD to backend/ so relative paths like "resume.pdf" resolve
os.chdir(BACKEND_DIR)

# Import the backend's FastAPI app (backend/main.py exports `app`)
import importlib
backend = importlib.import_module("main")   # backend/main.py

from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse

# ── Build the unified app ────────────────────────────────────────
app = FastAPI(title="HireMe AI — Portfolio + Chat")

# Cache so resume.pdf is only parsed once (LLM call is expensive)
_resume_info_cache: dict | None = None


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def serve_portfolio():
    """Serve the portfolio page instead of the backend's JSON response."""
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.get("/resume", include_in_schema=False)
@app.get("/resume.pdf", include_in_schema=False)
def serve_resume():
    """Serve the candidate's resume PDF directly for viewing or download."""
    resume_path = Path("resume.pdf")
    if resume_path.exists():
        return FileResponse(
            path=resume_path,
            filename="Nakshatra_Resume.pdf",
            media_type="application/pdf"
        )
    return HTMLResponse("Resume PDF not found.", status_code=404)


@app.get("/resume-info", include_in_schema=False)
def get_resume_info():
    """Return candidate name, email, title, and resume URL extracted from resume.pdf."""
    global _resume_info_cache
    if _resume_info_cache is not None:
        return _resume_info_cache
    try:
        resume_text = backend.read_pdf(Path("resume.pdf"))
        lines = [line.strip() for line in resume_text.splitlines() if line.strip()]
        resume = backend.parse_resume(resume_text)

        # Derive title: check header lines first, then experience position
        title = "AI Full-Stack Engineer"
        if len(lines) > 1 and "engineer" in lines[1].lower() or "developer" in lines[1].lower():
            title = lines[1]
        elif resume.experiences and resume.experiences[0].position:
            title = resume.experiences[0].position

        _resume_info_cache = {
            "name":  resume.name  or (lines[0] if lines else "Nakshatra Prajapati"),
            "email": resume.email or "nakshtraprajapati838@gmail.com",
            "title": title,
            "resume_url": "/resume.pdf",
        }
    except Exception as e:
        _resume_info_cache = {
            "name": "Nakshatra Prajapati",
            "email": "nakshtraprajapati838@gmail.com",
            "title": "AI Full-Stack Engineer",
            "resume_url": "/resume.pdf",
        }
    return _resume_info_cache


# Mount all backend routes except GET / (keep /chat, etc.)
for route in backend.app.routes:
    if hasattr(route, "path") and route.path == "/" and "GET" in getattr(route, "methods", set()):
        continue  # skip the JSON home endpoint
    app.routes.append(route)


# ── Entry point ──────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    # Pass the app object directly — avoids module-string resolution issues
    uvicorn.run(app, host="0.0.0.0", port=8000)
