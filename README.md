🚀 Career Portal – Student Placement
Career Portal – Student Placement is a web-based student career development and placement preparation platform. It helps students organize their profiles, build skills, practice problem-solving, track internships, showcase projects, and prepare for recruitment through learning resources and AI-powered guidance.

The goal is to bring important career preparation activities together in one place and help students move from academic learning towards becoming career-ready.
✨ Features
👤 Student Account & Profile
- Student registration, login, and logout.
- Personal profile and account settings.
- Individual student records and progress.
🎯 Career Development
- Add, update, and manage technical skills.
- Track Data Structures and Algorithms (DSA) practice.
- Store certificates and achievements.
- Track internship applications and their status.
- Build a portfolio from student skills, projects, certificates, and evidence.
📚 Learning & Career Preparation
- Personalized learning profile and career roadmap.
- Learning Academy with structured learning tracks and lessons.
- Practice activities and progress analytics.
- Project Studio to record projects, repository links, contributions, and milestones.
- Opportunity Hub to save internships, scholarships, hackathons, competitions, and events.
- Mentor request workflow.
🤖 AI Learning Companion
- Supports learning, concept explanations, error explanations, practice, and project guidance.
- Can use the Google Gemini API when an API key is configured.
- Provides an offline fallback when Gemini is not configured or unavailable.
🧪 Recruitment Intelligence Lab
- Interactive recruitment preparation and simulation.
- Practice activities covering aptitude, programming, technical, case-study, and HR-style rounds.
- Review session results after submission.
🛠️ Technology Stack
Layer	Technology
Frontend	HTML5, CSS3, JavaScript
Backend	Python, Flask
Database	SQLite
Templates	Jinja2
AI integration	Google Gemini API (optional)
Version control	Git and GitHub


📁 Project Structure
CAREER-PORTAL-STUDENT-PLACEMENT/
├── app.py                       # Main Flask application
├── careerverse_features.py      # Career development and learning features
├── lesson_resources.py          # Learning lesson resources
├── personalize.py               # Personalized roadmap support
├── topic_resources.py           # Topic-based learning resources
├── requirements.txt             # Python dependencies
├── templates/                   # HTML/Jinja2 pages
├── static/                      # CSS, JavaScript, and images
├── image/                       # Project screenshots and images
└── README.md                    # Project documentation
🚀 Getting Started
1️⃣ Requirements
- Python 3.10 or later recommended
- pip
- Visual Studio Code or another Python IDE
2️⃣ Download the Project
Clone the repository:
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd <PROJECT-FOLDER>
Alternatively, download the repository as a ZIP file and extract it.
3️⃣ Create and Activate a Virtual Environment
Windows PowerShell:
py -m venv .venv
.\.venv\Scripts\Activate.ps1
If PowerShell blocks activation, use Command Prompt:
.venv\Scripts\activate.bat
macOS / Linux:
python3 -m venv .venv
source .venv/bin/activate
4️⃣ Install Dependencies
python -m pip install -r requirements.txt
5️⃣ Configure Environment Variables
Create a file named .env in the project root. Add your own values:
SECRET_KEY=replace_with_a_long_random_secret
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.8-flash
GEMINI_API_KEY is optional. Without it, AI-powered responses use the application's offline fallback where available. Keep your .env file private and never commit API keys or secret values to GitHub.
6️⃣ Run the Application
python app.py
Open the following address in your browser:
http://127.0.0.1:5000
Register a student account or log in to start using the portal.
🗄️ Database
The application uses SQLite. On a fresh setup, the application initializes its database as configured by the project. Do not upload a database containing real student accounts or personal information to a public repository. Each developer should use their own local database and keep database files out of Git.
🔐 Security Notes
- Never publish .env, API keys, passwords, or private student data.
- Use a strong, unique SECRET_KEY for local or deployed environments.
- The included configuration is intended for development. Review authentication, session security, CSRF protection, input validation, HTTPS, backups, and privacy controls before deploying publicly.
- AI-generated guidance can contain mistakes; verify important information independently.
🔮 Future Scope
- Employer and institution dashboards.
- Verified internship and job listings.
- Expanded learning tracks and assessments.
- More advanced placement analytics.
- Additional interview practice and mock recruitment workflows.
- Production deployment with stronger security and scalability.
💡 Project Purpose
Career Portal – Student Placement aims to provide students with a centralized platform to manage career-related activities, strengthen technical skills, document achievements, and prepare more effectively for internship and placement opportunities.
📌 Project: Career Portal – Student Placement
🏷️ Category: Student Career Development and Placement Preparation
⚙️ Backend: Python Flask
🗃️ Database: SQLite
