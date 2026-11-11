"""Topic catalog used by the step-by-step roadmap.

A roadmap step (from Gemini or the curated fallback) is free text such as
"JavaScript fundamentals" or "SQL foundations". Each step is matched to one or more topics
below, and every topic carries English videos/playlists, articles, a mastery checklist and a
hands-on task. Videos are English by default; the personalisation layer only shows Hindi
videos to students who chose Hindi/Hinglish.

'q' entries are YouTube search links built from the exact title + channel (see lesson_resources.V).
"""
import re
from lesson_resources import V, A

TOPICS = {}


def T(tid, name, kw, videos, articles, mastery, handson, academy=()):
    TOPICS[tid] = {'id': tid, 'name': name, 'kw': kw, 'videos': videos, 'articles': articles,
                   'mastery': mastery, 'handson': handson, 'academy': list(academy)}


T('html-css', 'HTML, CSS & responsive pages', ['html', 'css', 'responsive', 'semantic', 'web foundation', 'webpage', 'web page', 'layout', 'forms'],
  [V('Learn HTML & CSS – Full Course for Beginners', 'freeCodeCamp.org', 'Build while you watch: the best single course to start web pages.', mode='Hands-on', vid='a_iQb1lnAEQ'),
   V('Web Development with HTML & CSS – Full Course for Beginners', 'freeCodeCamp.org', 'Project-based revision for layouts and responsive design.', mode='Hands-on', vid='dX8396ZmSPk')],
  [A('Structuring content with HTML', 'MDN Web Docs', 'https://developer.mozilla.org/en-US/docs/Learn/HTML', 'Official step-by-step module.'),
   A('CSS first steps', 'MDN Web Docs', 'https://developer.mozilla.org/en-US/docs/Learn/CSS/First_steps', 'Selectors, box model, colours and text.')],
  ['Build a semantic page from scratch.', 'Make a layout work at mobile and desktop widths.'],
  'Build and deploy a responsive one-page profile site on GitHub Pages.',
  [('web-foundations', 'html-structure'), ('web-foundations', 'css-basics'), ('web-foundations', 'responsive-project')])

T('javascript', 'JavaScript fundamentals', ['javascript', ' js ', 'dom', 'es6', 'events', 'interactive'],
  [V('JavaScript Programming – Full Course', 'freeCodeCamp.org', 'Complete beginner JavaScript course covering variables, functions, arrays, DOM.', q='JavaScript Programming Full Course freeCodeCamp.org'),
   V('JavaScript Tutorial for Beginners', 'Programming with Mosh', 'Short concept-focused introduction.', q='JavaScript Tutorial for Beginners Programming with Mosh 1 hour')],
  [A('JavaScript first steps', 'MDN Web Docs', 'https://developer.mozilla.org/en-US/docs/Learn/JavaScript/First_steps', 'Official beginner module with exercises.'),
   A('The Modern JavaScript Tutorial', 'javascript.info', 'https://javascript.info/', 'Deep, example-rich explanations.')],
  ['Write functions, arrays and loops without notes.', 'Change page content using the DOM and an event listener.'],
  'Build an expense calculator or quiz that updates the page when the user clicks.')

T('git-github', 'Git & GitHub', ['git', 'github', 'version control', 'branch', 'commit', 'pull request'],
  [V('Git and GitHub for Beginners – Crash Course', 'freeCodeCamp.org', 'Clear walkthrough of init, add, commit, branch, push and pull requests.', mode='Hands-on', q='Git and GitHub for Beginners Crash Course freeCodeCamp.org')],
  [A('Pro Git book', 'git-scm.com', 'https://git-scm.com/book/en/v2', 'Free official Git book; read chapters 1–3 first.'),
   A('Hello World (GitHub quickstart)', 'GitHub Docs', 'https://docs.github.com/en/get-started/start-your-journey/hello-world', 'Create a repo, branch and pull request in 10 minutes.')],
  ['Create a repo, commit, push and open a pull request.', 'Explain what a branch is and why it is used.'],
  'Put one of your projects on GitHub with a README and at least 5 meaningful commits.')

T('react', 'React & UI frameworks', ['react', 'component', 'state', 'routing', 'ui framework', 'frontend framework', 'jsx'],
  [V('React Course – Beginner’s Tutorial for React JavaScript Library', 'freeCodeCamp.org', 'Components, props, state and hooks with a project.', mode='Hands-on', q='React Course Beginners Tutorial for React JavaScript Library freeCodeCamp.org')],
  [A('Learn React', 'react.dev', 'https://react.dev/learn', 'Official interactive tutorial.')],
  ['Build components with props and state.', 'Fetch data from an API and render it.'],
  'Rebuild your JavaScript project in React and fetch data from a public API.')

T('api-backend', 'APIs & backend basics', ['api', 'backend', 'http', 'rest', 'flask', 'django', 'node', 'crud', 'server', 'framework'],
  [V('Flask Tutorial for Beginners', 'Corey Schafer', 'Practical Flask series: routes, templates, forms and database.', mode='Hands-on', q='Python Flask Tutorial Web Application Corey Schafer'),
   V('APIs for Beginners – How to use an API', 'freeCodeCamp.org', 'What APIs are and how to call them.', q='APIs for Beginners How to use an API freeCodeCamp.org')],
  [A('An overview of HTTP', 'MDN Web Docs', 'https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview', 'Requests, responses, methods and status codes.'),
   A('Flask Quickstart', 'Flask Docs', 'https://flask.palletsprojects.com/en/stable/quickstart/', 'Official minimal app and routing guide.')],
  ['Explain GET vs POST and common status codes.', 'Build routes that create and read records.'],
  'Build a small CRUD app (notes or expenses) with Flask and SQLite.')

T('python-basics', 'Python programming basics', ['python', 'programming foundation', 'variables', 'loops', 'command-line', 'scripting', 'script', 'functions', 'programming'],
  [V('Harvard CS50P – Introduction to Programming with Python', 'freeCodeCamp.org', 'Best concept-first beginner Python course with problem sets.', vid='nLRL_NcnK-4'),
   V('Python for Beginners – Learn Coding with Python in 1 Hour', 'Programming with Mosh', 'Fast one-hour start.', vid='kqtD5dpn9C8', length='~1 hr')],
  [A('The Python Tutorial', 'Python.org', 'https://docs.python.org/3/tutorial/', 'Official tutorial.'),
   A('Exercism – Python track', 'Exercism', 'https://exercism.org/tracks/python', 'Free exercises with feedback.')],
  ['Write programs with input, conditions, loops and functions.', 'Read a traceback and fix the error yourself.'],
  'Build a command-line tool (budget tracker or quiz) with input validation.',
  [('python-starter', 'first-program'), ('python-starter', 'variables-types'), ('python-starter', 'conditions'), ('python-starter', 'loops')])

T('oop-testing', 'OOP, testing & debugging', ['oop', 'object-oriented', 'object oriented', 'classes', 'testing', 'unit test', 'debugging', 'modular', 'software quality'],
  [V('Python OOP Tutorial', 'Corey Schafer', 'Classes, methods, inheritance with clear examples.', q='Python OOP Tutorial Classes and Instances Corey Schafer'),
   V('Pytest Tutorial – unit testing in Python', 'freeCodeCamp.org / Tech With Tim', 'Write and run your first tests.', mode='Hands-on', q='Pytest tutorial unit testing Python for beginners')],
  [A('Classes', 'Python.org Tutorial', 'https://docs.python.org/3/tutorial/classes.html', 'Official classes chapter.'),
   A('Getting started with pytest', 'pytest docs', 'https://docs.pytest.org/en/stable/getting-started.html', 'Write your first test in minutes.')],
  ['Model a real thing with a class and methods.', 'Write 5 tests including an edge case.'],
  'Turn your CLI tool into classes and add 5 pytest tests.')

T('dsa', 'Data structures & algorithms', ['data structure', 'algorithm', 'arrays', 'stacks', 'queues', 'sorting', 'searching', 'dsa', 'leetcode', 'problem solving'],
  [V('Data Structures Easy to Advanced Course', 'freeCodeCamp.org (William Fiset)', 'Full DSA course with animations; watch topic by topic.', q='Data Structures Easy to Advanced Course Full Tutorial William Fiset freeCodeCamp'),
   V('Harvard CS50x – Introduction to Computer Science', 'CS50', 'Strong problem-solving foundation, including algorithms.', q='CS50x Introduction to Computer Science full course Harvard')],
  [A('Learn Data Structures and Algorithms', 'GeeksforGeeks', 'https://www.geeksforgeeks.org/learn-data-structures-and-algorithms-dsa-tutorial/', 'Topic-wise written tutorials and practice.'),
   A('Exercism', 'Exercism', 'https://exercism.org/', 'Free practice problems with feedback.')],
  ['Choose a data structure for a problem and justify it.', 'Explain time complexity of a simple loop and a nested loop.'],
  'Solve and explain 20 beginner problems (arrays, strings, searching, sorting).')

T('sql', 'SQL & databases', ['sql', 'database', 'query', 'select', 'join', 'group by', 'queries'],
  [V('SQL Tutorial – Full Database Course for Beginners', 'freeCodeCamp.org', 'Complete beginner SQL course with practice queries.', mode='Hands-on', q='SQL Tutorial Full Database Course for Beginners freeCodeCamp.org')],
  [A('SQLBolt – interactive lessons', 'SQLBolt', 'https://sqlbolt.com/', 'Learn SQL by writing queries in the browser.'),
   A('Kaggle Learn – Intro to SQL', 'Kaggle', 'https://www.kaggle.com/learn/intro-to-sql', 'Short hands-on course.')],
  ['Write SELECT with WHERE, GROUP BY and ORDER BY.', 'Join two tables and explain the result.'],
  'Complete all SQLBolt lessons and write 10 queries on a sample dataset.')

T('spreadsheets', 'Spreadsheets & Excel', ['spreadsheet', 'excel', 'formulas', 'pivot', 'google sheets', 'data quality'],
  [V('Excel formulas you need to master as a beginner', 'SimonSezIT', 'Core formulas explained simply.', mode='Hands-on', vid='vgEKAVWWyRo'),
   V('Excel Tutorial for Beginners – full course', 'Leila Gharani', 'Tables, references, pivot tables.', q='Excel tutorial for beginners full course Leila Gharani')],
  [A('Overview of formulas in Excel', 'Microsoft Support', 'https://support.microsoft.com/en-us/office/overview-of-formulas-in-excel-ecfdc708-9162-49e8-b993-c311f47ca173', 'Official formula reference.')],
  ['Use SUM, AVERAGE, IF, COUNTIF and lookup functions.', 'Build a pivot table to answer a question.'],
  'Analyse a 50-row dataset with formulas and a pivot table.',
  [('data-analytics', 'spreadsheet-basics')])

T('statistics', 'Statistics & probability', ['statistics', 'probability', 'distribution', 'descriptive', 'average', 'variance', 'hypothesis', 'math'],
  [V('Statistics Fundamentals', 'StatQuest with Josh Starmer', 'Clearest visual explanations of core statistics.', q='StatQuest Statistics Fundamentals playlist')],
  [A('Summarizing quantitative data', 'Khan Academy', 'https://www.khanacademy.org/math/statistics-probability/summarizing-quantitative-data', 'Free lessons with practice questions.')],
  ['Choose mean vs median and explain why.', 'Explain standard deviation in one sentence.'],
  'Compute mean, median and standard deviation of a real dataset and interpret them.',
  [('data-analytics', 'charts-statistics')])

T('pandas-analysis', 'Python for data analysis (Pandas)', ['pandas', 'numpy', 'data cleaning', 'notebook', 'data analysis', 'eda', 'dataset', 'jupyter'],
  [V('Pandas Tutorial (Python)', 'Corey Schafer', 'Practical Pandas series with real data.', mode='Hands-on', q='Python Pandas Tutorial Series Corey Schafer'),
   V('Data Analysis with Python – Full Course', 'freeCodeCamp.org', 'NumPy, Pandas and visualisation in one course.', q='Data Analysis with Python Full Course for Beginners freeCodeCamp')],
  [A('10 minutes to pandas', 'pandas docs', 'https://pandas.pydata.org/docs/user_guide/10min.html', 'Official quick tour.'),
   A('Kaggle Learn – Pandas', 'Kaggle', 'https://www.kaggle.com/learn/pandas', 'Hands-on exercises in notebooks.')],
  ['Load a CSV, clean missing values and group data.', 'Document each cleaning decision.'],
  'Clean a public dataset in a notebook and write 3 findings.')

T('visualisation', 'Data visualisation & dashboards', ['dashboard', 'visualisation', 'visualization', 'power bi', 'tableau', 'chart', 'storytelling'],
  [V('Power BI Full Course for Beginners', 'freeCodeCamp.org / Microsoft', 'Build a report and dashboard end to end.', mode='Hands-on', q='Power BI full course for beginners freeCodeCamp'),
   V('Storytelling with Data', 'Cole Nussbaumer Knaflic (Talks at Google)', 'How to make charts that communicate.', q='storytelling with data Cole Nussbaumer Knaflic talk')],
  [A('Power BI learning paths', 'Microsoft Learn', 'https://learn.microsoft.com/training/powerplatform/power-bi/', 'Official guided learning.'),
   A('Kaggle Learn – Data Visualization', 'Kaggle', 'https://www.kaggle.com/learn/data-visualization', 'Hands-on charts.')],
  ['Choose a chart that fits the question.', 'State one limitation of your dashboard.'],
  'Publish a one-page dashboard with 3 charts and a short insight summary.')

T('machine-learning', 'Machine learning', ['machine learning', 'ml model', 'train', 'prediction', 'scikit', 'evaluation', 'ml ', 'neural', 'regression', 'classification'],
  [V('Machine Learning for Everybody – Full Course', 'freeCodeCamp.org', 'Beginner ML with code.', q='Machine Learning for Everybody Full Course freeCodeCamp'),
   V('Neural Networks', '3Blue1Brown', 'Visual intuition for neural networks.', pl='PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr')],
  [A('Machine Learning Crash Course', 'Google for Developers', 'https://developers.google.com/machine-learning/crash-course', 'Free interactive course.'),
   A('Kaggle Learn – Intro to Machine Learning', 'Kaggle', 'https://www.kaggle.com/learn/intro-to-machine-learning', 'Build your first models.')],
  ['Split data into train and test sets and explain why.', 'Compare a baseline and a model with a metric.'],
  'Train a baseline model on a Kaggle beginner dataset and report accuracy honestly.')

T('responsible-ai', 'Responsible AI & model validation', ['responsible ai', 'fairness', 'explainability', 'bias', 'leakage', 'imbalance', 'validation', 'ethic'],
  [V('Responsible AI explained', 'Google / IBM Technology', 'Fairness, bias and safe deployment.', q='responsible AI fairness bias explained IBM Technology')],
  [A('Responsible AI practices', 'Google AI', 'https://ai.google/responsibility/responsible-ai-practices/', 'Principles and practical recommendations.')],
  ['Explain data leakage with an example.', 'List two ways a model can be unfair.'],
  'Add a limitations section to your model project: data issues, bias risks, and what it must not be used for.')

T('networking', 'Networking basics', ['network', 'ip address', 'dns', 'tcp', 'osi', 'router', 'ip,'],
  [V('The Internet: IP Addresses & DNS', 'Code.org', 'Fast visual introduction.', vid='5o8CwafCxnU', length='~5 min'),
   V('How a DNS Server (Domain Name System) works', 'PowerCert Animated Videos', 'Animated DNS lookup.', vid='mpQZVYPuDGU'),
   V('Computer Networking Full Course', 'freeCodeCamp.org', 'OSI, TCP/IP, switches and routers.', mode='Hands-on', q='Computer Networking Full Course freeCodeCamp OSI TCP/IP')],
  [A('What is DNS?', 'Cloudflare', 'https://www.cloudflare.com/learning/dns/what-is-dns/', 'Illustrated DNS lookup.')],
  ['Explain what happens when you open a website.', 'Use ping and nslookup and interpret the output.'],
  'Draw a labelled network diagram of your home setup and run ping/nslookup.',
  [('cybersecurity', 'network-basics')])

T('linux', 'Linux & command line', ['linux', 'command line', 'terminal', 'shell', 'permissions', 'operating system', 'bash'],
  [V('Introduction to Linux – Full Course for Beginners', 'freeCodeCamp.org', 'Complete beginner Linux course.', mode='Hands-on', vid='sWbUDq4S6Y8')],
  [A('The 50 most used Linux terminal commands', 'freeCodeCamp News', 'https://www.freecodecamp.org/news/learn-the-50-most-used-linux-terminal-commands/', 'Command reference.'),
   A('OverTheWire: Bandit', 'OverTheWire', 'https://overthewire.org/wargames/bandit/', 'Legal game that teaches Linux by solving levels.')],
  ['Navigate, create and search files from the terminal.', 'Read and change file permissions.'],
  'Complete Bandit levels 0–8 and note each new command.',
  [('cybersecurity', 'linux-basics')])

T('security-fundamentals', 'Security fundamentals', ['security fundamental', 'threat', 'encryption', 'authentication', 'cyber', 'hardening', 'secure', 'cia'],
  [V('The CIA Triad – CompTIA Security+', 'Professor Messer', 'Confidentiality, integrity, availability.', vid='SBcDGb9l6yo'),
   V('Cybersecurity basics for beginners', 'IBM Technology', 'Threats, MFA and phishing overview.', q='IBM Technology cybersecurity basics beginners')],
  [A('OWASP Top 10', 'OWASP', 'https://owasp.org/www-project-top-ten/', 'Common web application risks.'),
   A('Secure Our World', 'CISA', 'https://www.cisa.gov/secure-our-world', 'Practical safe-computing guidance.')],
  ['Apply CIA to a real system.', 'Describe a basic threat model for a login page.'],
  'Write a one-page security checklist for a small web app you built.',
  [('cybersecurity', 'security-ethics')])

T('security-labs', 'Defensive labs, logs & incident basics', ['log', 'incident', 'labs', 'ctf', 'penetration', 'authorised practice', 'authorized', 'defensive', 'playbook'],
  [V('Intro to cybersecurity labs (TryHackMe walkthrough)', 'TryHackMe', 'Guided, legal beginner labs.', mode='Hands-on', q='TryHackMe Pre Security path walkthrough beginners')],
  [A('Web Security Academy', 'PortSwigger', 'https://portswigger.net/web-security', 'Free labs; only practise on these legal targets.'),
   A('TryHackMe', 'TryHackMe', 'https://tryhackme.com/', 'Guided rooms for beginners.')],
  ['Write down findings and a mitigation for each lab.', 'Explain why testing needs authorisation.'],
  'Complete 5 beginner labs and write a short, safe lab journal.')

T('business-analysis', 'Business analysis & requirements', ['requirement', 'stakeholder', 'user stories', 'user story', 'process', 'workflow', 'business problem', 'business'],
  [V('Business Analysis tutorial for beginners', 'Business Analyst Learnings', 'Requirements, stakeholders, user stories.', q='business analysis tutorial for beginners requirements user stories'),
   V('Process mapping basics', 'YouTube search', 'Draw a flow with decisions and handoffs.', mode='Hands-on', q='process mapping flowchart tutorial business analysis beginners')],
  [A('Business analysis guide', 'Atlassian', 'https://www.atlassian.com/agile/business-analysis', 'Requirements and stakeholders.'),
   A('Process mapping guide and symbols', 'Lucidchart', 'https://lucid.co/lucidchart/tutorial/process-mapping-guide-and-symbols', 'Symbols and steps.')],
  ['Write 5 user stories with acceptance criteria.', 'Map a current and future workflow.'],
  'Pick a campus process, map it, find one bottleneck and write a recommendation.',
  [('business-analysis', 'problem-framing'), ('business-analysis', 'process-mapping')])

T('communication', 'Communication, writing & presentation', ['communication', 'writing', 'presentation', 'documentation', 'report', 'technical writing', 'present', 'recommendation'],
  [V('How to speak so that people want to listen', 'Julian Treasure (TED)', 'Clear, confident speaking.', q='How to speak so that people want to listen Julian Treasure TED'),
   V('How to write a professional email', 'YouTube search', 'Subject, ask and deadline.', mode='Hands-on', q='how to write a professional email clear ask deadline')],
  [A('Technical Writing One', 'Google for Developers', 'https://developers.google.com/tech-writing/one', 'Free course on clear writing.')],
  ['Summarise your work in 3 sentences.', 'Write a short, clear email with an ask and deadline.'],
  'Present your latest project in 3 minutes to a friend and ask them to repeat the main point.',
  [('career-digital', 'communication'), ('business-analysis', 'presenting-insights')])

T('portfolio-interview', 'Portfolio, resume & interview preparation', ['portfolio', 'interview', 'resume', 'job', 'deploy', 'case study', 'career', 'walkthrough', 'readiness'],
  [V('How to build a portfolio website', 'freeCodeCamp.org', 'Build and deploy a simple portfolio.', mode='Hands-on', q='how to build a developer portfolio website beginners freeCodeCamp'),
   V('STAR method interview answers', 'YouTube search', 'Structure behavioural answers.', q='STAR method interview answers explained examples')],
  [A('GitHub Pages', 'GitHub', 'https://pages.github.com/', 'Free hosting for a portfolio site.'),
   A('Technical Writing One', 'Google for Developers', 'https://developers.google.com/tech-writing/one', 'Clear project descriptions and READMEs.')],
  ['Explain each project: problem, your role, result, limits.', 'Answer 5 common interview questions aloud.'],
  'Publish a portfolio with 2 projects and record a 3-minute walkthrough of one.')

T('engineering-fundamentals', 'Engineering practice & measurement', ['measurement', 'engineering', 'lab', 'practical', 'units', 'prototype', 'investigation', 'discipline'],
  [V('The Engineering Design Process', 'NASA / TryEngineering', 'Ask, imagine, plan, create, improve.', q='engineering design process explained steps'),
   V('Accuracy vs precision', 'YouTube search', 'Measurement errors explained.', q='accuracy vs precision measurement error explained')],
  [A('Engineering design process', 'Wikipedia', 'https://en.wikipedia.org/wiki/Engineering_design_process', 'Overview of stages.'),
   A('NPTEL courses', 'NPTEL', 'https://nptel.ac.in/courses', 'Free IIT/IISc lectures for your branch.')],
  ['Write requirements and constraints for a problem.', 'Record measurements with units and repeat them.'],
  'Document one small practical investigation with method, results and limitations.',
  [('core-engineering', 'engineering-problems'), ('core-engineering', 'measurements'), ('core-engineering', 'technical-documentation')])

T('accessibility-design', 'Design, UX & accessibility', ['accessibility', 'design', 'ux', 'figma', 'creative', 'wcag', 'user research', 'prototype', 'ui'],
  [V('Figma tutorial for beginners', 'Figma / freeCodeCamp', 'Frames, components and prototypes.', mode='Hands-on', q='Figma tutorial for beginners UI design full course'),
   V('Intro to Web Accessibility', 'Google Chrome Developers (A11ycasts)', 'Practical accessibility techniques.', q='A11ycasts Google Chrome Developers accessibility')],
  [A('Learn Accessibility', 'web.dev', 'https://web.dev/learn/accessibility/', 'Professional accessibility course.'),
   A('Figma resource library', 'Figma', 'https://www.figma.com/resource-library/', 'Guides and tutorials.')],
  ['Check contrast, alt text and keyboard access.', 'Prototype a flow in Figma.'],
  'Design a 3-screen mobile flow in Figma and test it with one real user.')

T('research-skills', 'Research & evidence skills', ['research', 'sources', 'evidence', 'literature', 'citation', 'critical thinking', 'source evaluation'],
  [V('How to read a research paper', 'YouTube search', 'Efficient strategies for reading papers.', q='how to read a research paper efficiently students')],
  [A('Zotero documentation', 'Zotero', 'https://www.zotero.org/support/', 'Manage references and citations.'),
   A('Google Scholar', 'Google', 'https://scholar.google.com/', 'Find and trace scholarly sources.')],
  ['Evaluate a source for quality and bias.', 'Cite and organise sources in a tool.'],
  'Write a one-page evidence summary with 5 cited sources.')

T('digital-fluency', 'Digital tools & productivity', ['digital', 'productivity', 'tools', 'file', 'google docs', 'office'],
  [V('Computer basics and file management', 'GCFGlobal', 'Files, folders, search and safety.', q='GCFGlobal computer basics managing files and folders')],
  [A('Computer Basics', 'GCFGlobal', 'https://edu.gcfglobal.org/en/computerbasics/', 'Free interactive lessons.'),
   A('Secure Our World', 'CISA', 'https://www.cisa.gov/secure-our-world', 'Passwords, MFA and phishing basics.')],
  ['Organise files with a clear structure.', 'Use MFA and a password manager.'],
  'Reorganise your study folders and enable MFA on your main accounts.',
  [('career-digital', 'digital-basics'), ('career-digital', 'problem-solving')])

DEFAULT_TOPIC = 'communication'


def _hit(kw, text):
    kw = kw.strip().lower()
    if not kw: return False
    if len(kw) <= 3:
        return re.search(r'\b' + re.escape(kw) + r'\b', text) is not None
    return re.search(r'\b' + re.escape(kw), text) is not None


def match_topics(week, limit=3):
    """Return topic dicts for a roadmap week (free text, from Gemini or the fallback)."""
    ids = [i for i in (week.get('topic_ids') or []) if i in TOPICS]
    text = ' '.join(str(week.get(k, '')) for k in ('focus', 'learn_and_practise', 'proof_of_skill')).lower()
    focus = str(week.get('focus', '')).lower()
    scored = []
    for tid, t in TOPICS.items():
        sc = sum((3 if _hit(k, focus) else 1) for k in t['kw'] if _hit(k, text))
        if sc: scored.append((sc, tid))
    scored.sort(key=lambda x: -x[0])
    top = scored[0][0] if scored else 0
    cutoff = max(2, top * 0.5) if top > 1 else 1  # drop weak, accidental keyword matches
    for sc, tid in scored:
        if sc >= cutoff and tid not in ids: ids.append(tid)
    if not ids: ids = [DEFAULT_TOPIC]
    return [TOPICS[i] for i in ids[:limit]]
