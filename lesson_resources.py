"""Per-lesson study resources for the CAREERVERSE Learning Academy.

Every lesson has:
  videos   - YouTube videos / playlists (concept first, then hands-on)
  articles - written resources for students who prefer reading
  mastery  - "you have mastered this when..." self-check list
  handson  - one practice activity to do right after watching

Link policy
  * 'vid' / 'pl'  -> direct YouTube video / playlist link (ID confirmed).
  * 'q'           -> YouTube search link. Search text contains the exact video title
                     and channel, so the intended video is the top result. Used where a
                     direct ID could not be confirmed, so the app never ships a dead link.
Edit this file to swap or add resources; no other code needs to change.
"""
from urllib.parse import quote_plus


def V(title, channel, why, mode='Concept', lang='English', vid=None, pl=None, q=None, length=''):
    if vid:
        url, kind, direct = f'https://www.youtube.com/watch?v={vid}', 'Video', True
    elif pl:
        url, kind, direct = f'https://www.youtube.com/playlist?list={pl}', 'Playlist', True
    else:
        url, kind, direct = 'https://www.youtube.com/results?search_query=' + quote_plus(q or f'{title} {channel}'), 'Video', False
    return {'title': title, 'channel': channel, 'why': why, 'mode': mode, 'lang': lang,
            'url': url, 'kind': kind, 'direct': direct, 'length': length}


def A(title, source, url, why=''):
    return {'title': title, 'source': source, 'url': url, 'why': why}


LESSON_RESOURCES = {
 # ───────────────────────── WEB FOUNDATIONS ─────────────────────────
 ('web-foundations', 'how-the-web-works'): {
  'videos': [
   V('The Internet: IP Addresses & DNS', 'Code.org', 'Short, animated and exact: what happens between typing a URL and seeing a page.', vid='5o8CwafCxnU', length='~5 min'),
   V('How Does the Internet Actually Work?', 'Dr. Angela Yu (Web Development Bootcamp)', 'Explains browser, server, request and response in beginner language.', vid='ULsBDQcD-Vk'),
   V('How a DNS Server (Domain Name System) works', 'PowerCert Animated Videos', 'Animated step-by-step DNS lookup. Watch after the Code.org video to go one level deeper.', vid='mpQZVYPuDGU'),
   V('HTML CSS JavaScript kya hai? Web development kaise kaam karti hai (Hindi)', 'CodeWithHarry', 'Hindi overview of how websites work and what each language does.', lang='Hindi', q='how website works HTML CSS JavaScript explained in Hindi CodeWithHarry'),
  ],
  'articles': [
   A('How the Web works', 'MDN Web Docs', 'https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web/How_the_Web_works', 'Official beginner article with diagrams: client, server, DNS, HTTP.'),
   A('What is DNS?', 'Cloudflare Learning Center', 'https://www.cloudflare.com/learning/dns/what-is-dns/', 'Clear, illustrated DNS explanation.'),
  ],
  'mastery': ['Explain what a browser, server and DNS each do when you open a website.', 'Say in one sentence what HTML, CSS and JavaScript are responsible for.', 'Open Developer Tools (F12) and point to the HTML of any page.'],
  'handson': 'Open any site, press F12, hover over elements and change a heading text in the Elements tab. Notice that only your browser copy changes.',
 },
 ('web-foundations', 'html-structure'): {
  'videos': [
   V('Learn HTML & CSS – Full Course for Beginners', 'freeCodeCamp.org', 'Build while you watch. Watch the HTML part first (headings, paragraphs, links, images, lists, forms).', mode='Hands-on', vid='a_iQb1lnAEQ'),
   V('HTML tutorial for beginners in Hindi (complete course with projects)', 'CodeWithHarry', 'Complete Hindi HTML course with notes and mini projects.', mode='Hands-on', lang='Hindi', q='HTML tutorial for beginners in Hindi complete HTML course CodeWithHarry'),
  ],
  'articles': [
   A('Structuring content with HTML', 'MDN Web Docs', 'https://developer.mozilla.org/en-US/docs/Learn/HTML', 'Official step-by-step module with exercises.'),
   A('HTML Full Course for Beginners', 'freeCodeCamp News', 'https://www.freecodecamp.org/news/html-full-course-for-beginners', 'Written companion to the video course.'),
  ],
  'mastery': ['Write a full page skeleton (doctype, html, head, body) from memory.', 'Use h1–h3, p, a, img (with alt text), ul/ol correctly.', 'Explain why heading order matters for accessibility.'],
  'handson': 'Build a one-page "About me" site without copying: title, 3 headings, a list of interests, one link, one image with alt text.',
 },
 ('web-foundations', 'css-basics'): {
  'videos': [
   V('Learn HTML & CSS – Full Course for Beginners', 'freeCodeCamp.org', 'Use the CSS section to practise selectors, box model, colours and fonts.', mode='Hands-on', vid='a_iQb1lnAEQ'),
   V('CSS tutorial for beginners (Zero to Hero)', 'Kevin Powell', 'Kevin Powell is the standard recommendation for really understanding CSS (cascade, box model, specificity).', q='CSS tutorial for beginners zero to hero Kevin Powell'),
   V('CSS tutorial in Hindi (with notes)', 'CodeWithHarry', 'Hindi CSS series covering selectors, box model and positioning.', lang='Hindi', mode='Hands-on', q='CSS tutorial in Hindi with notes CodeWithHarry'),
  ],
  'articles': [
   A('CSS first steps', 'MDN Web Docs', 'https://developer.mozilla.org/en-US/docs/Learn/CSS/First_steps', 'Selectors, box model, colours, text styling with practice tasks.'),
   A('The box model', 'MDN Web Docs', 'https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/The_box_model', 'The one concept that explains most "why is my layout broken" problems.'),
  ],
  'mastery': ['Write class, id and element selectors and explain the difference.', 'Explain margin vs padding vs border.', 'Style a .profile-card from scratch and describe each property.'],
  'handson': 'Take your Lesson 2 page and make it look professional: font pair, colour palette, spacing, one card component.',
 },
 ('web-foundations', 'responsive-project'): {
  'videos': [
   V('Web Development with HTML & CSS – Full Course for Beginners', 'freeCodeCamp.org', 'Project-based: you finish with real pages that you can show in a portfolio.', mode='Hands-on', vid='dX8396ZmSPk'),
   V('Responsive web design: media queries, flexbox and grid', 'Kevin Powell', 'Search his responsive-layout videos to learn flexbox/grid that adapts without many breakpoints.', q='responsive layout flexbox grid media queries Kevin Powell'),
  ],
  'articles': [
   A('Responsive design', 'MDN Web Docs', 'https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Responsive_Design', 'Media queries, viewport meta tag and mobile-first thinking.'),
   A('How to start thinking responsively', 'freeCodeCamp News', 'https://www.freecodecamp.org/news/how-to-start-thinking-responsively/', 'Practical mindset article by Kevin Powell.'),
   A('Conquering Responsive Layouts (free course)', 'Kevin Powell', 'https://courses.kevinpowell.co/conquering-responsive-layouts', 'Free video course that builds real responsive projects.'),
  ],
  'mastery': ['Add the viewport meta tag and explain why it is needed.', 'Write a media query that turns 2 columns into 1 on phones.', 'Test your page at 360px, 768px and 1280px using DevTools device mode.'],
  'handson': 'Build the portfolio page (About, Skills, Projects, Contact). Deploy it free on GitHub Pages or Netlify and open it on your phone.',
 },

 # ───────────────────────── PYTHON ─────────────────────────
 ('python-starter', 'first-program'): {
  'videos': [
   V('Harvard CS50P – Introduction to Programming with Python (full course)', 'freeCodeCamp.org', 'Best concept-first beginner course. Watch Lecture 0 (functions, variables) and do the problem set.', vid='nLRL_NcnK-4'),
   V('Python for Beginners – Learn Coding with Python in 1 Hour', 'Programming with Mosh', 'Fast one-hour overview if you want to start coding today.', vid='kqtD5dpn9C8', length='~1 hr'),
   V('Python for Beginners (Full Course) #100DaysOfCode', 'CodeWithHarry', 'Hindi playlist; follow along daily with code.', lang='Hindi', mode='Hands-on', pl='PLu0W_9lII9agwh1XjRt242xIpHhPT2llg'),
  ],
  'articles': [
   A('An Informal Introduction to Python', 'Python.org Tutorial', 'https://docs.python.org/3/tutorial/introduction.html', 'The official first read: numbers, text, lists.'),
   A('Installing Python 3 on any platform', 'Real Python', 'https://realpython.com/installing-python/', 'Step-by-step install guide so you can run your first script.'),
  ],
  'mastery': ['Install Python and run a .py file from the terminal.', 'Use print() and input() together in one program.', 'Read and fix a SyntaxError by yourself.'],
  'handson': 'Write a program that asks for your name and degree and prints a one-line introduction. Then change it so it prints 3 lines.',
 },
 ('python-starter', 'variables-types'): {
  'videos': [
   V('CS50P Lecture 0 – Functions, Variables', 'CS50 / freeCodeCamp', 'Same full course; focus on variables, strings, int/float and formatting.', vid='nLRL_NcnK-4'),
   V('Python Variables – Python Tutorial for Beginners', 'Programming with Mosh', 'Short and clear on variables and types.', q='Python Variables Python Tutorial for Beginners with Examples Mosh'),
   V('Python for Beginners (Full Course) #100DaysOfCode', 'CodeWithHarry', 'Hindi: variables, data types and typecasting inside the playlist.', lang='Hindi', mode='Hands-on', pl='PLu0W_9lII9agwh1XjRt242xIpHhPT2llg'),
  ],
  'articles': [
   A('Variables in Python', 'Real Python', 'https://realpython.com/python-variables/', 'Explains names, values and types with examples.'),
   A('Numbers and strings', 'Python.org Tutorial', 'https://docs.python.org/3/tutorial/introduction.html#using-python-as-a-calculator', 'Official reference examples you can paste into the REPL.'),
  ],
  'mastery': ['Name the four common types (int, float, str, bool) and use type() to check them.', 'Convert between types (int("5"), str(5)) and explain why input() returns text.', 'Format an output with an f-string.'],
  'handson': 'Create a "product card" program: store name, price, stock flag, then print a formatted line using an f-string.',
 },
 ('python-starter', 'conditions'): {
  'videos': [
   V('CS50P Lecture 1 – Conditionals', 'CS50 / freeCodeCamp', 'Best explanation of if/elif/else and boolean expressions; includes live-coding mistakes.', vid='nLRL_NcnK-4'),
   V('Python if, elif, else statements', 'Corey Schafer', 'Search his Python conditionals video for truthy/falsy values and common patterns.', q='Python Tutorial Conditionals and Booleans if else elif Corey Schafer'),
   V('Python for Beginners (Full Course) #100DaysOfCode', 'CodeWithHarry', 'Hindi: conditional statements chapter with exercises.', lang='Hindi', mode='Hands-on', pl='PLu0W_9lII9agwh1XjRt242xIpHhPT2llg'),
  ],
  'articles': [
   A('if Statements', 'Python.org Tutorial', 'https://docs.python.org/3/tutorial/controlflow.html#if-statements', 'Official syntax reference.'),
   A('Conditional Statements in Python', 'Real Python', 'https://realpython.com/python-conditional-statements/', 'Deep dive with examples and pitfalls.'),
  ],
  'mastery': ['Write if/elif/else for 3 or more outcomes (e.g. grade bands).', 'Combine conditions with and, or, not.', 'Predict the output of a snippet before running it.'],
  'handson': 'Write a grade calculator: marks to grade (A/B/C/Fail) with input validation for marks outside 0–100.',
 },
 ('python-starter', 'loops'): {
  'videos': [
   V('CS50P Lecture 2 – Loops', 'CS50 / freeCodeCamp', 'Teaches while and for loops, range, and how to think about repetition.', vid='nLRL_NcnK-4'),
   V('Python for loops and while loops', 'Corey Schafer', 'Search his Loops and Iterations video for break, continue and enumerate.', q='Python Tutorial Loops and Iterations for/while Corey Schafer'),
   V('Python for Beginners (Full Course) #100DaysOfCode', 'CodeWithHarry', 'Hindi: loops chapter with practice sets.', lang='Hindi', mode='Hands-on', pl='PLu0W_9lII9agwh1XjRt242xIpHhPT2llg'),
  ],
  'articles': [
   A('for Statements and range()', 'Python.org Tutorial', 'https://docs.python.org/3/tutorial/controlflow.html#for-statements', 'Official explanation of for and range().'),
   A('Python "for" Loops', 'Real Python', 'https://realpython.com/python-for-loop/', 'Complete guide with practice-friendly examples.'),
   A('Exercism – Python track', 'Exercism', 'https://exercism.org/tracks/python', 'Free exercises with feedback to cement loops and conditions.'),
  ],
  'mastery': ['Use range(start, stop, step) correctly.', 'Spot and fix an infinite while loop.', 'Solve sum, count and "find the maximum" problems with a loop.'],
  'handson': 'Print a multiplication table for any number, then FizzBuzz 1–50, then sum of even numbers 1–100.',
 },

 # ───────────────────────── DIGITAL & PROFESSIONAL ─────────────────────────
 ('career-digital', 'digital-basics'): {
  'videos': [
   V('Computer Basics – files, folders and operating system', 'GCFGlobal', 'Search GCFGlobal computer basics videos for files, folders and managing data.', q='GCFGlobal Computer Basics managing files and folders'),
   V('Digital literacy course for beginners', 'freeCodeCamp.org / Google Applied Digital Skills', 'Search for project-based lessons: Drive, Docs, Sheets, safe browsing.', mode='Hands-on', q='digital skills beginners file management Google Drive tutorial'),
  ],
  'articles': [
   A('Computer Basics (free lessons)', 'GCFGlobal', 'https://edu.gcfglobal.org/en/computerbasics/', 'Step-by-step lessons with interactive practice.'),
   A('Secure Our World', 'CISA', 'https://www.cisa.gov/secure-our-world', 'Official, simple guidance: passwords, MFA, phishing, updates.'),
  ],
  'mastery': ['Use a consistent folder structure and file naming convention.', 'Explain strong password + MFA in your own words.', 'Know how to back up important files (3-2-1 idea).'],
  'handson': 'Reorganise your own laptop/phone study folder into Year > Semester > Subject, rename 10 files clearly, enable MFA on your email.',
 },
 ('career-digital', 'communication'): {
  'videos': [
   V('How to write a professional email', 'YouTube search', 'Look for a short video with subject line, greeting, clear ask and deadline examples.', mode='Hands-on', q='how to write a professional email students clear ask deadline'),
   V('How to speak so that people want to listen', 'Julian Treasure (TED)', 'Classic talk on clear, confident speaking.', q='How to speak so that people want to listen Julian Treasure TED'),
  ],
  'articles': [
   A('Technical Writing One – clear sentences', 'Google for Developers', 'https://developers.google.com/tech-writing/one', 'Free course on short, active, precise writing that works for any email or report.'),
  ],
  'mastery': ['Write an email with context, ask and deadline in under 120 words.', 'Rewrite a vague message into a specific one.', 'Know what to attach and what not to share.'],
  'handson': 'Write a real email to a faculty member or HR asking for a clarification or internship. Ask a friend: "What is the one thing I am asking for?"',
 },
 ('career-digital', 'problem-solving'): {
  'videos': [
   V('How to solve problems like an engineer / debugging mindset', 'YouTube search', 'Pick a video that shows define → hypothesis → test one change → record.', q='problem solving framework define hypothesis test students'),
   V('Rubber duck debugging explained', 'YouTube search', 'Short explanation of explaining a problem aloud to find the cause.', q='rubber duck debugging explained'),
  ],
  'articles': [
   A('Problem solving', 'Wikipedia (overview)', 'https://en.wikipedia.org/wiki/Problem_solving', 'Overview of common methods and terminology.'),
   A("Polya's How to Solve It (summary)", 'Wikipedia', 'https://en.wikipedia.org/wiki/How_to_Solve_It', 'The classic four-step method: understand, plan, carry out, look back.'),
  ],
  'mastery': ['Break a problem into 3–5 smaller steps.', 'Change only one thing at a time and record the result.', 'Write down what you tried when asking for help.'],
  'handson': 'Pick a real small problem (Wi-Fi drops, slow laptop). Write: problem, 3 possible causes, test for each, result.',
 },

 # ───────────────────────── DATA ANALYTICS ─────────────────────────
 ('data-analytics', 'data-thinking'): {
  'videos': [
   V('Data analysis process: ask, prepare, process, analyze, share, act', 'Google Career Certificates', 'Search for the Google Data Analytics overview of the six-step analysis process.', q='Google Data Analytics six steps ask prepare process analyze share act'),
   V('Data Analytics for Beginners', 'Alex The Analyst', 'Practical, beginner-friendly analyst roadmap and thinking.', q='Alex The Analyst Data Analytics for beginners full course'),
  ],
  'articles': [
   A('Data analysis – process overview', 'Wikipedia', 'https://en.wikipedia.org/wiki/Data_analysis', 'Terminology, data cleaning, and common mistakes.'),
   A('Kaggle Learn – Data Cleaning', 'Kaggle', 'https://www.kaggle.com/learn/data-cleaning', 'Free hands-on micro-course on missing values and inconsistent data.'),
  ],
  'mastery': ['Turn a vague topic into a specific, answerable question.', 'List data fields, source and possible bias.', 'Explain the difference between correlation and causation with one example.'],
  'handson': 'Write the question "Does attendance affect marks in our class?" then list 3 fields, where to get them ethically, and 2 limitations.',
 },
 ('data-analytics', 'spreadsheet-basics'): {
  'videos': [
   V('Excel formulas you need to master as a beginner', 'SimonSezIT', 'Core formulas explained simply; pause and do each one yourself.', mode='Hands-on', vid='vgEKAVWWyRo'),
   V('Excel Tutorial for Beginners – full course', 'Leila Gharani / ExcelIsFun', 'Search for a complete beginner course to cover tables, absolute references and sorting/filtering.', q='Excel tutorial for beginners full course Leila Gharani'),
   V('Excel in Hindi – formulas and functions', 'Computer Gyan / Excel Hindi channels', 'Hindi spreadsheet formulas, SUM, AVERAGE, IF, VLOOKUP.', lang='Hindi', mode='Hands-on', q='Excel formulas and functions full course in Hindi beginners'),
  ],
  'articles': [
   A('Overview of formulas in Excel', 'Microsoft Support', 'https://support.microsoft.com/en-us/office/overview-of-formulas-in-excel-ecfdc708-9162-49e8-b993-c311f47ca173', 'Official reference for formula syntax and references.'),
   A('Easy Excel Formulas and Functions Tutorial', 'Pragmatic Works', 'https://pragmaticworks.com/blog/easy-excel-formulas-and-functions-tutorial', 'Written walkthrough of the most used functions.'),
  ],
  'mastery': ['Use SUM, AVERAGE, COUNT, MIN, MAX, IF without notes.', 'Explain relative (A1) vs absolute ($A$1) references.', 'Sort and filter a table without breaking rows.'],
  'handson': 'Make a monthly expense sheet with 15 rows: totals per category, average, highest expense and an IF flag for "over budget".',
 },
 ('data-analytics', 'charts-statistics'): {
  'videos': [
   V('Statistics Fundamentals (mean, median, standard deviation, distributions)', 'StatQuest with Josh Starmer', 'The clearest visual statistics explanations on YouTube; watch the first 6–8 videos in order.', q='StatQuest Statistics Fundamentals playlist'),
   V('Choosing the right chart', 'Storytelling with Data', 'Search for videos on picking bar vs line charts and avoiding misleading scales.', mode='Hands-on', q='choosing the right chart bar line scatter misleading charts storytelling with data'),
  ],
  'articles': [
   A('Summarizing quantitative data', 'Khan Academy', 'https://www.khanacademy.org/math/statistics-probability/summarizing-quantitative-data', 'Free lessons + practice questions on mean, median, spread.'),
   A('Kaggle Learn – Data Visualization', 'Kaggle', 'https://www.kaggle.com/learn/data-visualization', 'Hands-on charts in notebooks.'),
  ],
  'mastery': ['Choose between mean and median and explain why.', 'Pick the right chart for category comparison vs trend over time.', 'Spot a misleading axis or cut-off in someone else’s chart.'],
  'handson': 'Take 20 numbers (e.g. class marks). Calculate mean, median, range; make one bar chart and one line chart; write 2 honest observations.',
 },

 # ───────────────────────── CYBERSECURITY ─────────────────────────
 ('cybersecurity', 'network-basics'): {
  'videos': [
   V('How a DNS Server (Domain Name System) works', 'PowerCert Animated Videos', 'Animated DNS explanation to connect domain names with IP addresses.', vid='mpQZVYPuDGU'),
   V('The Internet: IP Addresses & DNS', 'Code.org', 'Fast visual introduction to IP addresses.', vid='5o8CwafCxnU', length='~5 min'),
   V('Computer Networking Full Course for beginners', 'freeCodeCamp.org', 'Long-form coverage of OSI, TCP/IP, switches and routers.', mode='Hands-on', q='Computer Networking Full Course freeCodeCamp OSI TCP/IP'),
  ],
  'articles': [
   A('What is DNS?', 'Cloudflare Learning Center', 'https://www.cloudflare.com/learning/dns/what-is-dns/', 'Illustrated DNS lookup process.'),
   A('What is the OSI model?', 'Cloudflare Learning Center', 'https://www.cloudflare.com/learning/ddos/glossary/open-systems-interconnection-model-osi/', 'Layered view of network communication.'),
  ],
  'mastery': ['Describe a DNS lookup in 4 steps.', 'Differentiate IP address, MAC address and port.', 'Run ping and nslookup and interpret the result.'],
  'handson': 'Run ping google.com and nslookup google.com on your laptop. Draw your home network: phone → Wi-Fi router → ISP → internet.',
 },
 ('cybersecurity', 'linux-basics'): {
  'videos': [
   V('Introduction to Linux – Full Course for Beginners', 'freeCodeCamp.org', 'Complete beginner Linux course with live terminal use.', mode='Hands-on', vid='sWbUDq4S6Y8'),
   V('Linux command line basics (pwd, ls, cd, mkdir, cat, chmod)', 'NetworkChuck / Linux Journey', 'Search for short, practical command-line walkthroughs.', q='Linux command line basics pwd ls cd mkdir chmod beginners'),
   V('Linux tutorial in Hindi (commands for beginners)', 'Hindi channels', 'Hindi Linux commands and file permission explanations.', lang='Hindi', q='Linux commands tutorial for beginners in Hindi'),
  ],
  'articles': [
   A('The 50 most used Linux terminal commands', 'freeCodeCamp News', 'https://www.freecodecamp.org/news/learn-the-50-most-used-linux-terminal-commands/', 'Command reference with examples.'),
   A('Command line basics for beginners', 'freeCodeCamp News', 'https://www.freecodecamp.org/news/command-line-basics-for-beginners', 'Gentle written introduction.'),
   A('OverTheWire: Bandit', 'OverTheWire', 'https://overthewire.org/wargames/bandit/', 'Free, legal game that teaches Linux by solving levels.'),
  ],
  'mastery': ['Navigate with pwd, ls, cd and create files/folders.', 'Read permissions like rwxr-xr-- and explain who can do what.', 'Complete Bandit levels 0–5.'],
  'handson': 'Complete OverTheWire Bandit levels 0–5 and write what each new command did in your own words.',
 },
 ('cybersecurity', 'security-ethics'): {
  'videos': [
   V('The CIA Triad – CompTIA Security+ SY0-701 – 1.2', 'Professor Messer', 'Confidentiality, integrity, availability in a few minutes.', vid='SBcDGb9l6yo'),
   V('Cybersecurity basics for beginners', 'YouTube search', 'Look for a beginner overview with threats, MFA, phishing and responsible disclosure.', q='IBM Technology cybersecurity basics beginners phishing MFA'),
  ],
  'articles': [
   A('The CIA Triad', 'Professor Messer', 'https://www.professormesser.com/security-plus/sy0-701/sy0-701-video/the-cia-triad-sy0-701/', 'Written version with notes.'),
   A('OWASP Top 10', 'OWASP', 'https://owasp.org/www-project-top-ten/', 'Standard list of web application risks.'),
   A('Secure Our World', 'CISA', 'https://www.cisa.gov/secure-our-world', 'Practical safe-computing guidance.'),
  ],
  'mastery': ['Explain confidentiality, integrity, availability with one example each.', 'Explain why you must have permission before testing any system.', 'Recognise a phishing message and know how to report it.'],
  'handson': 'Audit your own accounts: unique passwords in a password manager, MFA on email, check haveibeenpwned.com for your email.',
 },

 # ───────────────────────── BUSINESS ANALYSIS ─────────────────────────
 ('business-analysis', 'problem-framing'): {
  'videos': [
   V('What is business analysis? / Problem statement for BAs', 'YouTube search', 'Look for an overview with stakeholders, problem statement and success measures.', q='business analysis problem statement stakeholders success measures beginner'),
   V('How to define a problem (5 Whys)', 'YouTube search', 'Short video on 5 Whys and root-cause thinking.', mode='Hands-on', q='5 Whys root cause analysis explained example'),
  ],
  'articles': [
   A('Business analysis guide', 'Atlassian', 'https://www.atlassian.com/agile/business-analysis', 'Requirements, stakeholders and workflows.'),
  ],
  'mastery': ['Name the stakeholder, problem, constraint and success measure for a case.', 'Rewrite "sales are low" into an answerable question.', 'Explain what data you would need and why.'],
  'handson': 'Choose a college problem (long canteen queue). Write stakeholder, problem statement, 3 constraints and one success metric.',
 },
 ('business-analysis', 'process-mapping'): {
  'videos': [
   V('Introduction to Process Mapping', 'Process mapping tutorial', 'Short introduction to boxes, decisions and swimlanes.', q='Introduction to Process Mapping beginners flowchart swimlane'),
   V('Process Mapping for Business Analysts', 'YouTube search', 'Walkthrough with a real example and common symbols.', mode='Hands-on', q='Process Mapping for Business Analysts get started with process mapping'),
  ],
  'articles': [
   A('Process mapping guide and symbols', 'Lucidchart', 'https://lucid.co/lucidchart/tutorial/process-mapping-guide-and-symbols', 'Symbols and steps to build a clear map.'),
   A('Draw.io (diagrams.net) – free tool', 'diagrams.net', 'https://www.diagrams.net/', 'Free tool to draw your first process map.'),
  ],
  'mastery': ['Use start/end, process, decision and arrow symbols correctly.', 'Identify one bottleneck or duplicate step in a flow.', 'Show handoffs between people or teams.'],
  'handson': 'Draw the "assignment submission" flow in diagrams.net with at least one decision and one handoff; mark the slowest step.',
 },
 ('business-analysis', 'presenting-insights'): {
  'videos': [
   V('Storytelling with data', 'Cole Nussbaumer Knaflic (Talks at Google)', 'Search for the talk on clear, audience-focused data presentation.', q='storytelling with data Cole Nussbaumer Knaflic talk'),
   V('How to present data to non-technical people', 'YouTube search', 'Short practical tips for summaries and recommendations.', mode='Hands-on', q='how to present data insights to non technical stakeholders recommendation'),
  ],
  'articles': [
   A('Storytelling with Data – blog', 'Storytelling with Data', 'https://www.storytellingwithdata.com/blog', 'Examples of before/after charts and clear messages.'),
   A('Google Technical Writing One', 'Google for Developers', 'https://developers.google.com/tech-writing/one', 'Free lessons on clear, concise explanations.'),
  ],
  'mastery': ['Write a 3-sentence finding → evidence → next action summary.', 'State at least one limitation honestly.', 'Choose a chart that supports (not decorates) the message.'],
  'handson': 'Use your Excel expense data and write a 3-sentence recommendation plus one chart; ask a friend to repeat the key message in 10 seconds.',
 },

 # ───────────────────────── CORE ENGINEERING ─────────────────────────
 ('core-engineering', 'engineering-problems'): {
  'videos': [
   V('The Engineering Design Process', 'NASA / TryEngineering', 'Search for the engineering design process: ask, imagine, plan, create, improve.', q='engineering design process explained steps ask imagine plan create improve'),
   V('Requirements and constraints in engineering', 'YouTube search', 'Short overview of defining requirements, constraints and success criteria.', mode='Hands-on', q='engineering requirements and constraints explained beginners'),
  ],
  'articles': [
   A('Engineering design process', 'Wikipedia', 'https://en.wikipedia.org/wiki/Engineering_design_process', 'Overview of the typical stages and terminology.'),
   A('NPTEL engineering courses', 'NPTEL', 'https://nptel.ac.in/courses', 'Free university-level lectures by IIT/IISc faculty.'),
  ],
  'mastery': ['List user, requirements and constraints for a problem.', 'Separate "must have" from "nice to have".', 'Explain how you will test whether the solution works.'],
  'handson': 'Define a low-cost water-level alert: user, 5 requirements, 3 constraints (cost, safety, time), and 1 test.',
 },
 ('core-engineering', 'measurements'): {
  'videos': [
   V('Measurement, units and significant figures', 'Khan Academy / Physics Wallah', 'Search for a clear lesson on units, significant figures and uncertainty.', q='measurement units significant figures uncertainty physics lesson'),
   V('Accuracy vs precision and errors in measurement', 'YouTube search', 'Short explanation with examples; helpful for lab practicals.', mode='Hands-on', q='accuracy vs precision measurement error explained'),
  ],
  'articles': [
   A('Uncertainty of measurement results', 'NIST', 'https://physics.nist.gov/cuu/Uncertainty/index.html', 'Authoritative reference for expressing uncertainty.'),
   A('MIT OpenCourseWare', 'MIT OCW', 'https://ocw.mit.edu/', 'Free lab and engineering materials.'),
  ],
  'mastery': ['Always write units with values.', 'Repeat measurements and compute mean and range.', 'Explain accuracy vs precision.'],
  'handson': 'Measure a pen 5 times with a ruler (cm and mm). Table the values, compute mean and range, note the ruler’s smallest division.',
 },
 ('core-engineering', 'technical-documentation'): {
  'videos': [
   V('Technical writing for engineers', 'Google Technical Writing / Search', 'Search for a short intro on goal, method, results and limitations.', q='technical writing for engineers introduction report structure'),
   V('How to write a lab report', 'YouTube search', 'Walkthrough of title, objective, procedure, observations, conclusion.', mode='Hands-on', q='how to write a lab report engineering students'),
  ],
  'articles': [
   A('Technical Writing One', 'Google for Developers', 'https://developers.google.com/tech-writing/one', 'Free course on clear technical sentences, lists and paragraphs.'),
   A('Technical Writing Two', 'Google for Developers', 'https://developers.google.com/tech-writing/two', 'Editing, organising documents and drafting.'),
  ],
  'mastery': ['Write a procedure someone else can repeat without asking you.', 'Label diagrams and include units.', 'State limitations and next improvements honestly.'],
  'handson': 'Write a one-page procedure for your measurement activity; give it to a friend and see if they get the same result.',
 },
}

# Track-level "if you want one full path" suggestions (single playlist/course per track)
TRACK_MASTERY = {
 'web-foundations': [
  V('Learn HTML & CSS – Full Course for Beginners', 'freeCodeCamp.org', 'One long course that gets you from zero to a finished page.', mode='Hands-on', vid='a_iQb1lnAEQ'),
  V('Web Development with HTML & CSS – Full Course for Beginners', 'freeCodeCamp.org', 'Second project-based course for revision and more practice.', mode='Hands-on', vid='dX8396ZmSPk'),
 ],
 'python-starter': [
  V('Harvard CS50P – Introduction to Programming with Python', 'freeCodeCamp.org', 'Best full-course path in English for concepts + problem sets.', vid='nLRL_NcnK-4'),
  V('Python for Beginners (Full Course) #100DaysOfCode', 'CodeWithHarry', 'Hindi playlist for daily practice.', lang='Hindi', mode='Hands-on', pl='PLu0W_9lII9agwh1XjRt242xIpHhPT2llg'),
 ],
 'cybersecurity': [
  V('Introduction to Linux – Full Course for Beginners', 'freeCodeCamp.org', 'Strong foundation for every security role.', mode='Hands-on', vid='sWbUDq4S6Y8'),
 ],
 'data-analytics': [
  V('Excel formulas you need to master as a beginner', 'SimonSezIT', 'Quick start for the spreadsheet lessons.', mode='Hands-on', vid='vgEKAVWWyRo'),
 ],
}


def get_lesson_resources(track_id, slug):
    return LESSON_RESOURCES.get((track_id, slug))


def get_track_resources(track_id):
    return TRACK_MASTERY.get(track_id, [])
