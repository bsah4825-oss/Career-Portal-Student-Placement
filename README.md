<div align="center">
  <img src="static/careerverse/careerverse-logo.svg" alt="CAREERVERSE" width="360">
  <h1>CAREERVERSE</h1>
  <p><strong>Learn with purpose. Build real skills. Shape your career.</strong></p>
  <p>A student-focused career and learning platform built with Flask.</p>
  <p>
    <img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white" alt="Python 3.11+">
    <img src="https://img.shields.io/badge/Flask-3.1-black?logo=flask&logoColor=white" alt="Flask 3.1">
    <img src="https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white" alt="SQLite">
    <img src="https://img.shields.io/badge/AI-Gemini%20optional-8E75B2?logo=googlegemini&logoColor=white" alt="Optional Gemini integration">
  </p>
</div>

---

## 🧭 Contents

- [✨ What is CAREERVERSE?](#-what-is-careerverse)
- [🚀 What you can do](#-what-you-can-do)
- [🛠️ Built with](#️-built-with)
- [⚡ Get started](#-get-started)
- [🗺️ Explore the app](#️-explore-the-app)
- [📁 Project structure](#-project-structure)
- [🔐 Data, AI and limitations](#-data-ai-and-limitations)
- [📚 More documentation](#-more-documentation)

## ✨ What is CAREERVERSE?

CAREERVERSE brings career planning and skill-building into one place. Students can explore learning paths, practice new skills, build projects, track evidence of their work, and prepare for career opportunities.

The app combines a student career portal with the CAREERVERSE learning platform and the **Recruitment Intelligence Lab**, an educational interview-practice simulation.

## 🚀 What you can do

| Area | Highlights |
|---|---|
| 👤 **Your account** | Register, sign in, manage your profile and update your password. |
| 📌 **Career tracker** | Keep track of skills, DSA practice, certificates and internship applications. |
| 🧭 **Personal learning path** | Complete onboarding and a baseline diagnostic, then explore a career roadmap. |
| 🎓 **Learning academy** | Follow guided lessons and use curated learning resources across multiple fields. |
| 🧪 **Practice and projects** | Try quizzes, plan projects, track milestones and record skill evidence. |
| 📈 **Progress and portfolio** | Review learning activity and bring projects, skills and evidence together. |
| 🌱 **Career support** | Explore career roles, save opportunities and submit mentor requests. |
| 🤖 **AI learning companion** | Optionally use Gemini-powered tutoring and personalization, with offline fallbacks. |
| 💼 **Recruitment practice** | Try a multi-round AI/ML recruitment simulation and review your results. |

## 🛠️ Built with

- **Backend:** Python, Flask and Werkzeug
- **Database:** SQLite
- **Frontend:** Jinja, HTML, CSS and JavaScript
- **AI integration:** Google Gemini API (optional)

## ⚡ Get started

### Prerequisites

- Python **3.11 or later**
- PowerShell on Windows (or an equivalent terminal)

### 1. Create a virtual environment

From the project directory, run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use the virtual environment's Python directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

### 2. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 3. Add local configuration

Create a `.env` file in the project root:

```dotenv
SECRET_KEY=replace-with-a-long-random-secret
GEMINI_API_KEY=
GEMINI_MODEL=gemini-3.8-flash
FLASK_DEBUG=1
COOKIE_SECURE=0
```

`GEMINI_API_KEY` is optional. Leave it empty to use the available curated and offline fallback experience. To enable Gemini features, add your own API key. **Never share or commit your key or `.env` file.**

`FLASK_DEBUG=1` and `COOKIE_SECURE=0` are local-development settings only. For a public deployment, configure a strong secret key, HTTPS, secure cookies and other production protections.

### 4. Run CAREERVERSE

```powershell
python app.py
```

Open **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in your browser and create an account. The application initializes its SQLite database and required tables at startup.

## 🗺️ Explore the app

| Destination | Route |
|---|---|
| 🏠 Home | `/` |
| 📝 Register / sign in | `/register` · `/login` |
| 🌟 CAREERVERSE home | `/careerverse/` |
| 🎓 Learning academy | `/careerverse/academy` |
| 🧭 Career roadmap | `/careerverse/roadmap` |
| 📚 Learning resources | `/careerverse/resources` |
| 🧱 Project studio | `/careerverse/projects` |
| 🧪 Practice arena | `/careerverse/practice` |
| 📊 Progress analytics | `/careerverse/analytics` |
| 🤖 AI tutor | `/careerverse/tutor` |
| 🪪 Portfolio | `/careerverse/portfolio` |
| 💼 Recruitment Intelligence Lab | `/recruitment-lab` |

Most learning and student-profile pages require you to sign in.

## 📁 Project structure

```text
CAREERVERSE/
├── app.py                   # Flask app, account portal and recruitment lab
├── careerverse_features.py  # CAREERVERSE routes and feature logic
├── personalize.py           # Optional Gemini integration and personalization
├── lesson_resources.py      # Learning-track resources
├── topic_resources.py       # Curated topic resources
├── templates/               # Jinja page templates
├── static/                  # CSS, JavaScript, images and logos
├── requirements.txt         # Python dependencies
└── database.db              # Local data; excluded from Git
```

## 🔐 Data, AI and limitations

- **Your local data:** Account and learning activity are stored in SQLite. The local database is excluded from Git to help prevent publishing personal records.
- **Optional AI:** Gemini-generated roadmaps and tutoring responses may be inaccurate. Review important information, and do not enter secrets or sensitive personal information into prompts.
- **Learning guidance:** Diagnostic results and career suggestions are starting points, not validated measures of ability, job readiness or employment outcomes.
- **Recruitment simulation:** The Recruitment Intelligence Lab is an educational MVP, not an employer-certified assessment. Written-answer and code scoring are preliminary; submitted code is not executed by the server.
- **Before going live:** Review authentication and privacy, enable CSRF protection and rate limiting, configure secure sessions and HTTPS, and plan database backups and migrations.

## 📚 More documentation

- [CAREERVERSE feature guide](README_CAREERVERSE.md)
- [Recruitment Intelligence Lab guide](RECRUITMENT_LAB_README.md)
- [Changelog](CHANGELOG_V1.2.md)
