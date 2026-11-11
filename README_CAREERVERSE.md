# CAREERVERSE v1.2 — Student Transformation Platform

CAREERVERSE extends the existing Student Career Placement Portal and Recruitment Intelligence Lab. It is a Flask + SQLite modular application. It keeps the existing `users` table and the existing profile, skills, DSA, certificates, internships, settings and recruitment simulation features.

## Included in this build

### Student transformation journey
- Universal onboarding for students across degrees and disciplines.
- Student learning profile: degree, branch/subject, year, graduation year, interests, available time, language preference, experience level and device/internet access.
- Short baseline diagnostic with category-level feedback. Results are provisional and not a permanent ability label.
- Suggested roadmap with six stages: discover, foundations, practice, projects, evidence and career preparation.

### Free Learning Academy
- Web Development Foundations (HTML/CSS beginner track).
- Python Programming from Zero (beginner track).
- Digital & Professional Foundations (cross-discipline track).
- Data Analytics Foundations.
- Cybersecurity Foundations.
- Business & Professional Analytics.
- Core Engineering & Applied Problem Solving.
- Each lesson includes explanation, example, practice and a required learner reflection.
- Learning completion is stored separately from demonstrated skill evidence.

### Practice, projects and evidence
- Project Studio with problem statement, target track, repository/demo links, personal contribution reflection and five tracked build milestones.
- Practice Arena with a mixed foundation quiz, explanations and saved attempt history.
- Career Analytics showing lesson, project, milestone, practice and evidence activity separately.
- Skill Evidence records with evidence type, URL, explanation and transparent `self-reported` status.
- Portfolio page combines project work, existing skills, certificates and evidence.

### Career support
- Career role profiles for software, frontend, data, AI/ML, cybersecurity, business analysis, core engineering, arts/humanities, health/life sciences, design/creative fields and general professional pathways.
- Skill-gap starting checklist compared with names in the student's existing Skills tracker and evidence records. This is not a validated job-readiness score.
- Opportunity Hub for saving internships, scholarships, hackathons, competitions and events. It is a personal tracker, not a live job feed.
- Mentor Connect request form. Requests are stored; no mentor is automatically assigned in this MVP.
- Existing Recruitment Intelligence Lab remains available at `/recruitment-lab`.

### AI Learning Companion
- Modes for teaching, explaining errors, practice, knowledge checks and project guidance.
- If `GEMINI_API_KEY` is configured, the app attempts to use the Gemini API from the server.
- Without an API key or when the provider is unavailable, a deterministic offline fallback keeps the learning area usable.
- AI output may be wrong; students should verify it and demonstrate their own understanding.

## Run in VS Code (Windows PowerShell)

1. Extract this project folder.
2. Open the folder in VS Code.
3. Open Terminal → New Terminal.
4. Create a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use Command Prompt and run `.venv\Scripts\activate.bat`, or run `.venv\Scripts\python.exe` directly.

5. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

6. Create your local environment file:

   ```powershell
   Copy-Item .env.example .env
   ```

7. Open `.env` in VS Code. Add a long random `SECRET_KEY`. To enable Gemini-powered features, add your Gemini API key to `GEMINI_API_KEY`. Keep the key private and never commit `.env`. The default model is `gemini-3.8-flash`; you can change `GEMINI_MODEL` if Google updates model availability.

8. Start the app:

   ```powershell
   python app.py
   ```

9. Open `http://127.0.0.1:5000` and sign in or register. Choose **CAREERVERSE** from the dashboard sidebar, or open `http://127.0.0.1:5000/careerverse/`.

The downloadable ZIP intentionally excludes `database.db` so it does not distribute existing student records. For an upgrade, copy your own backed-up `database.db` into the project root after extracting; your existing accounts and records will then be used and new CAREERVERSE tables are added automatically. For a fresh installation, the app creates a new database when it starts.

## Main routes

- `/careerverse/` — student transformation home
- `/careerverse/onboarding` — student learning profile
- `/careerverse/diagnosis` — starting assessment
- `/careerverse/roadmap` — Gemini-personalised (or curated fallback) weekly learning path and role-specific resources
- `/careerverse/resources` — curated free learning library
- `/careerverse/academy` — learning tracks
- `/careerverse/projects` — project studio and milestones
- `/careerverse/practice` — practice arena
- `/careerverse/analytics` — student progress analytics
- `/careerverse/evidence` — skill evidence
- `/careerverse/tutor` — AI learning companion
- `/careerverse/careers` — career role and skills explorer
- `/careerverse/portfolio` — student portfolio
- `/careerverse/mentors` — mentor request workflow
- `/careerverse/opportunities` — saved opportunity tracker
- `/recruitment-lab` — existing recruitment simulation

## Gemini personalised roadmap and learning resources

- The roadmap uses the saved learning profile, target role and latest diagnostic category scores. It does not send student name, email, registration number or password to Gemini.
- Gemini generates a practical 12-week plan with weekly learning focus, practice and proof-of-skill tasks, plus a job-preparation checklist.
- If `GEMINI_API_KEY` is missing, the provider is unavailable, quota is exceeded or the response is invalid, CAREERVERSE saves a role-specific curated fallback plan instead. Learning never depends on the API being online.
- The student can change the target role and regenerate the roadmap. Each generated version is saved to the student's account.
- The resource library contains official documentation, free courses, videos and safe practice labs. Some providers may charge for optional certificates, exams or advanced features; check each provider's terms.
- Gemini output is guidance, not a guarantee or a validated hiring assessment. Students should verify important facts and demonstrate skills through their own work.

## CAREERVERSE identity

- `static/careerverse/careerverse-logo.svg` — full wordmark for the CAREERVERSE navigation.
- `static/careerverse/careerverse-logo-light.svg` — light wordmark used on dark Recruitment Lab headers.
- `static/careerverse/careerverse-mark.svg` — compact favicon / app mark.
- PNG exports are included for use in reports and presentations.

## Important limitations / production work still required

This is a working MVP foundation, not a finished production platform with every proposed ecosystem feature. It does not yet include a live mentor marketplace, institution/employer dashboards, a verified live opportunity feed, comprehensive courses for every degree and discipline, a full adaptive question bank, peer community, independent assessor workflows, role-specific recruitment simulations, or a secure code-execution sandbox. The current recruitment scoring remains preliminary and must not be treated as employer-certified hiring assessment. Do not execute arbitrary student code inside the Flask process.

Before public deployment: set a strong secret key, use HTTPS, add CSRF protection and rate limits, review authentication/session security, validate URLs, configure secure cookies, add backups and migrations, add tests and accessibility checks, use PostgreSQL for multi-user production scale, and obtain appropriate privacy/security review. Do not expose diagnostic responses, tutor chats or private student activity to colleges/employers without explicit consent and role-based controls.

## Data and fairness principles

- Core lessons, exercises, roadmaps and portfolio functions are free in this build.
- A diagnostic score is a starting estimate, not a permanent label.
- Lesson completion is not equivalent to skill proficiency.
- Evidence is labelled self-reported until an actual review occurs.
- Career recommendations are guidance, not employment guarantees.
- AI tutoring is optional; fallback learning remains available.
