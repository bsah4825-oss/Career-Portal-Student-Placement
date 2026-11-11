# CAREERVERSE v1.2 — Gemini roadmap, resources and brand update

## Added
- Gemini-powered personalised learning path generation from the student's saved profile, target career role and latest diagnostic category scores.
- A curated fallback roadmap when Gemini is not configured, unavailable, rate-limited or returns invalid output.
- Saved roadmap versions in the student's own SQLite account.
- Weekly plan sections covering learning focus, practice, proof-of-skill deliverables and a job-readiness checklist.
- Curated learning resources by field: official documentation, free video courses, articles, guided curricula and safe practice labs.
- More discipline coverage: arts/humanities/social sciences, health/life sciences, design/creative industries and general professional pathways, in addition to technology, business and engineering.
- Dedicated `/careerverse/resources` page.
- CAREERVERSE SVG and PNG logo assets, favicon mark and light logo for Recruitment Lab pages.
- Expanded navigation linking the Academy, Project Studio, Skill Evidence, AI Tutor, Opportunities, Mentors, Analytics, Portfolio and Recruitment Lab.
- `.env` loading for local Gemini configuration.
- Updated the default Gemini model to `gemini-3.8-flash`, the current stable Flash model listed in Google’s model documentation at build time.

## Improved
- Roadmap uses canonical role mapping for free-text interests such as AI/ML Engineer, Data Science, design, health and humanities.
- Recruitment Lab pages now display CAREERVERSE branding and a return link.
- Diagnosis continues to use independent radio groups for each question.

## Verification performed
- Python syntax compilation for `app.py` and `careerverse_features.py`.
- Jinja compilation of all 31 HTML templates.
- Isolated SQLite route harness verified fallback roadmap generation, persistence, page rendering, curated resources and recruitment navigation.
- Mocked Gemini client verified the Gemini response parsing and provider path without making an external API call.

## Not verified in this build environment
- A full live Flask server start: Flask and google-genai were not installed in the isolated build environment and package installation could not reach the package index.
- A real Gemini API request: requires the user's own API key, network access and available quota.

## Important boundaries
- Gemini roadmaps are learning guidance, not guaranteed employment outcomes.
- Curated resources may change availability or terms; check providers directly. Some optional certificates/exams/features may cost money.
- Recruitment Lab remains an educational simulation. Its written/code scoring is preliminary; submitted code is not executed by the server.
- A production release still needs CSRF protection, rate limiting, migrations, deployment security review, role-specific assessment design, a sandbox service and independent skill verification.
