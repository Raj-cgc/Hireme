import json
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
from pydantic import BaseModel
from pypdf import PdfReader

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY") or "dummy_key"
client = Groq(api_key=groq_api_key)

model = "llama-3.3-70b-versatile"
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# parse resume schemas
class Experience(BaseModel):
    company: str | None = None
    role: str | None = None
    duration: str | None = None
    description: str | None = None
    skills_used: list[str] = []

class Resume(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    total_experience_years: float | None = None
    skills: list[str] = []
    experiences: list[Experience] = []
    education: list[str] = []
    projects: list[str] = []
    certifications: list[str] = []

resume_schema = Resume.model_json_schema()

class ChatRequest(BaseModel):
    question: str

DEFAULT_RESUME = Resume(
    name="Raj",
    email="rajkumarbxr78@gmail.com",
    phone="+91-7004155718",
    total_experience_years=2.0,
    skills=[
        "C++", "Java", "HTML", "CSS", "JavaScript",
        "Spring Boot", "React.js", "Node.js", "Express.js", "Flutter",
        "MySQL", "MongoDB", "Firebase", "OOP", "DSA", "Low Level Design",
        "Operating Systems", "DBMS"
    ],
    experiences=[
        Experience(
            company="Full Stack & App Development Projects",
            role="Full Stack & Mobile App Developer",
            duration="2023 — Present",
            description="Developed MediBuddy (MERN Stack Doctor Appointment App with REST APIs) and WE CHAT (Flutter real-time messaging app with Firebase Auth & Cloud Firestore).",
            skills_used=["React.js", "Node.js", "Express.js", "MongoDB", "Flutter", "Firebase", "Java", "C++"]
        )
    ],
    education=[
        "B.Tech. Computer Science & Engineering, Chandigarh Engineering College, CGC, Landran (Expected 2027, CGPA: 8.68/10)",
        "Senior Secondary (Class XII), Cambridge Sr. Sec. School, Buxar (2022, 97%)",
        "Secondary (Class X), St. Pauls School, Sasaram (2020, 88.6%)"
    ],
    projects=[
        "MediBuddy - Doctor Appointment App (MERN Stack): Role-based doctor appointment portal for patient booking, doctor management, and admin workflow. Designed RESTful APIs for auth, appointment scheduling, and medical history.",
        "WE CHAT - Real time chat app (Flutter & Dart): Real-time messaging application with instant delivery, smooth UI, Firebase Authentication, and Cloud Firestore synchronization."
    ],
    certifications=[
        "HackerRank: Secured 5-star badge in Problem Solving and C++",
        "LeetCode: Solved 1000+ DSA problems with contest rating of 1800+",
        "NPTEL Certification (DBMS): Completed with Silver badge",
        "Infosys Springboard Certification: Certified HTML, CSS, JavaScript Developer",
        "Smart India Hackathon (SIH 2025): SIH 2025 Participant"
    ]
)

def ask_candidate(question: str, resume: Resume):
    if not os.getenv("GROQ_API_KEY"):
        q_lower = question.lower()
        if "skill" in q_lower or "stack" in q_lower or "technology" in q_lower or "language" in q_lower:
            return f"My technical skills include: {', '.join(resume.skills)}. I build applications using React.js, Node.js, Spring Boot, and Flutter."
        elif "project" in q_lower or "medibuddy" in q_lower or "we chat" in q_lower or "chat" in q_lower:
            return f"My main projects are:\n1. MediBuddy: Doctor Appointment App built with MERN stack featuring role-based workflows and RESTful APIs.\n2. WE CHAT: Real-time messaging app built with Flutter, Dart, and Firebase."
        elif "education" in q_lower or "cgpa" in q_lower or "college" in q_lower or "degree" in q_lower or "school" in q_lower:
            return f"I am pursuing B.Tech in CSE from Chandigarh Engineering College (CGC Landran) with a CGPA of 8.68/10. In Class XII, I scored 97%."
        elif "certification" in q_lower or "leetcode" in q_lower or "hackerrank" in q_lower or "rating" in q_lower:
            return f"I have solved 1000+ DSA problems on LeetCode with an 1800+ contest rating, hold a 5-Star HackerRank badge in Problem Solving & C++, and an NPTEL Silver badge in DBMS."
        elif "contact" in q_lower or "email" in q_lower or "phone" in q_lower:
            return f"You can contact me via email at {resume.email} or by phone at {resume.phone}."
        else:
            return f"Hello! I am Raj's AI assistant. I am a CSE student specializing in Full Stack and App Development. Feel free to ask about my skills, projects (MediBuddy, WE CHAT), education, or competitive programming background!"

    system_prompt = f"""
You are an AI assistant representing a job candidate.

Below is everything you know about the candidate.

{resume.model_dump_json(indent=2)}

Rules:
1. Answer only using this information.
2. Never hallucinate.
3. If information is unavailable, say "I don't have enough information to answer that."
4. Be professional.
5. Answer as if HR is interviewing this candidate.
"""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error communicating with AI model: {str(e)}. Please check your GROQ_API_KEY."

def parse_resume(resume_text):
    if not os.getenv("GROQ_API_KEY"):
        return DEFAULT_RESUME

    system_prompt = f"""
    You are an expert resume parser.
    Extract information from the resume into valid JSON matching this schema:
    {resume_schema}
    """
    user_prompt = f"Parse the following resume:\n{resume_text}"
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
        )
        raw_output = response.choices[0].message.content
        data = json.loads(raw_output)
        return Resume(**data)
    except Exception:
        return DEFAULT_RESUME

def read_pdf(file_path: Path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

cached_resume: Resume | None = None

def get_resume() -> Resume:
    global cached_resume
    if cached_resume is None:
        try:
            file_path = Path("Raj_2336991.pdf")
            if not file_path.exists():
                file_path = Path("my_resume.pdf")
            if not file_path.exists():
                pdf_files = list(Path(".").glob("*.pdf"))
                if pdf_files:
                    file_path = pdf_files[0]
                else:
                    file_path = None
            
            if file_path and file_path.exists():
                resume_text = read_pdf(file_path)
                cached_resume = parse_resume(resume_text)
            else:
                cached_resume = DEFAULT_RESUME
        except Exception:
            cached_resume = DEFAULT_RESUME
    return cached_resume

@app.get("/")
def home():
    return {
        "message": "HireMeAI Backend API is running for Raj's resume."
    }

@app.get("/profile")
def profile():
    resume = get_resume()
    return resume.model_dump()

@app.post("/chat")
def chat(request: ChatRequest):
    resume = get_resume()
    answer = ask_candidate(request.question, resume)
    return {
        "answer": answer
    }