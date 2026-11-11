# CAREERVERSE – Recruitment Intelligence Lab (MVP)

Integrated into the uploaded Flask + SQLite Student Career Placement Portal.

## Run locally

1. Extract this ZIP.
2. Open the `Student Career Placement Portal` folder in VS Code.
3. Create/activate a virtual environment (optional but recommended).
4. Install dependencies: `pip install -r requirements.txt`
5. Set a strong secret key before deployment. For local testing, the existing development fallback remains; do not deploy it.
6. Run: `python app.py`
7. Log in to CareerPortal and choose **Recruitment Lab** in the dashboard sidebar, or visit `/recruitment-lab`.

## Included functionality

- Authenticated student access; attempts are scoped to the logged-in user.
- Start/resume an entry-level AI/ML Engineer simulation.
- Six ordered rounds: aptitude (10), Python challenge (20), ML fundamentals (20), technical interview (20), ML case study (20), HR (10).
- SQLite persistence for attempts and round submissions.
- Objective question scoring with explanations.
- Transparent preliminary keyword/depth rubrics for written responses.
- Python code submission storage and transparent structural rubric; arbitrary code is NOT executed on the web server.
- Cumulative score and final report.

## Architecture

Browser (Jinja templates + vanilla JS) → Flask routes/JSON API → SQLite.
Existing `users.id` is the owner key. `recruitment_attempts` stores each simulation; `recruitment_rounds` stores per-round scores, responses and feedback. The existing app authentication session is reused.

## API

- `GET /recruitment-lab`
- `POST /api/recruitment/start`
- `GET /recruitment-lab/session/<attempt_id>`
- `POST /api/recruitment/submit` JSON: `{ "attempt_id": 1, "round_no": 1, "answers": {"0": "2"} }`
- `GET /api/recruitment/result/<attempt_id>`

## Important evaluation limitations

This is a working academic MVP, not an employer-certified assessment. The written-answer evaluator uses a transparent keyword-coverage and answer-length heuristic. The Python round uses a visible code-structure rubric and does not execute arbitrary submitted code. Replace these with human-reviewed rubrics and an isolated sandboxed code runner before using this for real candidate selection. The current AI/ML questions are authored sample questions, not proprietary company questions. No actual AI model/API is called in this MVP.

## Suggested production hardening

- Set a random `SECRET_KEY` in environment; remove development fallback.
- Add CSRF protection, secure cookie settings, login throttling and audit logs.
- Add attempt time limits, server-side stage-order enforcement, question randomization and retake policy.
- Add a sandboxed execution service (container isolation, CPU/memory/time/network limits) for code judging; never use `exec()` on user code inside Flask.
- Add versioned question banks and human-reviewed scoring rubrics.
- For AI feedback, integrate a provider server-side with API keys in environment variables, structured output validation, prompt-injection controls, privacy notice and human review. AI feedback must not make final hiring decisions.
