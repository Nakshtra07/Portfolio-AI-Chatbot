from fastapi import FastAPI
from pathlib import Path
from pypdf import PdfReader
import os
from typing import Optional, List
import json
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
app = FastAPI()

def read_pdf(file_path: Path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text() or ""
        if page_text:
            text += page_text + "\n"
    return text

class Experience(BaseModel):
    company: Optional[str] = None
    position: Optional[str] = None
    duration: Optional[str] = None
    responsibilities: Optional[List[str]] = None
    skills_used: Optional[List[str]] = None


# ---------------------------------------------------------
# Resume Model
# ---------------------------------------------------------

class Resume(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: Optional[List[str]] = None
    education: Optional[List[str]] = None
    certifications: Optional[List[str]] = None
    projects: Optional[List[str]] = None
    experiences: Optional[List[Experience]] = None
    total_experience_years: Optional[float] = None

resume_schema = Resume.model_json_schema()

class ChatRequest(BaseModel):
    question: str
def ask_candidate(question: str, resume: Resume):

    system_prompt = f"""
You are an AI assistant representing a job candidate.

Below is everything you know about the candidate.

{resume.model_dump_json(indent=2)}

Rules:

1. Answer only using this information.

2. Never hallucinate.

3. If information is unavailable,
say

"I don't have enough information to answer that."

4. Be professional.

5. Answer as if HR is interviewing this candidate.
"""

    response = client.chat.completions.create(

        model="openai/gpt-oss-120b",

        messages=[

            {
                "role":"system",
                "content":system_prompt
            },

            {
                "role":"user",
                "content":question
            }

        ]

    )

    return response.choices[0].message.content


#parsing resume
def parse_resume(resume_text):
    """
    Parse the extracted resume text into a Resume object.
    """
    
    # Generate the JSON schema for the Resume model.

    schema = Resume.model_json_schema()

    # User Prompt

    prompt = f"""
Parse the following resume.

Resume:

{resume_text}
"""

    # ---------------------------------------------------------
    # System Prompt
    # ---------------------------------------------------------

    system_prompt = f"""
You are an expert resume parser.

Different resumes use different headings.

Treat headings like:
- Experience
- Work History
- Employment
- Internship

as the same section.

Return ONLY valid JSON matching the following schema.
Do not return the schema itself.

Do not return unnecessary fields like "properties", "title", or "type".

Do not invent any information.

If some information is missing,
return null or an empty list.

Schema:

{schema}
"""

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    # Call the LLM.

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages,
        response_format={"type": "json_object"}
    )

    # ---------------------------------------------------------
    # Convert JSON string into a Python dictionary.
    # ---------------------------------------------------------

    answer = response.choices[0].message.content
    # print("========== RAW LLM RESPONSE ==========")
    # print(answer)
    # print("======================================")

    resume_dict = json.loads(answer)

    # ---------------------------------------------------------
    # Convert dictionary into a Resume object.
    # ---------------------------------------------------------

    resume = Resume(**resume_dict)

    return resume

@app.get("/")
def home():
    resume_text = read_pdf(Path("resume.pdf"))
    resume = parse_resume(resume_text)
    print(resume.model_dump_json(indent=2))
    return {
        "message": "resume parsed successfully",
    }

@app.post("/chat")
def chat(request: ChatRequest):
    resume_text = read_pdf(Path("resume.pdf"))
    resume = parse_resume(resume_text)
    answer = ask_candidate(request.question, resume)
    return {
        "answer": answer
    }