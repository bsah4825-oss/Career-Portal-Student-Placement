"""CAREERVERSE student transformation modules.
This module extends the existing Flask + SQLite application without replacing
its authentication, user table, profile, skills, DSA, certificates, internships,
or Recruitment Intelligence Lab.
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime
import json, os, re, logging
from lesson_resources import get_lesson_resources, get_track_resources, LESSON_RESOURCES
from personalize import build_personal_resources, ai_refine, recommend_for_prompt, visible_videos
from topic_resources import TOPICS, match_topics


cv = Blueprint('careerverse', __name__, url_prefix='/careerverse')

TRACKS = {
    'web-foundations': {
        'title': 'Web Development Foundations', 'category': 'Technology', 'level': 'Beginner',
        'description': 'Build your first web pages from zero using HTML and CSS.',
        'outcomes': ['Structure a page with semantic HTML', 'Style responsive layouts with CSS', 'Build and explain a small personal webpage'],
        'lessons': [
            {'slug':'how-the-web-works','title':'How the Web Works','minutes':15,'body':[
                ('Understand','A website is made of files that a browser reads. HTML describes the content, CSS controls its appearance, and JavaScript adds behaviour.'),
                ('Example','A heading is content: <h1>My first page</h1>. A CSS rule can make it blue: h1 { color: blue; }.'),
                ('Try it','Create a folder named my-first-site. Inside it create index.html. Add a heading, a paragraph and your name.')], 'task':'In your own words, explain the difference between HTML and CSS. Then write one HTML heading and one paragraph.'},
            {'slug':'html-structure','title':'HTML Page Structure','minutes':25,'body':[
                ('Understand','HTML elements use tags. A basic page has doctype, html, head and body. Put page metadata in head and visible content in body.'),
                ('Example','Use <h1> for the main heading, <p> for a paragraph, <a href="https://example.com"> for a link, and <img src="photo.jpg" alt="Description"> for an image.'),
                ('Try it','Create a page with a title, About section, three interests and one link. Use meaningful heading order.')], 'task':'Submit the HTML structure for a personal introduction page and explain what the head and body contain.'},
            {'slug':'css-basics','title':'CSS: Make It Look Good','minutes':25,'body':[
                ('Understand','CSS selects HTML elements and applies visual rules. You can use element selectors, class selectors and IDs. Prefer reusable classes.'),
                ('Example','A class selector looks like .card { padding: 20px; border-radius: 12px; }. Add class="card" to an HTML element.'),
                ('Try it','Add a stylesheet, choose readable fonts, spacing and colours, and create a simple card for your profile.')], 'task':'Write a CSS class named .profile-card with padding, a border and rounded corners. Explain what each property does.'},
            {'slug':'responsive-project','title':'Responsive Design & First Project','minutes':35,'body':[
                ('Understand','Responsive design adapts a page to different screen widths. Use flexible widths and media queries instead of fixed desktop-only layouts.'),
                ('Example','@media (max-width: 600px) { .columns { grid-template-columns: 1fr; } }'),
                ('Try it','Build a one-page student portfolio with About, Skills, Projects and Contact sections. Test it at mobile width.')], 'task':'Describe how you would make a two-column layout become one column on a phone. Include a media query.'}
        ]
    },
    'python-starter': {
        'title':'Python Programming: Start from Zero','category':'Technology','level':'Beginner',
        'description':'Learn programming logic, variables, conditions and loops with small exercises.',
        'outcomes':['Use variables and data types','Write conditions and loops','Solve beginner problems and explain the logic'],
        'lessons':[
            {'slug':'first-program','title':'Your First Program','minutes':20,'body':[('Understand','A program is a sequence of instructions. Python is a readable programming language often used for automation, data and web applications.'),('Example','print("Hello, world!") displays text. A variable stores a value: name = "Asha".'),('Try it','Run a program that prints your name, degree and one learning goal.')],'task':'Write a Python program that stores your name in a variable and prints a welcome message.'},
            {'slug':'variables-types','title':'Variables & Data Types','minutes':25,'body':[('Understand','Variables refer to values. Common types include int, float, str and bool. Use type(value) to inspect a value.'),('Example','age = 19; cgpa = 8.4; name = "Ravi"; is_student = True.'),('Try it','Store a product name, price and availability, then print each value.')],'task':'Create four variables with int, float, string and boolean values. State their types.'},
            {'slug':'conditions','title':'Decision Making with if','minutes':25,'body':[('Understand','if, elif and else let a program choose which instructions to run based on a condition.'),('Example','if marks >= 50: print("Pass") else: print("Try again")'),('Try it','Write a program that checks whether a number is positive, negative or zero.')],'task':'Write an if/elif/else program that classifies a mark as Distinction, Pass or Needs Improvement.'},
            {'slug':'loops','title':'Loops & Repetition','minutes':30,'body':[('Understand','A for loop repeats over a sequence. A while loop repeats while a condition remains true. Avoid infinite loops.'),('Example','for number in range(1, 6): print(number)'),('Try it','Print numbers from 1 to 10 and calculate their sum.')],'task':'Write a loop that calculates the sum of numbers from 1 to 20 and explain how it works.'}
        ]
    },
    'career-digital': {
        'title':'Digital & Professional Foundations','category':'All disciplines','level':'Beginner',
        'description':'Build practical digital confidence, communication and problem-solving habits for any degree.',
        'outcomes':['Organise files and use common productivity tools','Communicate work clearly','Break a practical problem into manageable steps'],
        'lessons':[
            {'slug':'digital-basics','title':'Digital Skills & File Organisation','minutes':20,'body':[('Understand','Digital confidence includes managing files, using search effectively, protecting accounts and understanding common file types.'),('Example','Use clear folder names, meaningful filenames and regular backups. Never share passwords or one-time codes.'),('Try it','Create a folder structure for notes, assignments, projects and certificates.')],'task':'Describe a safe folder and backup system for your college work.'},
            {'slug':'communication','title':'Clear Communication','minutes':20,'body':[('Understand','Professional communication is clear, respectful and specific. State the context, action needed and deadline.'),('Example','Instead of “I have a problem”, write “The login page returns an error after registration. Could you help me check the database connection?”'),('Try it','Write a short message asking a teammate for a code review.')],'task':'Write a concise project update with progress, blocker and next step.'},
            {'slug':'problem-solving','title':'Problem Solving','minutes':25,'body':[('Understand','Define the problem, gather evidence, identify possible causes, test one change at a time and record the result.'),('Example','If a page is blank, inspect the terminal error, browser console, route and template name rather than changing unrelated files.'),('Try it','Choose a small problem from college and break it into three actionable steps.')],'task':'Describe one real problem using: problem, evidence, possible cause, test and result.'}
        ]
    },
    'data-analytics': {
        'title':'Data Analytics Foundations','category':'Data & Business','level':'Beginner',
        'description':'Start with spreadsheets, data quality, basic statistics and clear visual explanations.',
        'outcomes':['Organise and clean a small dataset','Understand averages and variation','Explain a simple chart without overstating conclusions'],
        'lessons':[
            {'slug':'data-thinking','title':'Thinking with Data','minutes':20,'body':[('Understand','Data analysis begins with a clear question. Check where data came from, what each column means and whether important values are missing.'),('Example','A table of attendance percentages can describe a class, but it does not by itself explain why someone was absent.'),('Try it','Choose a question that could be answered with a small, responsibly collected dataset.')],'task':'Write one analysis question and list three data fields that could help answer it.'},
            {'slug':'spreadsheet-basics','title':'Spreadsheet Formulas','minutes':25,'body':[('Understand','Spreadsheets organise information in rows and columns. Formulas calculate values; functions such as SUM, AVERAGE and COUNT help summarise data.'),('Example','=AVERAGE(B2:B11) calculates the mean of values in cells B2 through B11.'),('Try it','Create a small table of five expenses and calculate the total and average.')],'task':'Explain the difference between SUM and AVERAGE and give one situation where each is useful.'},
            {'slug':'charts-statistics','title':'Statistics & Visualisation','minutes':30,'body':[('Understand','Mean, median and range summarise different aspects of data. Select charts based on the question and avoid misleading scales.'),('Example','A bar chart compares categories. A line chart can show change over time.'),('Try it','Create a chart from a small dataset and write two observations plus one limitation.')],'task':'Describe why a chart can show association without proving that one factor caused another.'}
        ]
    },
    'cybersecurity': {
        'title':'Cybersecurity Foundations','category':'Technology','level':'Beginner',
        'description':'Understand networks, operating-system basics and safe, ethical security practice.',
        'outcomes':['Explain basic network concepts','Understand files, users and permissions','Recognise common security risks and safe responses'],
        'lessons':[
            {'slug':'network-basics','title':'How Networks Work','minutes':25,'body':[('Understand','A network connects devices so they can exchange data. IP addresses identify network interfaces; DNS helps translate domain names into addresses.'),('Example','When you open a website, your device uses DNS and network protocols to contact a server.'),('Try it','Draw a simple diagram showing your device, router, internet and a website server.')],'task':'Explain the roles of an IP address and DNS in your own words.'},
            {'slug':'linux-basics','title':'Operating Systems & Linux Basics','minutes':25,'body':[('Understand','An operating system manages processes, memory, files, devices and users. Linux command-line tools can inspect and manage files.'),('Example','pwd shows the current directory; ls lists files; cd changes directories. Only run commands you understand.'),('Try it','Practise navigating a local folder and listing its files.')],'task':'Describe what pwd, ls and cd do. Explain why file permissions matter.'},
            {'slug':'security-ethics','title':'Security, Privacy & Ethics','minutes':25,'body':[('Understand','Security work must be authorised. Protect accounts with unique passwords and multi-factor authentication; keep systems updated and report suspicious activity.'),('Example','Only test systems you own or have explicit permission to assess. Never attempt to access another person’s account.'),('Try it','Create a checklist for securing a personal laptop and email account.')],'task':'Explain why written permission and scope are essential before any security test.'}
        ]
    },
    'business-analysis': {
        'title':'Business & Professional Analytics','category':'Business','level':'Beginner',
        'description':'Practise business problem framing, spreadsheet thinking and communicating recommendations.',
        'outcomes':['Describe a business problem clearly','Summarise simple operational data','Present a recommendation with evidence and limitations'],
        'lessons':[
            {'slug':'problem-framing','title':'Understand the Business Problem','minutes':20,'body':[('Understand','A useful analysis begins with a decision someone needs to make. Identify the stakeholder, problem, constraints and success measure.'),('Example','Instead of “sales are low”, ask “Which product categories changed most this month, and what evidence could explain the change?”'),('Try it','Choose a campus or community service and define one problem it could improve.')],'task':'Write a problem statement, stakeholder and one measurable success indicator.'},
            {'slug':'process-mapping','title':'Process Mapping','minutes':25,'body':[('Understand','A process map shows the steps, decisions and handoffs involved in a task. It can reveal delays or duplicated work.'),('Example','A simple assignment submission flow may include prepare file, upload, confirmation and review.'),('Try it','Map a familiar process with five steps and identify one possible bottleneck.')],'task':'Describe a process improvement and explain how you would measure whether it helped.'},
            {'slug':'presenting-insights','title':'Presenting Evidence','minutes':25,'body':[('Understand','A clear recommendation states the finding, supporting evidence, uncertainty and next action.'),('Example','“Average queue time fell from 12 to 9 minutes in this sample. We should collect another week of data before making a permanent change.”'),('Try it','Prepare a three-sentence summary of a small finding.')],'task':'Write a recommendation that includes evidence and one limitation.'}
        ]
    },
    'core-engineering': {
        'title':'Core Engineering & Applied Problem Solving','category':'Engineering','level':'Beginner',
        'description':'A cross-discipline start for engineering students: measurement, documentation and practical investigation.',
        'outcomes':['Define an engineering problem and constraints','Record observations and measurements','Document a repeatable practical test'],
        'lessons':[
            {'slug':'engineering-problems','title':'Frame an Engineering Problem','minutes':20,'body':[('Understand','Engineering starts with a need, requirements and constraints such as safety, cost, materials, time and environment.'),('Example','A low-cost water-level alert must detect a level, communicate clearly and operate safely.'),('Try it','Choose a small problem and list its user, requirements and constraints.')],'task':'Write a problem statement with at least three measurable requirements.'},
            {'slug':'measurements','title':'Measurement & Data Recording','minutes':25,'body':[('Understand','Measurements need units, context and repeatable methods. Record observations honestly and note uncertainty.'),('Example','Write 12.4 cm, not just 12.4. Repeat a measurement and compare results.'),('Try it','Record five measurements of a safe everyday object and calculate the average.')],'task':'Explain why units and repeated measurements matter in an experiment.'},
            {'slug':'technical-documentation','title':'Technical Documentation','minutes':25,'body':[('Understand','Good documentation helps another person understand the goal, setup, method, results and limitations of your work.'),('Example','A practical report includes a labelled diagram, tools, procedure, observations and conclusion.'),('Try it','Write a short procedure that another student could repeat safely.')],'task':'List the sections you would include in a practical project report and why.'}
        ]
    }
}


# Curated free/low-cost learning resources. Links point to maintained official
# documentation, open courses or reputable educational channels. Availability can change.
LEARNING_RESOURCES = {
 'web-foundations': [
  {'title':'MDN Learn Web Development','kind':'Guided articles + practice','level':'Beginner → intermediate','url':'https://developer.mozilla.org/en-US/docs/Learn_web_development','why':'A structured, free curriculum covering HTML, CSS, JavaScript, accessibility and practical challenges.'},
  {'title':'freeCodeCamp – Responsive Web Design','kind':'Video course + projects','level':'Beginner','url':'https://www.freecodecamp.org/learn/2022/responsive-web-design/','why':'Hands-on lessons and projects that make you build instead of only watch.'},
  {'title':'The Odin Project – Foundations','kind':'Project-based curriculum','level':'Beginner','url':'https://www.theodinproject.com/paths/foundations/courses/foundations','why':'A practical path covering developer tools, Git, HTML, CSS and JavaScript.'},
  {'title':'JavaScript.info','kind':'Detailed articles','level':'Beginner → advanced','url':'https://javascript.info/','why':'Deep explanations and examples for modern JavaScript.'},
  {'title':'Web.dev Learn Accessibility','kind':'Professional guide','level':'All levels','url':'https://web.dev/learn/accessibility/','why':'Learn to build interfaces that work for people with different access needs.'}
 ],
 'python-starter': [
  {'title':'Harvard CS50P – Introduction to Programming with Python','kind':'Full video course + exercises','level':'Beginner','url':'https://cs50.harvard.edu/python/','why':'A complete beginner-friendly course with lectures, problem sets and practical work.'},
  {'title':'Official Python Tutorial','kind':'Documentation + examples','level':'Beginner','url':'https://docs.python.org/3/tutorial/','why':'The authoritative reference for Python syntax and core language concepts.'},
  {'title':'Automate the Boring Stuff with Python','kind':'Free online book','level':'Beginner','url':'https://automatetheboringstuff.com/','why':'Practical automation examples that connect programming to everyday tasks.'},
  {'title':'freeCodeCamp Python Full Course','kind':'Video course','level':'Beginner','url':'https://www.youtube.com/results?search_query=freeCodeCamp+Python+full+course','why':'Long-form video lessons to reinforce concepts alongside coding practice.'},
  {'title':'Exercism Python Track','kind':'Practice + mentor feedback','level':'Beginner → intermediate','url':'https://exercism.org/tracks/python','why':'Short exercises with feedback and opportunities to improve code quality.'}
 ],
 'data-analytics': [
  {'title':'Kaggle Learn','kind':'Interactive micro-courses','level':'Beginner','url':'https://www.kaggle.com/learn','why':'Hands-on introductions to Python, Pandas, data visualisation, SQL and machine learning.'},
  {'title':'SQLBolt','kind':'Interactive SQL lessons','level':'Beginner','url':'https://sqlbolt.com/','why':'Learn SQL by writing queries in the browser.'},
  {'title':'Microsoft Learn – Power BI','kind':'Official guided learning','level':'Beginner → intermediate','url':'https://learn.microsoft.com/training/powerplatform/power-bi/','why':'Official learning paths for connecting, cleaning, modelling and visualising data.'},
  {'title':'Pandas Getting Started','kind':'Official documentation','level':'Beginner → intermediate','url':'https://pandas.pydata.org/docs/getting_started/index.html','why':'Learn the core data manipulation library used in Python analytics.'},
  {'title':'StatQuest – Statistics & Machine Learning','kind':'Video lessons','level':'Beginner → advanced','url':'https://www.youtube.com/@statquest','why':'Clear visual explanations of statistics and machine-learning ideas.'}
 ],
 'ai-ml': [
  {'title':'Google Machine Learning Crash Course','kind':'Interactive course + videos','level':'Beginner → intermediate','url':'https://developers.google.com/machine-learning/crash-course','why':'Practical ML foundations with visual explanations and exercises.'},
  {'title':'Kaggle Learn – Intro to Machine Learning','kind':'Interactive course','level':'Beginner','url':'https://www.kaggle.com/learn/intro-to-machine-learning','why':'Build and evaluate your first predictive models in notebook exercises.'},
  {'title':'Harvard CS50P','kind':'Full video course + exercises','level':'Beginner','url':'https://cs50.harvard.edu/python/','why':'Build the Python foundation needed before serious ML work.'},
  {'title':'Scikit-learn User Guide','kind':'Official documentation','level':'Intermediate','url':'https://scikit-learn.org/stable/user_guide.html','why':'Learn model selection, preprocessing, pipelines and evaluation using a widely used ML library.'},
  {'title':'3Blue1Brown – Neural Networks','kind':'Visual video series','level':'Beginner → intermediate','url':'https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr','why':'Build intuition for neural networks and the mathematics behind them.'}
 ],
 'cybersecurity': [
  {'title':'Cisco Networking Academy','kind':'Free courses','level':'Beginner','url':'https://www.netacad.com/','why':'Free self-paced introductions to networking and cybersecurity.'},
  {'title':'PortSwigger Web Security Academy','kind':'Guided labs','level':'Beginner → advanced','url':'https://portswigger.net/web-security','why':'Free, interactive web security lessons and legal practice labs.'},
  {'title':'OWASP Top 10','kind':'Security reference','level':'Beginner → intermediate','url':'https://owasp.org/www-project-top-ten/','why':'Understand common web application security risks and defensive practices.'},
  {'title':'OverTheWire: Bandit','kind':'Hands-on Linux game','level':'Beginner','url':'https://overthewire.org/wargames/bandit/','why':'Practise Linux command-line fundamentals in a safe learning environment.'},
  {'title':'Professor Messer – Security+ videos','kind':'Video lessons','level':'Beginner → intermediate','url':'https://www.youtube.com/@professormesser','why':'Structured security and networking explanations for foundational study.'}
 ],
 'business-analysis': [
  {'title':'Microsoft Learn – Power BI','kind':'Guided learning','level':'Beginner → intermediate','url':'https://learn.microsoft.com/training/powerplatform/power-bi/','why':'Build data preparation, modelling and dashboard skills.'},
  {'title':'Excel Training – Microsoft Support','kind':'Official tutorials','level':'Beginner','url':'https://support.microsoft.com/excel','why':'Learn spreadsheet formulas, tables, charts and practical workflows.'},
  {'title':'SQLBolt','kind':'Interactive SQL lessons','level':'Beginner','url':'https://sqlbolt.com/','why':'Practise the SQL querying used in many analyst roles.'},
  {'title':'Atlassian – Business Analysis','kind':'Articles and guides','level':'Beginner → intermediate','url':'https://www.atlassian.com/agile/business-analysis','why':'Understand requirements, stakeholders, workflows and business problem framing.'},
  {'title':'Google Technical Writing Courses','kind':'Free writing courses','level':'All levels','url':'https://developers.google.com/tech-writing','why':'Improve clear technical explanations, documentation and professional communication.'}
 ],
 'core-engineering': [
  {'title':'NPTEL Courses','kind':'University video courses','level':'Beginner → advanced','url':'https://nptel.ac.in/courses','why':'Broad engineering and science courses taught by Indian academic institutions; course access is free, while optional certification exams may cost money.'},
  {'title':'MIT OpenCourseWare','kind':'Open university courses','level':'Beginner → advanced','url':'https://ocw.mit.edu/','why':'Free lecture notes, assignments and learning materials across engineering and science.'},
  {'title':'OpenStax','kind':'Free textbooks','level':'Beginner','url':'https://openstax.org/subjects/science','why':'Peer-reviewed, openly available foundational science textbooks.'},
  {'title':'Google Technical Writing','kind':'Free articles + exercises','level':'All levels','url':'https://developers.google.com/tech-writing','why':'Build documentation and technical communication skills valuable in every engineering discipline.'},
  {'title':'Autodesk Education','kind':'Design software learning','level':'Beginner → intermediate','url':'https://www.autodesk.com/education/edu-software/overview','why':'Explore education access and learning for engineering design tools; eligibility and product terms apply.'}
 ],
 'arts-humanities': [
  {'title':'MIT OpenCourseWare – Humanities','kind':'Open university courses','level':'Beginner → advanced','url':'https://ocw.mit.edu/','why':'Free course materials across history, literature, philosophy, languages and social sciences.'},
  {'title':'OpenStax – Social Sciences','kind':'Free textbooks','level':'Beginner','url':'https://openstax.org/subjects/social-sciences','why':'Open textbooks for introductory social science study.'},
  {'title':'Zotero – Research Skills','kind':'Free tool + guides','level':'Beginner → intermediate','url':'https://www.zotero.org/support/','why':'Organise references and build a reliable academic research workflow.'},
  {'title':'Google Scholar','kind':'Research discovery','level':'All levels','url':'https://scholar.google.com/','why':'Find scholarly literature and learn to trace sources; always evaluate quality and context.'},
  {'title':'Google Technical Writing','kind':'Free writing lessons','level':'All levels','url':'https://developers.google.com/tech-writing','why':'Improve clear writing, structured explanations and documentation.'}
 ],
 'health-life-sciences': [
  {'title':'OpenWHO','kind':'Free learning courses','level':'Beginner → advanced','url':'https://openwho.org/','why':'Open learning materials on public health and health-related topics; follow current course guidance.'},
  {'title':'NCBI Bookshelf','kind':'Free academic books','level':'Beginner → advanced','url':'https://www.ncbi.nlm.nih.gov/books/','why':'Access biomedical and life-science books and reference material.'},
  {'title':'Khan Academy – Biology','kind':'Video lessons + practice','level':'Beginner','url':'https://www.khanacademy.org/science/biology','why':'Build foundational biology understanding with explanations and exercises.'},
  {'title':'MIT OpenCourseWare – Biology','kind':'Open university courses','level':'Beginner → advanced','url':'https://ocw.mit.edu/search/?d=Biology','why':'Explore university-level life-science course materials.'},
  {'title':'Google Scholar','kind':'Research discovery','level':'All levels','url':'https://scholar.google.com/','why':'Find research literature and practise evaluating evidence and publication context.'}
 ],
 'design-creative': [
  {'title':'Figma Learn','kind':'Guided tutorials','level':'Beginner → intermediate','url':'https://www.figma.com/resource-library/','why':'Learn interface design, prototyping and collaborative design workflows.'},
  {'title':'Canva Design School','kind':'Free design lessons','level':'Beginner','url':'https://www.canva.com/designschool/','why':'Learn visual communication, layout and design fundamentals.'},
  {'title':'Material Design','kind':'Design system documentation','level':'Intermediate','url':'https://m3.material.io/','why':'Study components, interaction patterns and accessible interface principles.'},
  {'title':'Web.dev – Accessibility','kind':'Professional guide','level':'All levels','url':'https://web.dev/learn/accessibility/','why':'Understand inclusive design and accessible digital products.'},
  {'title':'Adobe Learn','kind':'Video tutorials','level':'Beginner → advanced','url':'https://www.adobe.com/learn','why':'Explore creative software tutorials and practical workflows.'}
 ],
 'career-digital': [
  {'title':'Harvard CS50x','kind':'Full video course + problem sets','level':'Beginner','url':'https://cs50.harvard.edu/x/','why':'A rigorous introduction to computer science and problem solving for students from any background.'},
  {'title':'GCFGlobal – Computer Basics','kind':'Free lessons','level':'Beginner','url':'https://edu.gcfglobal.org/en/computerbasics/','why':'Build confidence with computers, files, internet and common digital tasks.'},
  {'title':'Google Applied Digital Skills','kind':'Practical video lessons','level':'Beginner','url':'https://applieddigitalskills.withgoogle.com/','why':'Project-based digital productivity and workplace skills.'},
  {'title':'Google Technical Writing','kind':'Free course','level':'All levels','url':'https://developers.google.com/tech-writing','why':'Practise clear, concise professional and technical writing.'},
  {'title':'freeCodeCamp','kind':'Free video courses + projects','level':'Beginner → advanced','url':'https://www.freecodecamp.org/learn/','why':'A large library of free, project-oriented learning paths.'}
 ]
}

ROLE_RESOURCE_MAP = {
 'Frontend Developer':'web-foundations', 'Software Developer':'python-starter',
 'Data Analyst':'data-analytics', 'Data Scientist / AI-ML':'ai-ml',
 'Cybersecurity Analyst':'cybersecurity', 'Business Analyst':'business-analysis',
 'Core Engineering / Other':'core-engineering',
 'Arts, Humanities & Social Sciences':'arts-humanities',
 'Health & Life Sciences':'health-life-sciences',
 'Design & Creative Industries':'design-creative',
 'General Professional / Any Degree':'career-digital'
}

DIAGNOSTIC = [
    {'q':'Have you written a program before?','opts':['Never','A little (basic print/variables)','I can write small programs','I can build projects'], 'skill':'programming','correct':None},
    {'q':'What does a variable do in programming?','opts':['Stores a value','Deletes a file','Connects to Wi-Fi','Draws an image'],'skill':'programming','correct':0},
    {'q':'Which HTML tag is commonly used for the main heading?','opts':['<p>','<h1>','<img>','<table>'],'skill':'web','correct':1},
    {'q':'What is CSS mainly used for?','opts':['Database storage','Styling web pages','Sending emails','Operating systems'],'skill':'web','correct':1},
    {'q':'What does SQL help you do?','opts':['Query relational databases','Edit photos','Compile Java','Design slides'],'skill':'data','correct':0},
    {'q':'Which is a spreadsheet skill?','opts':['Using formulas to calculate totals','Writing a device driver','Training a neural network','Configuring a router'],'skill':'digital','correct':0},
    {'q':'A project has a bug. What is a sensible first step?','opts':['Delete the whole project','Reproduce the issue and inspect the error','Change random files','Ignore it'],'skill':'problem_solving','correct':1},
    {'q':'What does Git help developers do?','opts':['Track changes in files','Increase internet speed','Create passwords','Design logos'],'skill':'software_tools','correct':0},
    {'q':'Which statement about data is most accurate?','opts':['Data never contains errors','Data should be checked before drawing conclusions','More data always means better results','Charts prove causation'],'skill':'data','correct':1},
    {'q':'How comfortable are you explaining your work to another person?','opts':['Not comfortable yet','A little comfortable','Mostly comfortable','Very comfortable'],'skill':'communication','correct':None}
]

ROLES = {
 'Software Developer': {'skills':['Programming fundamentals','Data structures & algorithms','Git & GitHub','OOP and software design','Database / SQL','Testing and debugging','Projects and communication'], 'tracks':['python-starter','web-foundations']},
 'Frontend Developer': {'skills':['HTML','CSS and responsive design','JavaScript','Git & GitHub','React or another UI framework','Accessibility','Portfolio project'], 'tracks':['web-foundations']},
 'Data Analyst': {'skills':['Spreadsheets','SQL','Statistics','Python or R','Data visualisation','Communication','Case studies'], 'tracks':['data-analytics','python-starter']},
 'Data Scientist / AI-ML': {'skills':['Python','Statistics and probability','SQL','Data analysis','Machine learning','Model evaluation','Responsible AI projects'], 'tracks':['python-starter']},
 'Cybersecurity Analyst': {'skills':['Networking','Linux','Security fundamentals','Scripting','Threat analysis','Ethical practice','Lab evidence'], 'tracks':['cybersecurity','python-starter']},
 'Business Analyst': {'skills':['Communication','Spreadsheets','Process analysis','SQL basics','Requirements writing','Presentation','Case studies'], 'tracks':['business-analysis','data-analytics']},
 'Core Engineering / Other': {'skills':['Discipline fundamentals','Digital tools','Problem solving','Technical communication','Practical project','Documentation'], 'tracks':['core-engineering','career-digital']},
 'Arts, Humanities & Social Sciences': {'skills':['Research and source evaluation','Writing and communication','Digital research tools','Data literacy','Critical thinking','Portfolio or field project'], 'tracks':['career-digital','business-analysis']},
 'Health & Life Sciences': {'skills':['Discipline fundamentals','Evidence evaluation','Data literacy','Ethics and privacy','Research documentation','Practical or lab experience'], 'tracks':['career-digital','data-analytics']},
 'Design & Creative Industries': {'skills':['Design fundamentals','Creative software','User research','Portfolio development','Accessibility','Client communication'], 'tracks':['web-foundations','career-digital']},
 'General Professional / Any Degree': {'skills':['Digital fluency','Communication','Problem solving','Research and source evaluation','Project planning','Career portfolio'], 'tracks':['career-digital','business-analysis']}
}


def init_careerverse_db(get_db):
    conn=get_db()
    statements=[
    '''CREATE TABLE IF NOT EXISTS cv_profiles (user_id INTEGER PRIMARY KEY, degree TEXT DEFAULT '', branch TEXT DEFAULT '', study_year TEXT DEFAULT '', graduation_year TEXT DEFAULT '', interests TEXT DEFAULT '', career_target TEXT DEFAULT '', hours_per_day TEXT DEFAULT '1', preferred_language TEXT DEFAULT 'English', experience_level TEXT DEFAULT 'beginner', device_access TEXT DEFAULT 'laptop', updated_at TEXT DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(user_id) REFERENCES users(id))''',
    '''CREATE TABLE IF NOT EXISTS cv_diagnostics (id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER NOT NULL,answers_json TEXT NOT NULL,scores_json TEXT NOT NULL,created_at TEXT DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY(user_id) REFERENCES users(id))''',
    '''CREATE TABLE IF NOT EXISTS cv_lesson_progress (id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER NOT NULL,track_id TEXT NOT NULL,lesson_slug TEXT NOT NULL,status TEXT DEFAULT 'completed',reflection TEXT DEFAULT '',completed_at TEXT DEFAULT CURRENT_TIMESTAMP,UNIQUE(user_id,track_id,lesson_slug),FOREIGN KEY(user_id) REFERENCES users(id))''',
    '''CREATE TABLE IF NOT EXISTS cv_projects (id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER NOT NULL,title TEXT NOT NULL,track_id TEXT DEFAULT '',description TEXT DEFAULT '',repo_url TEXT DEFAULT '',demo_url TEXT DEFAULT '',reflection TEXT DEFAULT '',status TEXT DEFAULT 'started',created_at TEXT DEFAULT CURRENT_TIMESTAMP,updated_at TEXT DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY(user_id) REFERENCES users(id))''',
    '''CREATE TABLE IF NOT EXISTS cv_skill_evidence (id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER NOT NULL,skill_name TEXT NOT NULL,evidence_type TEXT NOT NULL,evidence_url TEXT DEFAULT '',explanation TEXT DEFAULT '',review_status TEXT DEFAULT 'self-reported',created_at TEXT DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY(user_id) REFERENCES users(id))''',
    '''CREATE TABLE IF NOT EXISTS cv_tutor_sessions (id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER NOT NULL,mode TEXT NOT NULL,prompt TEXT NOT NULL,response TEXT NOT NULL,created_at TEXT DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY(user_id) REFERENCES users(id))''',
    '''CREATE TABLE IF NOT EXISTS cv_mentor_requests (id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER NOT NULL,topic TEXT NOT NULL,message TEXT NOT NULL,status TEXT DEFAULT 'open',created_at TEXT DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY(user_id) REFERENCES users(id))''',
    '''CREATE TABLE IF NOT EXISTS cv_saved_opportunities (id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER NOT NULL,title TEXT NOT NULL,organisation TEXT DEFAULT '',opportunity_type TEXT DEFAULT 'Learning',url TEXT DEFAULT '',notes TEXT DEFAULT '',created_at TEXT DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY(user_id) REFERENCES users(id))''',
    '''CREATE TABLE IF NOT EXISTS cv_project_milestones (id INTEGER PRIMARY KEY AUTOINCREMENT,project_id INTEGER NOT NULL,user_id INTEGER NOT NULL,title TEXT NOT NULL,status TEXT DEFAULT 'pending',completed_at TEXT,FOREIGN KEY(project_id) REFERENCES cv_projects(id) ON DELETE CASCADE,FOREIGN KEY(user_id) REFERENCES users(id))''',
    '''CREATE TABLE IF NOT EXISTS cv_practice_attempts (id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER NOT NULL,topic TEXT NOT NULL,score INTEGER NOT NULL,max_score INTEGER NOT NULL,answers_json TEXT NOT NULL,created_at TEXT DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY(user_id) REFERENCES users(id))''',
    '''CREATE TABLE IF NOT EXISTS cv_roadmap_progress (id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER NOT NULL,roadmap_id INTEGER NOT NULL,step_index INTEGER NOT NULL,proof TEXT DEFAULT '',status TEXT DEFAULT 'completed',completed_at TEXT DEFAULT CURRENT_TIMESTAMP,UNIQUE(user_id,roadmap_id,step_index))''',
    '''CREATE TABLE IF NOT EXISTS cv_ai_roadmaps (id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER NOT NULL,role TEXT NOT NULL,provider TEXT NOT NULL DEFAULT 'curated-fallback',roadmap_json TEXT NOT NULL,created_at TEXT DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY(user_id) REFERENCES users(id))'''
    ]
    for s in statements: conn.execute(s)
    cols={r['name'] for r in conn.execute('PRAGMA table_info(cv_profiles)').fetchall()}
    if 'career_target' not in cols: conn.execute("ALTER TABLE cv_profiles ADD COLUMN career_target TEXT DEFAULT ''")
    conn.commit(); conn.close()


def _uid(): return session.get('user_id')
def _latest_scores(get_db):
    conn=get_db(); r=conn.execute('SELECT scores_json FROM cv_diagnostics WHERE user_id=? ORDER BY id DESC LIMIT 1',(_uid(),)).fetchone(); conn.close()
    try: return json.loads(r['scores_json']) if r else {}
    except Exception: return {}

def _profile(get_db):
    conn=get_db(); row=conn.execute('SELECT * FROM cv_profiles WHERE user_id=?',(_uid(),)).fetchone(); conn.close(); return row

def _fallback_roadmap(role, profile, diagnostic_scores):
    """A transparent, useful plan that works even without an external AI key."""
    experience=(profile['experience_level'] if profile else 'beginner') or 'beginner'
    hours=(profile['hours_per_day'] if profile else '1 hour') or '1 hour'
    language=(profile['preferred_language'] if profile else 'English') or 'English'
    templates={
      'Frontend Developer':[
       ('Weeks 1–2','HTML, CSS and web foundations','Build semantic pages, forms and responsive layouts.','Publish a responsive personal profile page.'),
       ('Weeks 3–4','JavaScript fundamentals','Practise variables, functions, arrays, DOM and events.','Build an interactive quiz or expense calculator.'),
       ('Weeks 5–6','Git, accessibility and UI quality','Use Git branches, commits, semantic HTML and keyboard checks.','Improve and document two projects on GitHub.'),
       ('Weeks 7–9','React and API basics','Learn components, state, routing and fetch requests.','Build a small React application using a public API.'),
       ('Weeks 10–12','Portfolio and interview preparation','Deploy projects, explain design decisions and practise role questions.','Publish a portfolio, resume and project walkthrough.')],
      'Software Developer':[
       ('Weeks 1–2','Programming foundations','Choose one language and master variables, conditions, loops and functions.','Build a command-line utility with input validation.'),
       ('Weeks 3–4','OOP, debugging and Git','Practise classes, modular code, testing and version control.','Create a small object-oriented application with tests.'),
       ('Weeks 5–7','Data structures and algorithms','Learn arrays, strings, stacks, queues, searching and sorting.','Solve and explain 20 beginner problems.'),
       ('Weeks 8–10','Databases and backend fundamentals','Learn SQL, HTTP, APIs and one backend framework.','Build a CRUD application backed by a database.'),
       ('Weeks 11–12','Software quality and job preparation','Add tests, documentation, deployment and interview practice.','Publish two projects and a technical portfolio.')],
      'Data Analyst':[
       ('Weeks 1–2','Spreadsheets and data thinking','Learn formulas, sorting, filtering, pivot tables and data quality.','Analyse a small real-world spreadsheet dataset.'),
       ('Weeks 3–4','SQL foundations','Practise SELECT, WHERE, GROUP BY, JOIN and subqueries.','Answer 25 SQL questions and write a mini case study.'),
       ('Weeks 5–6','Statistics and Python / Pandas','Learn distributions, averages, missing values and data cleaning.','Clean a dataset and document your decisions.'),
       ('Weeks 7–9','Visualisation and dashboards','Build charts and dashboards; explain limitations honestly.','Publish a Power BI or Tableau-style dashboard.'),
       ('Weeks 10–12','Portfolio and analyst interviews','Practise business questions, insight writing and presentations.','Create two case studies with clear recommendations.')],
      'Data Scientist / AI-ML':[
       ('Weeks 1–3','Python and problem solving','Learn Python, functions, data structures and debugging.','Build a small data collection or analysis script.'),
       ('Weeks 4–5','Math, statistics and SQL','Study probability, descriptive statistics, vectors and querying.','Complete a notebook exploring a dataset.'),
       ('Weeks 6–8','Data analysis and machine learning','Learn Pandas, train/test split, baseline models and evaluation.','Train and evaluate a simple prediction model.'),
       ('Weeks 9–10','Model improvement and responsible AI','Study leakage, imbalance, fairness, explainability and validation.','Compare models and write a limitations report.'),
       ('Weeks 11–12','End-to-end portfolio and interviews','Package a reproducible project and practise explaining trade-offs.','Publish an end-to-end ML project with README and demo.')],
      'Cybersecurity Analyst':[
       ('Weeks 1–2','Networking and operating systems','Learn IP, DNS, HTTP, Linux commands and permissions.','Document a safe home-lab network diagram.'),
       ('Weeks 3–4','Security fundamentals','Study threat models, authentication, encryption and secure habits.','Create a security review checklist for a test application.'),
       ('Weeks 5–7','Defensive tools and logs','Practise log analysis, incident basics and system hardening.','Write a small log-analysis report.'),
       ('Weeks 8–10','Authorised practice labs','Use legal beginner labs and document findings responsibly.','Complete selected beginner labs and explain mitigations.'),
       ('Weeks 11–12','Portfolio and interview preparation','Build a lab journal, threat explanations and response playbooks.','Publish a defensive security portfolio with no sensitive data.')],
      'Business Analyst':[
       ('Weeks 1–2','Business problem framing','Learn stakeholders, requirements, processes and measurable outcomes.','Write a problem statement and stakeholder map.'),
       ('Weeks 3–4','Spreadsheets and data literacy','Use formulas, pivot tables, charts and data quality checks.','Create a short evidence-based analysis.'),
       ('Weeks 5–6','SQL and process modelling','Practise querying and map current/future workflows.','Build a process map and simple SQL report.'),
       ('Weeks 7–9','Dashboards and communication','Create dashboards and concise recommendations.','Present a dashboard with assumptions and limitations.'),
       ('Weeks 10–12','Case studies and job readiness','Practise requirement gathering, user stories and interview cases.','Publish two BA case studies and a portfolio.')],
      'Core Engineering / Other':[
       ('Weeks 1–2','Discipline foundations and digital fluency','Map core concepts, tools, safety and digital skills for your subject.','Create a structured subject revision and tool plan.'),
       ('Weeks 3–4','Measurement and technical problem solving','Practise data recording, calculations, constraints and repeatability.','Document a small investigation with units and results.'),
       ('Weeks 5–7','Discipline tools and applied practice','Choose software, lab tools or methods relevant to your branch.','Complete a guided practical exercise and explain it.'),
       ('Weeks 8–10','Project and technical communication','Build a useful branch-related prototype or case study.','Document the design, test method, result and limitations.'),
       ('Weeks 11–12','Portfolio and career preparation','Research entry-level roles, internships and required competencies.','Prepare a technical portfolio and practise interview explanations.')]
    }
    if role in ('Arts, Humanities & Social Sciences','Health & Life Sciences','Design & Creative Industries','General Professional / Any Degree'):
        templates[role]=[
          ('Weeks 1–2','Discipline foundations and digital fluency','Identify core concepts, ethical standards, digital tools and research practices for your field.','Create a subject-specific learning map and source notebook.'),
          ('Weeks 3–4','Research, communication and evidence','Practise evaluating sources, taking notes and communicating ideas clearly.','Write a short evidence-based report or creative brief.'),
          ('Weeks 5–7','Field tools and practical skills','Learn the software, methods, lab practices or workflows used in your discipline.','Complete a guided practical task and document your process.'),
          ('Weeks 8–10','Applied project and portfolio','Create a project that addresses a real problem or demonstrates a core capability.','Publish a case study, project report, design portfolio or practical log.'),
          ('Weeks 11–12','Professional preparation','Research entry-level roles, internships, ethical expectations and interview formats.','Prepare a role-specific portfolio, resume and interview stories.') ]
    steps=templates.get(role,templates['Core Engineering / Other'])
    if experience in ('intermediate','advanced'):
        steps=steps[1:]+[('Final weeks','Advanced project and role preparation','Skip basics you can demonstrate; deepen one role-specific specialism.','Publish a substantial project with tests and a clear technical walkthrough.')]
    return {'title':f'{role} learning path','summary':f'A practical starter plan designed around your current level ({experience}), available time ({hours} per day) and preferred learning language ({language}). Adjust the pace to your semester and responsibilities.','weekly_commitment':hours,'language':language,'starting_assumptions':['This is a provisional plan based on your profile and latest diagnostic, not a permanent label.','If you can already demonstrate a skill, skip its beginner lesson and move to a practical challenge.','Spend more time building and explaining projects than collecting certificates.'],'weeks':[{'period':a,'focus':b,'learn_and_practise':c,'proof_of_skill':d} for a,b,c,d in steps],'job_readiness_checklist':['Two or more relevant projects with readable documentation','GitHub or an equivalent portfolio of work','Ability to explain design choices, trade-offs and mistakes','Role-specific fundamentals and practical exercises','Resume tailored to the role and truthful project descriptions','Mock interviews and applications reviewed regularly'],'next_action':'Start with the first week, complete one small task, and save evidence of what you built.'}


def _generate_personal_roadmap(get_db, role, profile):
    conn=get_db()
    latest=conn.execute('SELECT scores_json FROM cv_diagnostics WHERE user_id=? ORDER BY id DESC LIMIT 1',(_uid(),)).fetchone()
    conn.close()
    scores=json.loads(latest['scores_json']) if latest else {}
    fallback=_fallback_roadmap(role,profile,scores)
    api_key=os.environ.get('GEMINI_API_KEY')
    if not api_key:
        return fallback,'curated-fallback'
    try:
        from google import genai
        client=genai.Client(api_key=api_key)
        safe_profile={
          'degree':profile['degree'] if profile else '', 'branch_or_subject':profile['branch'] if profile else '',
          'year':profile['study_year'] if profile else '', 'graduation_year':profile['graduation_year'] if profile else '',
          'career_interest':profile['interests'] if profile else '', 'target_role':role,
          'hours_per_day':profile['hours_per_day'] if profile else '1 hour',
          'preferred_language':profile['preferred_language'] if profile else 'English',
          'experience_level':profile['experience_level'] if profile else 'beginner',
          'device_access':profile['device_access'] if profile else 'laptop', 'diagnostic_category_scores':scores
        }
        prompt=("You are CAREERVERSE's careful career-learning planner for college students of every degree. "
          "Create a realistic, supportive, practical 12-week learning path for the student's target role. "
          "Assume the student may be starting from zero. Adapt to available time, device limits, language and diagnostic gaps. "
          "Do not guarantee employment, invent certifications, recommend paid-only resources, or label the student negatively. "
          "Prioritise fundamentals, practice, projects, Git/version control where relevant, portfolio evidence, communication and interview preparation. "
          "Do not repeat topics that a learner can prove through a practical challenge. "
          "Return ONLY valid JSON with keys title, summary, weekly_commitment, language, starting_assumptions (array of 3 strings), "
          "weeks (array of 6 objects with period, focus, learn_and_practise, proof_of_skill, topic_ids), job_readiness_checklist (array of 6 strings), next_action. "
          "topic_ids is an array of 1-3 ids chosen ONLY from this list that best match the week: "+", ".join(TOPICS)+". "
          "Keep the content concise and achievable. Student learning profile and diagnostic scores: "+json.dumps(safe_profile,ensure_ascii=False))
        response=client.models.generate_content(model=os.environ.get('GEMINI_MODEL','gemini-3.8-flash'),contents=prompt)
        raw=(getattr(response,'text',None) or '').strip()
        raw=re.sub(r'^```(?:json)?\s*|\s*```$','',raw,flags=re.I)
        data=json.loads(raw)
        raw_weeks=data.get('weeks') if isinstance(data.get('weeks'),list) else []
        if not isinstance(data.get('weeks'),list) or not data['weeks']:
            raise ValueError('Gemini response did not contain a valid week plan')
        # Bound model output before saving/rendering.
        for key in ('title','summary','weekly_commitment','language','next_action'):
            data[key]=str(data.get(key,fallback.get(key,'')))[:1200]
        data['starting_assumptions']=[str(x)[:500] for x in data.get('starting_assumptions',[])[:6]]
        data['job_readiness_checklist']=[str(x)[:500] for x in data.get('job_readiness_checklist',[])[:10]]
        data['weeks']=[{k:str(w.get(k,''))[:1000] for k in ('period','focus','learn_and_practise','proof_of_skill')} for w in data['weeks'][:12] if isinstance(w,dict)]
        for _w,_src in zip(data['weeks'],[w for w in raw_weeks[:12] if isinstance(w,dict)]):
            _w['topic_ids']=[t for t in (_src.get('topic_ids') or []) if t in TOPICS][:3] if isinstance(_src.get('topic_ids'),list) else []
        if not data['weeks']: raise ValueError('Empty roadmap weeks')
        return data,'gemini'
    except Exception:
        # Gemini outage, invalid response or quota issue never blocks core learning.
        return fallback,'curated-fallback'


def _infer_role(value):
    """Map free-text interests to a supported role without forcing one degree path."""
    value=(value or '').strip()
    if value in ROLES: return value
    lower=value.lower()
    rules=[
      (['front','web','website','ui'], 'Frontend Developer'),
      (['cyber','security'], 'Cybersecurity Analyst'),
      (['business','commerce','management','account'], 'Business Analyst'),
      (['data analyst','analytics','excel','power bi'], 'Data Analyst'),
      (['machine learning','ai/ml','artificial intelligence','data scientist','data science'], 'Data Scientist / AI-ML'),
      (['art','history','humanities','sociology','psychology','political','literature','language'], 'Arts, Humanities & Social Sciences'),
      (['health','biology','biotech','biomedical','pharma','nursing','life science'], 'Health & Life Sciences'),
      (['design','creative','graphic','animation','media','fashion'], 'Design & Creative Industries'),
      (['general','undecided','any degree','explore'], 'General Professional / Any Degree'),
      (['engineer','mechanical','electrical','civil','electronics'], 'Core Engineering / Other'),
      (['software','developer','program','computer science'], 'Software Developer')]
    for words,role in rules:
        if any(word in lower for word in words): return role
    return 'General Professional / Any Degree'


def register_careerverse(app,get_db,login_required):
    init_careerverse_db(get_db)
    def protected(): return login_required()

    @cv.route('/')
    def hub():
        if not protected(): return redirect('/login')
        conn=get_db(); uid=_uid()
        profile=conn.execute('SELECT * FROM cv_profiles WHERE user_id=?',(uid,)).fetchone()
        diag=conn.execute('SELECT * FROM cv_diagnostics WHERE user_id=? ORDER BY id DESC LIMIT 1',(uid,)).fetchone()
        completed=conn.execute('SELECT COUNT(*) FROM cv_lesson_progress WHERE user_id=?',(uid,)).fetchone()[0]
        projects=conn.execute('SELECT * FROM cv_projects WHERE user_id=? ORDER BY id DESC LIMIT 4',(uid,)).fetchall()
        evidence=conn.execute('SELECT COUNT(*) FROM cv_skill_evidence WHERE user_id=?',(uid,)).fetchone()[0]
        conn.close()
        return render_template('careerverse/hub.html',profile=profile,diagnosed=bool(diag),completed=completed,projects=projects,evidence=evidence,tracks=TRACKS)

    @cv.route('/onboarding',methods=['GET','POST'])
    def onboarding():
        if not protected(): return redirect('/login')
        if request.method=='POST':
            data=request.form
            conn=get_db(); conn.execute('''INSERT INTO cv_profiles(user_id,degree,branch,study_year,graduation_year,interests,hours_per_day,preferred_language,experience_level,device_access,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?,CURRENT_TIMESTAMP) ON CONFLICT(user_id) DO UPDATE SET degree=excluded.degree,branch=excluded.branch,study_year=excluded.study_year,graduation_year=excluded.graduation_year,interests=excluded.interests,hours_per_day=excluded.hours_per_day,preferred_language=excluded.preferred_language,experience_level=excluded.experience_level,device_access=excluded.device_access,updated_at=CURRENT_TIMESTAMP''',(_uid(),data.get('degree','')[:100],data.get('branch','')[:100],data.get('study_year',''),data.get('graduation_year','')[:8],data.get('interests','')[:500],data.get('hours_per_day','1'),data.get('preferred_language','English'),data.get('experience_level','beginner'),data.get('device_access','laptop'))); conn.commit(); conn.close()
            flash('Your learning profile has been saved. You can update it whenever your goals change.','success')
            return redirect(url_for('careerverse.diagnosis'))
        return render_template('careerverse/onboarding.html',profile=_profile(get_db))

    @cv.route('/diagnosis',methods=['GET','POST'])
    def diagnosis():
        if not protected(): return redirect('/login')
        if request.method=='POST':
            answers={str(i):request.form.get(f'q{i}','') for i in range(len(DIAGNOSTIC))}
            scores={k:{'correct':0,'total':0} for k in ['programming','web','data','digital','problem_solving','software_tools','communication']}
            for i,q in enumerate(DIAGNOSTIC):
                key=q['skill']
                if q['correct'] is not None:
                    scores[key]['total']+=1
                    if answers[str(i)]==str(q['correct']): scores[key]['correct']+=1
            # Experience/communication self-reports are retained but not treated as verified test scores.
            scores['programming']['self_report']=answers['0']; scores['communication']['self_report']=answers['9']
            conn=get_db(); cur=conn.execute('INSERT INTO cv_diagnostics(user_id,answers_json,scores_json) VALUES(?,?,?)',(_uid(),json.dumps(answers),json.dumps(scores))); did=cur.lastrowid; conn.commit(); conn.close()
            return redirect(url_for('careerverse.results',diagnostic_id=did))
        return render_template('careerverse/diagnosis.html',questions=DIAGNOSTIC)

    @cv.route('/diagnosis/result/<int:diagnostic_id>')
    def results(diagnostic_id):
        if not protected(): return redirect('/login')
        conn=get_db(); d=conn.execute('SELECT * FROM cv_diagnostics WHERE id=? AND user_id=?',(diagnostic_id,_uid())).fetchone(); conn.close()
        if not d: return 'Assessment not found',404
        scores=json.loads(d['scores_json']); profile=_profile(get_db)
        rec='career-digital'
        interests=(profile['interests'] or '').lower() if profile else ''
        if any(w in interests for w in ['web','frontend','front end','website']): rec='web-foundations'
        elif any(w in interests for w in ['cyber','security']): rec='cybersecurity'
        elif any(w in interests for w in ['business','management','commerce']): rec='business-analysis'
        elif any(w in interests for w in ['engineering','mechanical','electrical','civil']): rec='core-engineering'
        elif any(w in interests for w in ['data','analyst','statistics']): rec='data-analytics'
        elif any(w in interests for w in ['ai','machine','python','software','developer']): rec='python-starter'
        return render_template('careerverse/results.html',scores=scores,recommended=rec,track=TRACKS[rec],diagnostic=d)

    @cv.route('/roadmap', methods=['GET','POST'])
    def roadmap():
        if not protected(): return redirect('/login')
        profile=_profile(get_db)
        role=(profile['career_target'] if profile and profile['career_target'] else (profile['interests'] if profile else '')) or 'Explore my options'
        role_key=next((k for k in ROLES if k.lower()==role.lower()), None)
        if not role_key:
            role_lower=role.lower()
            if any(w in role_lower for w in ['front','web','website','ui']): role_key='Frontend Developer'
            elif any(w in role_lower for w in ['cyber','security']): role_key='Cybersecurity Analyst'
            elif any(w in role_lower for w in ['business','commerce','management']): role_key='Business Analyst'
            elif any(w in role_lower for w in ['data analyst','analytics','excel','power bi']): role_key='Data Analyst'
            elif any(w in role_lower for w in ['machine learning','ai/ml','data scientist','artificial intelligence']): role_key='Data Scientist / AI-ML'
            elif any(w in role_lower for w in ['engineer','mechanical','electrical','civil','electronics']): role_key='Core Engineering / Other'
            elif any(w in role_lower for w in ['software','developer','program']): role_key='Software Developer'
            elif any(w in role_lower for w in ['art','history','humanities','sociology','psychology','political','literature','language']): role_key='Arts, Humanities & Social Sciences'
            elif any(w in role_lower for w in ['health','biology','biotech','biomedical','pharma','nursing','life science']): role_key='Health & Life Sciences'
            elif any(w in role_lower for w in ['design','creative','graphic','animation','media','fashion']): role_key='Design & Creative Industries'
            elif any(w in role_lower for w in ['general','undecided','any degree','explore']): role_key='General Professional / Any Degree'
            else: role_key='Core Engineering / Other'
        if request.method=='POST':
            requested=request.form.get('role','').strip()
            if requested in ROLES:
                role_key=requested
                conn=get_db(); conn.execute('UPDATE cv_profiles SET career_target=?,updated_at=CURRENT_TIMESTAMP WHERE user_id=?',(role_key,_uid())); conn.commit(); conn.close()
                profile=_profile(get_db)
            roadmap_data, provider = _generate_personal_roadmap(get_db, role_key, profile)
            conn=get_db(); conn.execute('INSERT INTO cv_ai_roadmaps(user_id,role,provider,roadmap_json) VALUES(?,?,?,?)',(_uid(),role_key,provider,json.dumps(roadmap_data,ensure_ascii=False))); conn.commit(); conn.close()
            flash('Your personalised learning path has been generated.' if provider=='gemini' else 'Your learning path is ready using CAREERVERSE curated guidance. Add your Gemini API key to personalise it with Gemini.','success')
            return redirect(url_for('careerverse.roadmap'))
        conn=get_db()
        done=conn.execute('SELECT track_id,lesson_slug FROM cv_lesson_progress WHERE user_id=?',(_uid(),)).fetchall()
        saved=conn.execute('SELECT * FROM cv_ai_roadmaps WHERE user_id=? ORDER BY id DESC LIMIT 1',(_uid(),)).fetchone()
        step_status={}
        if saved:
            conn=get_db(); step_status={r['step_index'] for r in conn.execute("SELECT step_index FROM cv_roadmap_progress WHERE user_id=? AND roadmap_id=? AND status='completed'",(_uid(),saved['id'])).fetchall()}; conn.close()
        conn=None
        roadmap_data=json.loads(saved['roadmap_json']) if saved else None
        n_steps=len(roadmap_data['weeks']) if roadmap_data else 0
        next_step=next((i for i in range(n_steps) if i not in step_status),None)
        resource_key=ROLE_RESOURCE_MAP.get(role_key,'career-digital')
        track_ids=ROLES[role_key]['tracks'] if role_key in ROLES else ['career-digital']
        return render_template('careerverse/roadmap.html',profile=profile,role=role_key,track_ids=track_ids,tracks=TRACKS,done={(r['track_id'],r['lesson_slug']) for r in done},step_status=step_status,next_step=next_step,n_steps=n_steps,roadmap_data=roadmap_data,roadmap_provider=(saved['provider'] if saved else None),resources=LEARNING_RESOURCES.get(resource_key,LEARNING_RESOURCES['career-digital']),roles=ROLES,gemini_enabled=bool(os.environ.get('GEMINI_API_KEY')))

    def _load_roadmap():
        conn=get_db(); saved=conn.execute('SELECT * FROM cv_ai_roadmaps WHERE user_id=? ORDER BY id DESC LIMIT 1',(_uid(),)).fetchone(); conn.close()
        if not saved: return None,None
        try: return saved,json.loads(saved['roadmap_json'])
        except Exception: return saved,None

    @cv.route('/roadmap/step/<int:i>',methods=['GET','POST'])
    def roadmap_step(i):
        if not protected(): return redirect('/login')
        saved,data=_load_roadmap()
        if not data or not data.get('weeks'):
            flash('Generate your roadmap first, then open a step.','error'); return redirect(url_for('careerverse.roadmap'))
        weeks=data['weeks']
        if i<0 or i>=len(weeks): return 'Step not found',404
        week=weeks[i]; rid=saved['id']
        if request.method=='POST':
            proof=request.form.get('proof','').strip()[:3000]
            if len(proof)<15:
                flash('Write at least a short explanation or link to your proof before marking this step complete.','error')
            else:
                conn=get_db(); conn.execute("INSERT INTO cv_roadmap_progress(user_id,roadmap_id,step_index,proof,status) VALUES(?,?,?,?, 'completed') ON CONFLICT(user_id,roadmap_id,step_index) DO UPDATE SET proof=excluded.proof,status='completed',completed_at=CURRENT_TIMESTAMP",(_uid(),rid,i,proof)); conn.commit(); conn.close()
                flash('Step completed. Great work, now move to the next step.','success')
                return redirect(url_for('careerverse.roadmap_step',i=i+1) if i+1<len(weeks) else url_for('careerverse.roadmap'))
        conn=get_db()
        rows=conn.execute('SELECT step_index,proof FROM cv_roadmap_progress WHERE user_id=? AND roadmap_id=?',(_uid(),rid)).fetchall()
        lessons_done={(r['track_id'],r['lesson_slug']) for r in conn.execute('SELECT track_id,lesson_slug FROM cv_lesson_progress WHERE user_id=?',(_uid(),)).fetchall()}
        conn.close()
        done={r['step_index'] for r in rows}; my_proof=next((r['proof'] for r in rows if r['step_index']==i),'')
        profile=_profile(get_db); scores=_latest_scores(get_db)
        blocks=[]
        for t in match_topics(week):
            pseudo={'title':t['name'],'slug':t['id'],'minutes':35}
            p=build_personal_resources('topic:'+t['id'],pseudo,t,profile,scores)
            ac=[{'track_id':tid,'slug':slug,'title':next(l['title'] for l in TRACKS[tid]['lessons'] if l['slug']==slug),'done':(tid,slug) in lessons_done} for tid,slug in t['academy'] if tid in TRACKS]
            blocks.append({'topic':t,'pres':p,'academy':ac})
        return render_template('careerverse/roadmap_step.html',i=i,n=len(weeks),week=week,weeks=weeks,done=done,my_proof=my_proof,blocks=blocks,title=data.get('title',''))

    @cv.route('/resources')
    def resources():
        if not protected(): return redirect('/login')
        profile=_profile(get_db)
        role=_infer_role((profile['career_target'] if profile and profile['career_target'] else '') or (profile['interests'] if profile else ''))
        resource_key=ROLE_RESOURCE_MAP.get(role,'career-digital')
        return render_template('careerverse/resources.html',role=role,resources=LEARNING_RESOURCES.get(resource_key,LEARNING_RESOURCES['career-digital']),all_resources=LEARNING_RESOURCES)

    @cv.route('/academy')
    def academy():
        if not protected(): return redirect('/login')
        conn=get_db(); rows=conn.execute('SELECT track_id,COUNT(*) AS n FROM cv_lesson_progress WHERE user_id=? GROUP BY track_id',(_uid(),)).fetchall(); conn.close(); progress={r['track_id']:r['n'] for r in rows}
        return render_template('careerverse/academy.html',tracks=TRACKS,progress=progress)

    @cv.route('/academy/<track_id>')
    def track(track_id):
        if not protected(): return redirect('/login')
        t=TRACKS.get(track_id)
        if not t: return 'Track not found',404
        conn=get_db(); rows=conn.execute('SELECT lesson_slug FROM cv_lesson_progress WHERE user_id=? AND track_id=?',(_uid(),track_id)).fetchall(); conn.close(); done={r['lesson_slug'] for r in rows}
        return render_template('careerverse/track.html',track_id=track_id,track=t,done=done,track_videos=visible_videos(get_track_resources(track_id),_profile(get_db)))

    @cv.route('/academy/<track_id>/<lesson_slug>',methods=['GET','POST'])
    def lesson(track_id,lesson_slug):
        if not protected(): return redirect('/login')
        t=TRACKS.get(track_id); lesson=next((x for x in t['lessons'] if x['slug']==lesson_slug),None) if t else None
        if not lesson: return 'Lesson not found',404
        if request.method=='POST':
            reflection=request.form.get('reflection','').strip()[:2000]
            if len(reflection)<15:
                flash('Please write at least a short explanation of what you learned before marking this lesson complete.','error')
            else:
                conn=get_db(); conn.execute('INSERT INTO cv_lesson_progress(user_id,track_id,lesson_slug,reflection) VALUES(?,?,?,?) ON CONFLICT(user_id,track_id,lesson_slug) DO UPDATE SET reflection=excluded.reflection,status="completed",completed_at=CURRENT_TIMESTAMP',(_uid(),track_id,lesson_slug,reflection)); conn.commit(); conn.close(); flash('Lesson evidence saved. Learning progress is not the same as verified proficiency.','success'); return redirect(url_for('careerverse.track',track_id=track_id))
        res=get_lesson_resources(track_id,lesson_slug)
        pres=build_personal_resources(track_id,lesson,res,_profile(get_db),_latest_scores(get_db)) if res else None
        return render_template('careerverse/lesson.html',track_id=track_id,track=t,lesson=lesson,res=res,pres=pres,ai_enabled=bool(os.environ.get('GEMINI_API_KEY')))

    @cv.route('/academy/<track_id>/<lesson_slug>/personalize')
    def lesson_personalize(track_id,lesson_slug):
        if not protected(): return jsonify({'error':'login required'}),401
        t=TRACKS.get(track_id); lesson=next((x for x in t['lessons'] if x['slug']==lesson_slug),None) if t else None
        res=get_lesson_resources(track_id,lesson_slug)
        if not lesson or not res: return jsonify({'error':'not found'}),404
        profile=_profile(get_db); scores=_latest_scores(get_db)
        base=build_personal_resources(track_id,lesson,res,profile,scores)
        out=ai_refine(get_db,_uid(),track_id,lesson,base,profile,scores)
        return jsonify({'ok':bool(out),**(out or {})})

    @cv.route('/projects',methods=['GET','POST'])
    def projects():
        if not protected(): return redirect('/login')
        if request.method=='POST':
            f=request.form; title=f.get('title','').strip(); desc=f.get('description','').strip()
            if not title or not desc: flash('Project title and problem statement are required.','error')
            else:
                conn=get_db(); cur=conn.execute('INSERT INTO cv_projects(user_id,title,track_id,description,repo_url,demo_url,reflection) VALUES(?,?,?,?,?,?,?)',(_uid(),title,f.get('track_id',''),desc[:3000],f.get('repo_url','')[:500],f.get('demo_url','')[:500],f.get('reflection','')[:2000])); project_id=cur.lastrowid
                for milestone in ['Define the problem and success criteria','Plan the design and tools','Build the first working version','Test, debug and improve','Document and demonstrate the project']:
                    conn.execute('INSERT INTO cv_project_milestones(project_id,user_id,title) VALUES(?,?,?)',(project_id,_uid(),milestone))
                conn.commit(); conn.close(); flash('Project added with five build milestones.','success'); return redirect(url_for('careerverse.projects'))
        conn=get_db(); rows=conn.execute('SELECT * FROM cv_projects WHERE user_id=? ORDER BY id DESC',(_uid(),)).fetchall(); milestones={}
        for project in rows: milestones[project['id']]=conn.execute('SELECT * FROM cv_project_milestones WHERE project_id=? AND user_id=? ORDER BY id',(project['id'],_uid())).fetchall()
        conn.close()
        return render_template('careerverse/projects.html',projects=rows,tracks=TRACKS,milestones=milestones)

    @cv.route('/projects/<int:project_id>/milestone/<int:milestone_id>',methods=['POST'])
    def project_milestone(project_id,milestone_id):
        if not protected(): return redirect('/login')
        conn=get_db(); row=conn.execute('SELECT m.* FROM cv_project_milestones m JOIN cv_projects p ON p.id=m.project_id WHERE m.id=? AND m.project_id=? AND m.user_id=? AND p.user_id=?',(milestone_id,project_id,_uid(),_uid())).fetchone()
        if not row: conn.close(); return 'Milestone not found',404
        new_status='completed' if row['status']!='completed' else 'pending'
        conn.execute('UPDATE cv_project_milestones SET status=?,completed_at=CASE WHEN ?="completed" THEN CURRENT_TIMESTAMP ELSE NULL END WHERE id=? AND user_id=?',(new_status,new_status,milestone_id,_uid()))
        conn.commit(); conn.close(); return redirect(url_for('careerverse.projects'))

    @cv.route('/evidence',methods=['GET','POST'])
    def evidence():
        if not protected(): return redirect('/login')
        if request.method=='POST':
            f=request.form; skill=f.get('skill_name','').strip(); explanation=f.get('explanation','').strip()
            if not skill or len(explanation)<20: flash('Add a skill and explain how your evidence demonstrates it (at least 20 characters).','error')
            else:
                conn=get_db(); conn.execute('INSERT INTO cv_skill_evidence(user_id,skill_name,evidence_type,evidence_url,explanation) VALUES(?,?,?,?,?)',(_uid(),skill[:100],f.get('evidence_type','Project'),f.get('evidence_url','')[:500],explanation[:2000])); conn.commit(); conn.close(); flash('Evidence saved as self-reported. It is not independently verified yet.','success'); return redirect(url_for('careerverse.evidence'))
        conn=get_db(); rows=conn.execute('SELECT * FROM cv_skill_evidence WHERE user_id=? ORDER BY id DESC',(_uid(),)).fetchall(); conn.close()
        return render_template('careerverse/evidence.html',rows=rows)

    @cv.route('/tutor',methods=['GET','POST'])
    def tutor():
        if not protected(): return redirect('/login')
        answer=None; prompt=''; mode='Teach me'; ai_error=None
        if request.method=='POST':
            prompt=request.form.get('prompt','').strip()[:3000]; mode=request.form.get('mode','Teach me')
            if prompt:
                answer=None; key=os.environ.get('GEMINI_API_KEY')
                if key:
                    try:
                        from google import genai
                        client=genai.Client(api_key=key)
                        instruction=f"You are CAREERVERSE, a patient free learning tutor for college students across all degrees. Mode: {mode}. Explain simply, step by step, avoid doing assessed work dishonestly, ask the learner to try. If unsure say so. Student question: {prompt}"
                        answer=client.models.generate_content(model=os.environ.get('GEMINI_MODEL','gemini-3.8-flash'),contents=instruction).text
                    except Exception as exc:
                        # Keep the student-facing fallback, but record the real cause
                        # in the Flask terminal so API problems are diagnosable.
                        logging.exception('CAREERVERSE Gemini tutor request failed')
                        ai_error=f'{type(exc).__name__}: Gemini request failed. Check the Flask terminal for details.'
                        answer=None
                if not answer:
                    lower=prompt.lower()
                    if mode=='Give me practice':
                        answer='Here is a small practice task: '+('Create an HTML page with a heading, paragraph and link.' if 'html' in lower else 'Write a short Python program that reads three numbers and prints their sum.' if ('python' in lower or 'program' in lower) else 'Choose one concept from your question, create a tiny example and explain the result.\n\nAfter trying it, ask for feedback on your attempt.')+'\n\nTry it without copying a complete solution. Then explain what you changed.'
                    elif mode=='Test my knowledge':
                        answer='Quick knowledge check:\n1. Explain the idea in your own words.\n2. Give one real example.\n3. Describe one common mistake or limitation.\n\nReply with your answers and I can help you review them. This offline mode does not automatically grade open-ended answers.'
                    elif mode=='Guide my project':
                        answer='Use this project sequence:\n1. Define the user and problem.\n2. Write three features for the first version.\n3. Sketch the screen or system design.\n4. Build one small working feature.\n5. Test normal and edge cases.\n6. Document what you built and what you would improve.\n\nTell me your project topic and current stage to make this plan more specific.'
                    elif mode=='Explain my error':
                        answer='Let us debug it systematically. Share the exact error message and the smallest relevant code snippet (remove passwords, API keys and personal data). First reproduce the error, read the traceback from the bottom, identify the file and line, then test one change at a time. Do not randomly rewrite unrelated files.'
                    elif 'html' in lower: answer='HTML provides the structure and meaning of a web page. Start with <!doctype html>, then <html>, <head> for metadata and <body> for visible content. Try creating one heading and one paragraph.\n\nAI tutor is currently in offline fallback mode; this is a starter explanation, not a generated answer.'
                    elif 'css' in lower: answer='CSS controls how HTML looks. A rule has a selector and declarations, for example: p { color: navy; font-size: 16px; }. Try changing one property at a time and refresh the page.\n\nAI tutor is currently in offline fallback mode.'
                    elif 'python' in lower or 'loop' in lower: answer='In Python, a loop repeats instructions. Example: for n in range(1, 4): print(n). This prints 1, 2 and 3. First predict the output, then run it and compare.\n\nAI tutor is currently in offline fallback mode.'
                    else: answer='Let us break this down. First, write what you already understand in one sentence. Next, identify the exact part that is confusing. Try a tiny example, observe the result, and change one thing at a time.\n\nAI tutor is currently in offline fallback mode. Add GEMINI_API_KEY in your local environment to enable generated tutoring; the platform remains usable without it.'
                conn=get_db(); conn.execute('INSERT INTO cv_tutor_sessions(user_id,mode,prompt,response) VALUES(?,?,?,?)',(_uid(),mode,prompt,answer)); conn.commit(); conn.close()
        recs=recommend_for_prompt(prompt,TRACKS,LESSON_RESOURCES,_profile(get_db),_latest_scores(get_db)) if (answer and prompt) else []
        return render_template('careerverse/tutor.html',answer=answer,prompt=prompt,mode=mode,ai_enabled=bool(os.environ.get('GEMINI_API_KEY')),ai_error=ai_error,recs=recs)

    practice_questions=[
        {'q':'Which HTML element represents the main page heading?','o':['<h1>','<div>','<span>','<footer>'],'a':0,'why':'Use a heading element such as h1 for the primary heading.'},
        {'q':'Which CSS property changes text colour?','o':['font-style','color','background','display'],'a':1,'why':'The color property sets the foreground text colour.'},
        {'q':'What is the output of Python: print(2 + 3 * 2)?','o':['10','12','8','7'],'a':2,'why':'Multiplication is evaluated before addition: 2 + 6 = 8.'},
        {'q':'Which data structure stores key-value pairs in Python?','o':['List','Tuple','Dictionary','Set'],'a':2,'why':'A dictionary maps keys to values.'},
        {'q':'What is a primary key in a relational database?','o':['A unique row identifier','A duplicate field','A chart title','A password hint'],'a':0,'why':'A primary key uniquely identifies each record in a table.'},
        {'q':'A chart shows correlation between two variables. What can you conclude?','o':['One definitely causes the other','They are associated in this dataset','The data is perfect','There are no confounding factors'],'a':1,'why':'Correlation alone does not prove causation.'}
    ]

    @cv.route('/practice',methods=['GET','POST'])
    def practice():
        if not protected(): return redirect('/login')
        if request.method=='POST':
            answers={str(i):request.form.get(f'q{i}','') for i in range(len(practice_questions))}
            score=sum(1 for i,q in enumerate(practice_questions) if answers[str(i)]==str(q['a']))
            conn=get_db(); cur=conn.execute('INSERT INTO cv_practice_attempts(user_id,topic,score,max_score,answers_json) VALUES(?,?,?,?,?)',(_uid(),'Foundation mixed practice',score,len(practice_questions),json.dumps(answers))); attempt_id=cur.lastrowid; conn.commit(); conn.close()
            return render_template('careerverse/practice_result.html',questions=practice_questions,answers=answers,score=score,attempt_id=attempt_id)
        conn=get_db(); history=conn.execute('SELECT * FROM cv_practice_attempts WHERE user_id=? ORDER BY id DESC LIMIT 5',(_uid(),)).fetchall(); conn.close()
        return render_template('careerverse/practice.html',questions=practice_questions,history=history)

    @cv.route('/analytics')
    def analytics():
        if not protected(): return redirect('/login')
        conn=get_db(); uid=_uid()
        lessons=conn.execute('SELECT COUNT(*) FROM cv_lesson_progress WHERE user_id=?',(uid,)).fetchone()[0]
        projects=conn.execute('SELECT COUNT(*) FROM cv_projects WHERE user_id=?',(uid,)).fetchone()[0]
        milestones=conn.execute("SELECT COUNT(*) FROM cv_project_milestones WHERE user_id=? AND status='completed'",(uid,)).fetchone()[0]
        evidence=conn.execute('SELECT COUNT(*) FROM cv_skill_evidence WHERE user_id=?',(uid,)).fetchone()[0]
        practice=conn.execute('SELECT * FROM cv_practice_attempts WHERE user_id=? ORDER BY id DESC LIMIT 5',(uid,)).fetchall()
        diagnostics=conn.execute('SELECT created_at,scores_json FROM cv_diagnostics WHERE user_id=? ORDER BY id DESC LIMIT 5',(uid,)).fetchall()
        conn.close()
        return render_template('careerverse/analytics.html',lessons=lessons,projects=projects,milestones=milestones,evidence=evidence,practice=practice,diagnostics=diagnostics)

    @cv.route('/careers',methods=['GET','POST'])
    def careers():
        if not protected(): return redirect('/login')
        if request.method=='POST':
            role=request.form.get('role','')
            if role not in ROLES:
                flash('Please choose one of the listed career directions.','error')
                return redirect(url_for('careerverse.careers'))
            conn=get_db(); conn.execute('UPDATE cv_profiles SET career_target=?,updated_at=CURRENT_TIMESTAMP WHERE user_id=?',(role,_uid())); conn.commit(); conn.close(); flash('Career direction updated. You can change it at any time.','success'); return redirect(url_for('careerverse.careers'))
        profile=_profile(get_db); selected=((profile['career_target'] or profile['interests']) if profile else '') or ''
        conn=get_db(); skills=conn.execute('SELECT name,progress FROM skills WHERE user_id=?',(_uid(),)).fetchall(); evidence=conn.execute('SELECT skill_name FROM cv_skill_evidence WHERE user_id=?',(_uid(),)).fetchall(); conn.close()
        known={r['name'].lower() for r in skills}|{r['skill_name'].lower() for r in evidence}
        return render_template('careerverse/careers.html',roles=ROLES,tracks=TRACKS,selected=selected,known=known)

    @cv.route('/portfolio')
    def portfolio():
        if not protected(): return redirect('/login')
        conn=get_db(); uid=_uid(); user=conn.execute('SELECT * FROM users WHERE id=?',(uid,)).fetchone(); profile=conn.execute('SELECT * FROM cv_profiles WHERE user_id=?',(uid,)).fetchone(); projects=conn.execute('SELECT * FROM cv_projects WHERE user_id=?',(uid,)).fetchall(); skills=conn.execute('SELECT * FROM skills WHERE user_id=?',(uid,)).fetchall(); evidence=conn.execute('SELECT * FROM cv_skill_evidence WHERE user_id=?',(uid,)).fetchall(); certs=conn.execute('SELECT * FROM certificates WHERE user_id=?',(uid,)).fetchall(); conn.close()
        return render_template('careerverse/portfolio.html',user=user,profile=profile,projects=projects,skills=skills,evidence=evidence,certs=certs)

    @cv.route('/mentors',methods=['GET','POST'])
    def mentors():
        if not protected(): return redirect('/login')
        if request.method=='POST':
            topic=request.form.get('topic','').strip(); message=request.form.get('message','').strip()
            if topic and len(message)>=20:
                conn=get_db(); conn.execute('INSERT INTO cv_mentor_requests(user_id,topic,message) VALUES(?,?,?)',(_uid(),topic[:120],message[:1500])); conn.commit(); conn.close(); flash('Your mentor request has been saved. A mentor is not automatically assigned in this MVP.','success'); return redirect(url_for('careerverse.mentors'))
            flash('Add a topic and a message of at least 20 characters.','error')
        conn=get_db(); rows=conn.execute('SELECT * FROM cv_mentor_requests WHERE user_id=? ORDER BY id DESC',(_uid(),)).fetchall(); conn.close()
        return render_template('careerverse/mentors.html',rows=rows)

    @cv.route('/opportunities',methods=['GET','POST'])
    def opportunities():
        if not protected(): return redirect('/login')
        if request.method=='POST':
            f=request.form; title=f.get('title','').strip()
            if title:
                conn=get_db(); conn.execute('INSERT INTO cv_saved_opportunities(user_id,title,organisation,opportunity_type,url,notes) VALUES(?,?,?,?,?,?)',(_uid(),title[:150],f.get('organisation','')[:150],f.get('opportunity_type','Learning'),f.get('url','')[:500],f.get('notes','')[:1000])); conn.commit(); conn.close(); flash('Opportunity saved to your tracker. Check the provider before sharing personal information.','success'); return redirect(url_for('careerverse.opportunities'))
        conn=get_db(); rows=conn.execute('SELECT * FROM cv_saved_opportunities WHERE user_id=? ORDER BY id DESC',(_uid(),)).fetchall(); conn.close()
        return render_template('careerverse/opportunities.html',rows=rows)

    app.register_blueprint(cv)
