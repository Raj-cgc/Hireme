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
            company="Backend & API Development Projects",
            role="Backend Engineer",
            duration="2023 — Present",
            description="Developed MediBuddy REST APIs (doctor appointment portal with role-based auth & medical history) and backend messaging services for WE CHAT with Firebase.",
            skills_used=["Spring Boot", "Node.js", "Express.js", "MongoDB", "MySQL", "C++", "Java", "Firebase"]
        )
    ],
    education=[
        "B.Tech. Computer Science & Engineering, Chandigarh Engineering College, CGC, Landran (Expected 2027, CGPA: 8.68/10)",
        "Senior Secondary (Class XII), Cambridge Sr. Sec. School, Buxar (2022, 97%)",
        "Secondary (Class X), St. Pauls School, Sasaram (2020, 88.6%)"
    ],
    projects=[
        "MediBuddy - Doctor Appointment Backend & APIs: Role-based doctor appointment portal for patient booking, doctor management, and admin workflow. Designed RESTful APIs for auth, appointment scheduling, and medical history.",
        "WE CHAT - Real time messaging service: Backend & real-time communication services with instant delivery, Firebase Authentication, and Cloud Firestore synchronization."
    ],
    certifications=[
        "HackerRank: Secured 5-star badge in Problem Solving and C++",
        "LeetCode: Solved 1000+ DSA problems with contest rating of 1800+",
        "NPTEL Certification (DBMS): Completed with Silver badge",
        "Infosys Springboard Certification: Certified Developer",
        "Smart India Hackathon (SIH 2025): SIH 2025 Participant"
    ]
)

import re
import difflib

def normalize_text(text: str) -> str:
    t = text.lower().strip()
    
    # Common tech & spacing aliases, typos, and phrasing normalizations
    aliases = {
        "springboot": "spring boot",
        "spring-boot": "spring boot",
        "spring": "spring boot",
        "nodejs": "node.js",
        "node": "node.js",
        "expressjs": "express.js",
        "express": "express.js",
        "reactjs": "react.js",
        "react": "react.js",
        "cpp": "c++",
        "cplusplus": "c++",
        "restapi": "rest api",
        "restapis": "rest apis",
        "wechat": "we chat",
        "fole": "role",
        "developper": "developer",
        "devloper": "developer",
        "enginner": "engineer",
        "suited": "fit",
        "suitable": "fit",
        "hiring": "hire",
        "qualify": "fit",
        "leetcode": "dsa",
        "hackerrank": "dsa",
        "gpa": "cgpa",
        "cgpa": "cgpa",
        "btech": "education",
        "college": "education",
        "university": "education",
    }
    
    cleaned = re.sub(r'[^\w\s\+\#\.-]', ' ', t)
    words = cleaned.split()
    replaced = [aliases.get(w, w) for w in words]
    normalized = " ".join(replaced)
    return normalized

def ask_candidate(question: str, resume: Resume):
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    use_groq = bool(api_key and not api_key.startswith("dummy"))
    
    if use_groq:
        system_prompt = f"""
You are {resume.name}, a Computer Science & Engineering student and Backend Engineer interviewing for software engineering roles.

Candidate Resume & Data:
{resume.model_dump_json(indent=2)}

Strict Guidelines:
1. Speak in the FIRST PERSON ("I", "my", "me").
2. Answer the user's question directly and concisely without repeating generic opening introductions like "I am Raj, a Backend Engineer..." unless asked to introduce yourself.
3. Handle typos and informal questions gracefully (e.g., "fole" -> "role", "springboot" -> "Spring Boot", "dsa" -> "Data Structures & Algorithms").
4. Be professional, confident, and enthusiastic about backend development, software architecture, REST APIs, databases, and problem-solving.
5. If asked about a technical topic or project, explain your experience clearly based on your resume stack (Spring Boot, Node.js, Express, C++, Java, MySQL, MongoDB, Firebase, MediBuddy, WE CHAT, 1000+ LeetCode problems).
6. If asked an out-of-scope question unrelated to a job interview or software engineering (e.g. weather, recipes), politely bring the focus back to your engineering qualifications and resume background.
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
        except Exception:
            # Fall through to robust rule engine if Groq call fails
            pass

    # High-Performance Offline Fallback Q&A Engine
    q_raw = question.strip()
    q_norm = normalize_text(question)
    words_set = set(re.findall(r'\b[\w\+\#\.-]+\b', q_norm))

    # 1. Job Role Fit / Suitability / Hiring Questions (Higher Priority)
    if any(w in words_set for w in ["fit", "role", "hire", "job", "position", "candidate", "developer", "engineer", "suitable", "qualify"]) or "why hire" in q_norm or "why should we hire" in q_norm:
        return (
            f"Yes, absolutely! As a CSE student specializing in Backend Engineering (CGPA 8.68), I am a strong fit for backend software engineering roles. "
            f"I have practical experience building RESTful APIs, database schemas, and real-time backend services using Spring Boot, Node.js, Express.js, C++, Java, MySQL, MongoDB, and Firebase. "
            f"I've built systems like MediBuddy (doctor appointment booking APIs) and WE CHAT (messaging backend), and solved over 1,000 DSA problems on LeetCode (1800+ rating) to ensure optimal backend performance."
        )

    # 2. Greetings & Introductions
    if any(w in words_set for w in ["hi", "hello", "hey", "intro", "introduce", "summary"]) or "who are you" in q_norm or "about yourself" in q_norm:
        return (
            f"Hello! I'm {resume.name}, a CSE student and Backend Engineer specializing in building scalable RESTful microservices, "
            f"backend APIs, and database architecture with Spring Boot, Node.js, Express, Java, C++, MySQL, and MongoDB. "
            f"I have solved 1,000+ DSA problems on LeetCode (1800+ rating) and built projects like MediBuddy (doctor appointment APIs) and WE CHAT (real-time chat backend). "
            f"What would you like to know about my skills, projects, or experience?"
        )

    # 3. Specific Tech Skill Enquiries
    tech_knowledge_map = {
        "spring boot": "Java & Spring Boot are central to my backend tech stack! I use Spring Boot to build structured RESTful microservices, dependency injection modules, and database-backed services.",
        "java": "I code extensively in Java for enterprise backend services and Spring Boot applications, leveraging Object-Oriented Programming (OOP) principles and robust design patterns.",
        "c++": "C++ is my primary language for competitive programming and core Data Structures & Algorithms. I've solved 1,000+ DSA problems using C++ and hold a 5-Star Problem Solving badge on HackerRank.",
        "node.js": "I use Node.js and Express.js to build asynchronous, fast REST APIs and backend services, including user auth, data validation, and database connectors.",
        "express.js": "Express.js is one of my core tools for designing RESTful API endpoints, middleware pipelines, authentication checks, and backend controllers.",
        "mysql": "I have strong experience in relational database design using MySQL, writing optimized SQL queries, database normalization, schema indexing, and ACID transactions for backend applications.",
        "mongodb": "I use MongoDB with Mongoose/Node.js for document-based NoSQL storage, implementing flexible JSON schemas for features like medical records in MediBuddy.",
        "database": "I have experience with both relational (MySQL) and NoSQL (MongoDB, Firebase Cloud Firestore) databases, focusing on schema design, query optimization, and REST API integration.",
        "firebase": "I used Firebase Authentication and Cloud Firestore real-time database synchronization to build the WE CHAT messaging backend.",
        "react.js": "I have experience with React.js for frontend integration, building responsive user interfaces that consume backend REST APIs.",
        "flutter": "I built the WE CHAT mobile messaging app using Flutter and Dart, integrating instant message delivery and cloud sync.",
        "rest api": "REST API design is one of my primary strengths. I design clean RESTful endpoints using standard HTTP methods, JSON serialization, input validation, and role-based JWT authentication."
    }

    for key, answer_text in tech_knowledge_map.items():
        if key in q_norm or key.replace(" ", "") in q_norm.replace(" ", ""):
            return f"Yes! {answer_text} My technical stack also includes {', '.join(resume.skills)}."

    # 4. General Tech Stack / Skills Query
    if any(w in words_set for w in ["skill", "skills", "stack", "tech", "technology", "technologies", "language", "languages", "framework", "frameworks", "tool", "tools"]):
        return (
            f"My technical stack includes:\n"
            f"• Languages: C++, Java, JavaScript, Dart, HTML/CSS\n"
            f"• Backend & Frameworks: Spring Boot, Node.js, Express.js, RESTful APIs\n"
            f"• Databases & Cloud: MySQL, MongoDB, Firebase Cloud Firestore\n"
            f"• Core CS: Data Structures & Algorithms (1000+ LeetCode), Low Level Design (LLD), OOP, Operating Systems, DBMS"
        )

    # 5. DSA / Competitive Programming / LeetCode / HackerRank
    if any(w in words_set for w in ["dsa", "leetcode", "hackerrank", "rating", "contest", "codeforces", "algo", "algorithm", "algorithms"]) or "problem solving" in q_norm:
        return (
            f"I actively practice Data Structures & Algorithms (DSA) to write clean, time and space-optimized code:\n"
            f"• LeetCode: Solved 1,000+ problems with an active contest rating of 1800+\n"
            f"• HackerRank: 5-Star Badge in Problem Solving & C++\n"
            f"• Core Focus: Arrays, Trees, Graphs, Dynamic Programming, System Design & LLD"
        )

    # 6. Specific Projects (MediBuddy / WE CHAT)
    if "medibuddy" in q_norm or ("doctor" in q_norm and "appointment" in q_norm):
        return (
            f"MediBuddy is a role-based doctor appointment portal and medical API service I developed. "
            f"Key backend highlights:\n"
            f"• Designed RESTful APIs for patient appointment booking, doctor management, and admin workflows.\n"
            f"• Implemented authentication, medical history records, and database operations with Node.js, Express, MongoDB, and React."
        )

    if "we chat" in q_norm or "wechat" in q_norm or ("chat" in q_norm and "app" in q_norm):
        return (
            f"WE CHAT is a real-time messaging application I built using Flutter, Dart, and Firebase. "
            f"Key backend highlights:\n"
            f"• Real-time message delivery and device synchronization using Firebase Cloud Firestore.\n"
            f"• Firebase Authentication for secure user sign-in and user chat session management."
        )

    if any(w in words_set for w in ["project", "projects", "built", "build", "system", "systems", "app", "apps", "application"]):
        proj_str = "\n".join([f"{i+1}. {p}" for i, p in enumerate(resume.projects)])
        return f"Here are the key projects I've built:\n{proj_str}"

    # 7. Education / CGPA / College
    if any(w in words_set for w in ["education", "cgpa", "gpa", "college", "degree", "school", "university", "btech", "marks", "percentage", "study"]):
        edu_str = "\n".join([f"• {e}" for e in resume.education])
        return f"Here is my educational record:\n{edu_str}"

    # 8. Certifications & Achievements
    if any(w in words_set for w in ["certification", "certifications", "certif", "achievement", "achievements", "award", "badge", "nptel", "infosys", "sih", "hackathon"]):
        cert_str = "\n".join([f"• {c}" for c in resume.certifications])
        return f"Here are my certifications & achievements:\n{cert_str}"

    # 9. Experience & Work History
    if any(w in words_set for w in ["exp", "experience", "work", "background", "history", "intern", "company", "years"]):
        exp_details = [f"• {e.role} at {e.company} ({e.duration}): {e.description}" for e in resume.experiences]
        exp_str = "\n".join(exp_details)
        return f"I have around {resume.total_experience_years or 2.0} years of practical software development experience:\n{exp_str}"

    # 10. Contact / Social Links
    if any(w in words_set for w in ["contact", "email", "phone", "reach", "mail", "number", "call", "linkedin", "github"]):
        return (
            f"You can reach me directly via:\n"
            f"• Email: {resume.email}\n"
            f"• Phone: {resume.phone}\n"
            f"• GitHub: https://github.com/Raj-cgc\n"
            f"• LinkedIn: https://linkedin.com/in/Raj."
        )

    # 11. Technical Deep-Dive / Situational Questions
    if any(kw in q_norm for kw in ["design api", "api design", "sql vs nosql", "indexing", "authentication", "jwt", "solid"]):
        return (
            f"In my software design, I apply SOLID OOP principles and clean API patterns. "
            f"For REST APIs, I enforce structured routing, HTTP standard status codes, JWT authentication, and schema validation. "
            f"For databases, I choose MySQL when ACID compliance and relational links are required, and MongoDB/Firestore when rapid JSON document indexing and real-time synchronization are needed."
        )

    # 12. Smart Fallback for any other software/candidate inquiry
    return (
        f"As a Backend Engineer & CSE student (CGPA 8.68), I specialize in C++, Java, Spring Boot, Node.js, Express, REST APIs, MySQL, MongoDB, and DSA (1000+ LeetCode problems). "
        f"I've built systems like MediBuddy and WE CHAT. Feel free to ask about any specific project, skill, education, or technical topic!"
    )


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