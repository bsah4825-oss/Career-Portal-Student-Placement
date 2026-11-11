from flask import Flask, render_template, request, redirect, session, jsonify
import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

# Load local .env values for Gemini and development configuration.
load_dotenv()


app = Flask(__name__)

# Secret key is read from the deployment environment.
# The fallback is only for local development.
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(32)
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.environ.get("COOKIE_SECURE", "0") == "1"
)

# Keep the SQLite database beside app.py so the path is stable
# when the app is started by Gunicorn or another server.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "database.db")


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# =========================================================
# RECRUITMENT INTELLIGENCE LAB
# =========================================================

RIL_ROUNDS = [
    {"name":"Aptitude & Logical Reasoning", "max":10, "type":"mcq", "questions":[
        {"q":"A dataset contains 200 rows. 25% are used for testing. How many rows are in the test set?","o":["25","40","50","75"],"a":2,"why":"25% of 200 is 50."},
        {"q":"Find the next number: 2, 6, 12, 20, 30, __","o":["36","40","42","44"],"a":2,"why":"The differences are 4, 6, 8, 10, then 12."},
        {"q":"If all ML engineers know Python and some Python developers know SQL, which statement must be true?","o":["All ML engineers know SQL","All ML engineers know Python","No Python developer knows SQL","All SQL developers are ML engineers"],"a":1,"why":"Only the first premise is guaranteed for every ML engineer."},
        {"q":"A model processes 120 samples in 4 seconds. At the same rate, how long for 300 samples?","o":["8 seconds","9 seconds","10 seconds","12 seconds"],"a":2,"why":"30 samples per second means 300 samples take 10 seconds."},
        {"q":"Which number is prime?","o":["21","27","29","33"],"a":2,"why":"29 has no positive divisors other than 1 and itself."},
        {"q":"A team has 5 members. Each pair reviews one another exactly once. How many unique pairs are there?","o":["5","10","15","20"],"a":1,"why":"5×4÷2 = 10 unique pairs."},
        {"q":"A task accuracy rises from 0.70 to 0.84. What is the absolute increase in percentage points?","o":["10","12","14","20"],"a":2,"why":"84% − 70% = 14 percentage points."},
        {"q":"Which value is the median of 2, 3, 7, 9, 20?","o":["3","7","8.2","9"],"a":1,"why":"The middle value in the sorted list is 7."},
        {"q":"If A takes 6 hours and B takes 3 hours to complete a task, how long working together?","o":["1 hour","2 hours","3 hours","4.5 hours"],"a":1,"why":"Combined rate is 1/6 + 1/3 = 1/2 task per hour."},
        {"q":"A fair coin is tossed twice. What is the probability of exactly one head?","o":["1/4","1/2","3/4","1"],"a":1,"why":"HT and TH are 2 of 4 equally likely outcomes."}
    ]},
    {"name":"Python Programming Challenge", "max":20, "type":"code", "prompt":"Write a Python function named `count_frequency(items)` that returns a dictionary containing the frequency of each item. Example: [1, 2, 1, 3, 2, 1] → {1: 3, 2: 2, 3: 1}. Handle an empty list.", "checks":[["def","return"],["dict","{}","frequency"],["for","items"],["get(","count("],["empty","{}"]], "hint":"Consider a dictionary and a loop. A common approach is counts[item] = counts.get(item, 0) + 1.", "note":"This first version uses transparent rubric checks, not execution of arbitrary submitted code. Do not paste secrets or personal data."},
    {"name":"Machine Learning Fundamentals", "max":20, "type":"mcq", "questions":[
        {"q":"Which task is supervised learning?","o":["Grouping customers without labels","Predicting house prices from labelled examples","Reducing dimensions without a target","Finding frequent itemsets"],"a":1,"why":"Regression learns from labelled input-output examples."},
        {"q":"What is overfitting?","o":["Poor performance on training and test data","Excellent training performance but weak generalization","A model with too few features","A missing dataset"],"a":1,"why":"Overfit models memorize training-specific patterns."},
        {"q":"Which metric is especially useful when false negatives are costly?","o":["Recall","Specificity only","R-squared","Training time"],"a":0,"why":"Recall measures the fraction of actual positives correctly identified."},
        {"q":"Which algorithm is commonly used for clustering?","o":["Linear regression","K-means","Logistic regression","Naive Bayes"],"a":1,"why":"K-means groups observations into clusters."},
        {"q":"Why split data into train and test sets?","o":["To increase row count","To estimate performance on unseen data","To remove all outliers","To guarantee 100% accuracy"],"a":1,"why":"The test set provides an independent generalization estimate."},
        {"q":"What does a confusion matrix summarize?","o":["Memory usage","Classification predictions versus actual classes","Feature scaling values","Training epochs"],"a":1,"why":"It counts true/false positives and negatives."},
        {"q":"Which technique helps prevent data leakage?","o":["Fit preprocessing only on training data","Scale the full dataset before splitting","Use test labels during tuning","Duplicate test rows"],"a":0,"why":"Learn preprocessing parameters from training data only."},
        {"q":"Which is an ensemble method based on decision trees?","o":["PCA","Random Forest","K-means","KNN"],"a":1,"why":"Random Forest combines multiple decision trees."},
        {"q":"What is the purpose of cross-validation?","o":["Estimate stability across data splits","Encrypt the dataset","Replace feature engineering","Increase class labels"],"a":0,"why":"Cross-validation evaluates performance over multiple folds."},
        {"q":"What does standardization usually do?","o":["Convert features to mean 0 and standard deviation 1","Remove every feature","Make all labels equal","Guarantee normality"],"a":0,"why":"Z-score standardization centers and scales features."}
    ]},
    {"name":"Technical Interview", "max":20, "type":"written", "questions":[
        {"q":"Explain the difference between a Python list and a tuple.","points":["mutable","immutable","ordered"]},
        {"q":"What is the difference between classification and regression? Give one example of each.","points":["classification","regression","class","continuous"]},
        {"q":"Explain overfitting and mention two ways to reduce it.","points":["overfit","generalization","regularization","cross-validation","pruning","dropout"]},
        {"q":"Why do we use Pandas and NumPy in an ML workflow?","points":["dataframe","array","numerical","data manipulation","vector"]}
    ]},
    {"name":"Practical AI/ML Case Study", "max":20, "type":"written", "questions":[
        {"q":"A college wants to identify students who may need academic support. Describe a responsible ML approach, including the target variable and possible features.","points":["target","features","historical","label","privacy","consent"]},
        {"q":"How would you handle missing values and categorical features before training a model?","points":["imput","missing","one-hot","encoding","categorical","training"]},
        {"q":"The dataset is imbalanced. Which evaluation metrics and techniques would you consider?","points":["precision","recall","f1","stratified","class weight","resampling"]},
        {"q":"How would you explain model limitations and avoid harmful decisions based on its output?","points":["bias","fairness","human","limitations","explain","monitor"]}
    ]},
    {"name":"HR & Behavioural Interview", "max":10, "type":"written", "questions":[
        {"q":"Introduce yourself and explain why you want to become an AI/ML Engineer.","points":["interest","learn","project","goal"]},
        {"q":"Describe a time you faced a difficult technical problem. How did you approach it?","points":["problem","approach","debug","solution","result"]},
        {"q":"How do you respond when a teammate disagrees with your technical decision?","points":["listen","evidence","discuss","team","compromise"]}
    ]}
]

@app.route("/recruitment-lab")
def recruitment_lab():
    if not login_required(): return redirect("/login")
    conn=get_db()
    attempts=conn.execute("SELECT * FROM recruitment_attempts WHERE user_id=? ORDER BY id DESC LIMIT 5",(session["user_id"],)).fetchall()
    latest=conn.execute("SELECT * FROM recruitment_attempts WHERE user_id=? AND status='in_progress' ORDER BY id DESC LIMIT 1",(session["user_id"],)).fetchone()
    conn.close()
    return render_template("recruitment_lab.html", attempts=attempts, latest=latest)

@app.route("/api/recruitment/start", methods=["POST"])
def recruitment_start():
    if not login_required(): return jsonify({"error":"Please log in."}),401
    conn=get_db()
    existing=conn.execute("SELECT id,current_round FROM recruitment_attempts WHERE user_id=? AND status='in_progress' ORDER BY id DESC LIMIT 1",(session["user_id"],)).fetchone()
    if existing:
        attempt_id=existing["id"]
    else:
        cur=conn.execute("INSERT INTO recruitment_attempts(user_id,target_role,difficulty) VALUES(?,?,?)",(session["user_id"],"AI/ML Engineer","Entry level"))
        attempt_id=cur.lastrowid
    conn.commit(); conn.close()
    return jsonify({"attempt_id":attempt_id,"redirect":"/recruitment-lab/session/"+str(attempt_id)})

@app.route("/recruitment-lab/session/<int:attempt_id>")
def recruitment_session(attempt_id):
    if not login_required(): return redirect("/login")
    conn=get_db(); attempt=conn.execute("SELECT * FROM recruitment_attempts WHERE id=? AND user_id=?",(attempt_id,session["user_id"])).fetchone()
    if not attempt: conn.close(); return "Attempt not found",404
    completed=conn.execute("SELECT round_no,round_name,score,max_score,feedback_json FROM recruitment_rounds WHERE attempt_id=? ORDER BY round_no",(attempt_id,)).fetchall()
    conn.close()
    return render_template("recruitment_session.html",attempt=attempt,rounds=RIL_ROUNDS,completed=completed)

def _score_written(answer, points):
    text=(answer or "").lower(); hits=[p for p in points if p.lower() in text]
    # Transparent rubric: keyword coverage + minimum answer depth; capped at full credit.
    coverage=len(hits)/max(1,len(points)); depth=min(1.0,len(text.strip())/220)
    score=round((coverage*0.75+depth*0.25)*5,2)
    return score, {"matched":hits,"missing":[p for p in points if p not in hits],"note":"Automated preliminary rubric based on concept coverage and answer depth; human review is recommended."}

@app.route("/api/recruitment/submit", methods=["POST"])
def recruitment_submit():
    if not login_required(): return jsonify({"error":"Please log in."}),401
    data=request.get_json(silent=True) or {}; attempt_id=data.get("attempt_id"); round_no=data.get("round_no"); answers=data.get("answers",{})
    if not isinstance(attempt_id,int) or not isinstance(round_no,int) or round_no<1 or round_no>6 or not isinstance(answers,dict): return jsonify({"error":"Invalid submission."}),400
    conn=get_db(); attempt=conn.execute("SELECT * FROM recruitment_attempts WHERE id=? AND user_id=? AND status='in_progress'",(attempt_id,session["user_id"])).fetchone()
    if not attempt: conn.close(); return jsonify({"error":"Active attempt not found."}),404
    if round_no != attempt["current_round"]:
        conn.close(); return jsonify({"error":"Complete the rounds in sequence."}),409
    prior=conn.execute("SELECT id FROM recruitment_rounds WHERE attempt_id=? AND round_no=?",(attempt_id,round_no)).fetchone()
    if prior: conn.close(); return jsonify({"error":"This round has already been submitted."}),409
    spec=RIL_ROUNDS[round_no-1]; score=0; feedback=[]
    if spec["type"]=="mcq":
        for i,q in enumerate(spec["questions"]):
            try: chosen=int(answers.get(str(i),-1))
            except: chosen=-1
            correct=chosen==q["a"]; score+=1 if correct else 0
            feedback.append({"question":q["q"],"correct":correct,"explanation":q["why"],"selected":chosen,"correct_option":q["a"]})
    elif spec["type"]=="code":
        code=str(answers.get("code",""))[:12000]
        for idx,group in enumerate(spec["checks"]):
            found=any(term.lower() in code.lower() for term in group)
            score+=4 if found else 0
            feedback.append({"criterion":f"Code rubric {idx+1}","met":found,"expected":"At least one relevant construct: "+", ".join(group)})
        feedback.append({"note":spec["note"]})
    else:
        for i,q in enumerate(spec["questions"]):
            answer=str(answers.get(str(i),""))[:5000]
            part,fb=_score_written(answer,q["points"]); score+=part
            feedback.append({"question":q["q"],"score":part,"max":5,"feedback":fb})
    score=round(min(score,spec["max"]),2)
    conn.execute("INSERT INTO recruitment_rounds(attempt_id,round_no,round_name,score,max_score,response_json,feedback_json) VALUES(?,?,?,?,?,?,?)",(attempt_id,round_no,spec["name"],score,spec["max"],__import__('json').dumps(answers),__import__('json').dumps(feedback)))
    total=conn.execute("SELECT COALESCE(SUM(score),0) FROM recruitment_rounds WHERE attempt_id=?",(attempt_id,)).fetchone()[0]
    done=round_no==6
    conn.execute("UPDATE recruitment_attempts SET current_round=?,total_score=?,status=?,completed_at=CASE WHEN ? THEN CURRENT_TIMESTAMP ELSE completed_at END WHERE id=?",(min(round_no+1,6),total,"completed" if done else "in_progress",1 if done else 0,attempt_id))
    conn.commit(); conn.close()
    return jsonify({"score":score,"max_score":spec["max"],"total_score":total,"feedback":feedback,"completed":done,"next_round":round_no+1})

@app.route("/api/recruitment/result/<int:attempt_id>")
def recruitment_result(attempt_id):
    if not login_required(): return jsonify({"error":"Please log in."}),401
    conn=get_db(); attempt=conn.execute("SELECT * FROM recruitment_attempts WHERE id=? AND user_id=?",(attempt_id,session["user_id"])).fetchone()
    if not attempt: conn.close(); return jsonify({"error":"Not found"}),404
    rounds=conn.execute("SELECT round_no,round_name,score,max_score,feedback_json FROM recruitment_rounds WHERE attempt_id=? ORDER BY round_no",(attempt_id,)).fetchall(); conn.close()
    return jsonify({"attempt":dict(attempt),"rounds":[dict(r) for r in rounds]})

# =========================================================
# DATABASE INITIALIZATION
# =========================================================

def init_db():

    conn = get_db()

    # =====================================================
    # USERS TABLE
    # =====================================================

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            registration_no TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            department TEXT NOT NULL,
            year INTEGER NOT NULL,
            phone TEXT DEFAULT '',
            career_role TEXT DEFAULT '',
            bio TEXT DEFAULT '',
            github TEXT DEFAULT '',
            linkedin TEXT DEFAULT ''
        )
    """)

    # Check existing user columns
    user_cols = {
        row["name"]
        for row in conn.execute("PRAGMA table_info(users)").fetchall()
    }

    # Add missing career/profile columns
    user_columns = {
        "phone": "TEXT DEFAULT ''",
        "career_role": "TEXT DEFAULT ''",
        "bio": "TEXT DEFAULT ''",
        "github": "TEXT DEFAULT ''",
        "linkedin": "TEXT DEFAULT ''"
    }

    for column_name, column_type in user_columns.items():

        if column_name not in user_cols:

            conn.execute(
                f"ALTER TABLE users ADD COLUMN {column_name} {column_type}"
            )

    # =====================================================
    # SKILLS TABLE
    # =====================================================

    conn.execute("""
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            category TEXT DEFAULT 'Other',
            progress INTEGER DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    skill_cols = {
        row["name"]
        for row in conn.execute("PRAGMA table_info(skills)").fetchall()
    }

    if "category" not in skill_cols:

        conn.execute(
            "ALTER TABLE skills ADD COLUMN category TEXT DEFAULT 'Other'"
        )

    # =====================================================
    # DSA TABLE
    # =====================================================

    conn.execute("""
        CREATE TABLE IF NOT EXISTS dsa_problems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            problem_name TEXT NOT NULL,
            platform TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # =====================================================
    # CERTIFICATES TABLE
    # =====================================================

    conn.execute("""
        CREATE TABLE IF NOT EXISTS certificates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            provider TEXT NOT NULL,
            category TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # =====================================================
    # INTERNSHIPS TABLE
    # =====================================================

    conn.execute("""
        CREATE TABLE IF NOT EXISTS internships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            status TEXT NOT NULL,
            application_date TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    # =====================================================
    # RECRUITMENT INTELLIGENCE LAB
    # =====================================================
    conn.execute("""CREATE TABLE IF NOT EXISTS recruitment_attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        target_role TEXT NOT NULL DEFAULT 'AI/ML Engineer',
        difficulty TEXT NOT NULL DEFAULT 'Entry level',
        current_round INTEGER NOT NULL DEFAULT 1,
        status TEXT NOT NULL DEFAULT 'in_progress',
        total_score REAL NOT NULL DEFAULT 0,
        max_score REAL NOT NULL DEFAULT 100,
        started_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        completed_at TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS recruitment_rounds (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        attempt_id INTEGER NOT NULL,
        round_no INTEGER NOT NULL,
        round_name TEXT NOT NULL,
        score REAL NOT NULL DEFAULT 0,
        max_score REAL NOT NULL,
        response_json TEXT NOT NULL DEFAULT '{}',
        feedback_json TEXT NOT NULL DEFAULT '[]',
        submitted_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(attempt_id, round_no),
        FOREIGN KEY(attempt_id) REFERENCES recruitment_attempts(id) ON DELETE CASCADE
    )""")

    conn.commit()
    conn.close()


# =========================================================
# LOGIN CHECK
# =========================================================

def login_required():

    return "user_id" in session


# =========================================================
# DASHBOARD
# STEP 7 - PLACEMENT READINESS SYSTEM
# =========================================================

@app.route("/")
def home():

    if not login_required():
        return redirect("/login")

    user_id = session["user_id"]

    conn = get_db()

    # =====================================================
    # CURRENT USER
    # =====================================================

    user = conn.execute("""
        SELECT *
        FROM users
        WHERE id = ?
    """, (user_id,)).fetchone()

    # =====================================================
    # USER DATA
    # =====================================================

    skills = conn.execute("""
        SELECT *
        FROM skills
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,)).fetchall()

    problems = conn.execute("""
        SELECT *
        FROM dsa_problems
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,)).fetchall()

    certificates = conn.execute("""
        SELECT *
        FROM certificates
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,)).fetchall()

    internships = conn.execute("""
        SELECT *
        FROM internships
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,)).fetchall()

    # =====================================================
    # DSA STATISTICS
    # =====================================================

    solved_count = conn.execute("""
        SELECT COUNT(*)
        FROM dsa_problems
        WHERE user_id = ?
        AND status = 'Solved'
    """, (user_id,)).fetchone()[0]

    attempted_count = conn.execute("""
        SELECT COUNT(*)
        FROM dsa_problems
        WHERE user_id = ?
        AND status != 'Solved'
    """, (user_id,)).fetchone()[0]

    easy_count = conn.execute("""
        SELECT COUNT(*)
        FROM dsa_problems
        WHERE user_id = ?
        AND difficulty = 'Easy'
        AND status = 'Solved'
    """, (user_id,)).fetchone()[0]

    medium_count = conn.execute("""
        SELECT COUNT(*)
        FROM dsa_problems
        WHERE user_id = ?
        AND difficulty = 'Medium'
        AND status = 'Solved'
    """, (user_id,)).fetchone()[0]

    hard_count = conn.execute("""
        SELECT COUNT(*)
        FROM dsa_problems
        WHERE user_id = ?
        AND difficulty = 'Hard'
        AND status = 'Solved'
    """, (user_id,)).fetchone()[0]

    total_problems = solved_count + attempted_count

    # =====================================================
    # CERTIFICATE STATISTICS
    # =====================================================

    certificate_count = len(certificates)

    # =====================================================
    # INTERNSHIP STATISTICS
    # =====================================================

    internship_count = len(internships)

    applied_count = conn.execute("""
        SELECT COUNT(*)
        FROM internships
        WHERE user_id = ?
        AND status = 'Applied'
    """, (user_id,)).fetchone()[0]

    interview_count = conn.execute("""
        SELECT COUNT(*)
        FROM internships
        WHERE user_id = ?
        AND status = 'Interview'
    """, (user_id,)).fetchone()[0]

    selected_count = conn.execute("""
        SELECT COUNT(*)
        FROM internships
        WHERE user_id = ?
        AND status = 'Selected'
    """, (user_id,)).fetchone()[0]

    rejected_count = conn.execute("""
        SELECT COUNT(*)
        FROM internships
        WHERE user_id = ?
        AND status = 'Rejected'
    """, (user_id,)).fetchone()[0]

    saved_count = conn.execute("""
        SELECT COUNT(*)
        FROM internships
        WHERE user_id = ?
        AND status = 'Saved'
    """, (user_id,)).fetchone()[0]

    # =====================================================
    # PLACEMENT READINESS COMPONENTS
    # =====================================================

    # -----------------------------------------------------
    # SKILLS
    # -----------------------------------------------------

    if skills:

        skill_progress = round(
            sum(
                int(skill["progress"] or 0)
                for skill in skills
            ) / len(skills)
        )

    else:

        skill_progress = 0

    skill_progress = max(0, min(skill_progress, 100))

    # -----------------------------------------------------
    # DSA
    #
    # 50 solved problems = 100%
    # -----------------------------------------------------

    dsa_progress = min(
        solved_count * 2,
        100
    )

    # -----------------------------------------------------
    # CERTIFICATES
    #
    # 10 certificates = 100%
    # -----------------------------------------------------

    certificate_progress = min(
        certificate_count * 10,
        100
    )

    # -----------------------------------------------------
    # INTERNSHIPS
    #
    # 5 tracked internships = 100%
    # -----------------------------------------------------

    internship_progress = min(
        internship_count * 20,
        100
    )

    # =====================================================
    # WEIGHTED PLACEMENT READINESS
    # =====================================================
    #
    # Skills       = 30%
    # DSA          = 30%
    # Certificates = 15%
    # Internships  = 25%
    #
    # Total        = 100%
    # =====================================================

    placement_readiness = round(
        (skill_progress * 0.30)
        + (dsa_progress * 0.30)
        + (certificate_progress * 0.15)
        + (internship_progress * 0.25)
    )

    placement_readiness = max(
        0,
        min(placement_readiness, 100)
    )

    # =====================================================
    # RECENT DATA
    # =====================================================

    recent_internships = conn.execute("""
        SELECT *
        FROM internships
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 5
    """, (user_id,)).fetchall()

    recent_certificates = conn.execute("""
        SELECT *
        FROM certificates
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 5
    """, (user_id,)).fetchall()

    conn.close()

    # =====================================================
    # DASHBOARD
    # =====================================================

    return render_template(
        "index.html",

        user=user,

        skills=skills,
        problems=problems,
        certificates=certificates,
        internships=internships,

        recent_internships=recent_internships,
        recent_certificates=recent_certificates,

        solved_count=solved_count,
        attempted_count=attempted_count,
        total_problems=total_problems,

        easy_count=easy_count,
        medium_count=medium_count,
        hard_count=hard_count,

        certificate_count=certificate_count,

        internship_count=internship_count,

        applied_count=applied_count,
        interview_count=interview_count,
        selected_count=selected_count,
        rejected_count=rejected_count,
        saved_count=saved_count,

        # Readiness components
        skill_progress=skill_progress,
        dsa_progress=dsa_progress,
        certificate_progress=certificate_progress,
        internship_progress=internship_progress,

        # Overall readiness
        placement_readiness=placement_readiness
    )


# =========================================================
# REGISTER
# =========================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        registration_no = request.form["registration_no"].strip()
        name = request.form["name"].strip()
        email = request.form["email"].strip()
        password = request.form["password"]
        department = request.form["department"]
        year = request.form["year"]

        if (
            not registration_no
            or not name
            or not email
            or not password
        ):

            return render_template(
                "register.html",
                error="Please fill all required fields."
            )

        try:

            conn = get_db()

            conn.execute("""
                INSERT INTO users
                (
                    registration_no,
                    name,
                    email,
                    password_hash,
                    department,
                    year
                )

                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                registration_no,
                name,
                email,
                generate_password_hash(password),
                department,
                year
            ))

            conn.commit()
            conn.close()

            return redirect("/login")

        except sqlite3.IntegrityError:

            return render_template(
                "register.html",
                error="Registration number or email already exists."
            )

    return render_template("register.html")


# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        registration_no = request.form["registration_no"].strip()
        password = request.form["password"]

        conn = get_db()

        user = conn.execute("""
            SELECT *
            FROM users
            WHERE registration_no = ?
        """, (registration_no,)).fetchone()

        conn.close()

        if (
            user
            and check_password_hash(
                user["password_hash"],
                password
            )
        ):

            session["user_id"] = user["id"]

            return redirect("/")

        return render_template(
            "login.html",
            error="Invalid registration number or password."
        )

    return render_template("login.html")


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# =========================================================
# PROFILE
# =========================================================

@app.route("/profile")
def profile():

    if not login_required():
        return redirect("/login")

    user_id = session["user_id"]

    conn = get_db()

    user = conn.execute("""
        SELECT *
        FROM users
        WHERE id = ?
    """, (user_id,)).fetchone()

    skills = conn.execute("""
        SELECT *
        FROM skills
        WHERE user_id = ?
    """, (user_id,)).fetchall()

    solved_count = conn.execute("""
        SELECT COUNT(*)
        FROM dsa_problems
        WHERE user_id = ?
        AND status = 'Solved'
    """, (user_id,)).fetchone()[0]

    certificate_count = conn.execute("""
        SELECT COUNT(*)
        FROM certificates
        WHERE user_id = ?
    """, (user_id,)).fetchone()[0]

    internship_count = conn.execute("""
        SELECT COUNT(*)
        FROM internships
        WHERE user_id = ?
    """, (user_id,)).fetchone()[0]

    conn.close()

    # =====================================================
    # PROFILE PROGRESS
    # =====================================================

    if skills:

        skill_progress = round(
            sum(
                int(skill["progress"] or 0)
                for skill in skills
            ) / len(skills)
        )

    else:

        skill_progress = 0

    skill_progress = max(
        0,
        min(skill_progress, 100)
    )

    dsa_score = min(
        solved_count * 2,
        100
    )

    certificate_score = min(
        certificate_count * 10,
        100
    )

    internship_score = min(
        internship_count * 20,
        100
    )

    # Same weighted model as dashboard
    overall_progress = round(
        (skill_progress * 0.30)
        + (dsa_score * 0.30)
        + (certificate_score * 0.15)
        + (internship_score * 0.25)
    )

    return render_template(
        "profile.html",

        user=user,

        skill_progress=skill_progress,
        dsa_score=dsa_score,
        certificate_score=certificate_score,
        internship_score=internship_score,

        overall_progress=overall_progress,

        solved_count=solved_count,
        certificate_count=certificate_count,
        internship_count=internship_count
    )


# =========================================================
# UPDATE PROFILE
# =========================================================

@app.route("/update-profile", methods=["POST"])
def update_profile():

    if not login_required():
        return redirect("/login")

    user_id = session["user_id"]

    # =====================================================
    # PERSONAL INFORMATION FORM
    # =====================================================

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    department = request.form.get("department", "").strip()
    year = request.form.get("year", "").strip()

    # =====================================================
    # CAREER INFORMATION FORM
    # =====================================================

    career_role = request.form.get(
        "career_role",
        ""
    ).strip()

    github = request.form.get(
        "github",
        ""
    ).strip()

    linkedin = request.form.get(
        "linkedin",
        ""
    ).strip()

    phone = request.form.get(
        "phone",
        ""
    ).strip()

    bio = request.form.get(
        "bio",
        ""
    ).strip()

    # =====================================================
    # DATABASE
    # =====================================================

    conn = get_db()

    try:

        # -------------------------------------------------
        # If personal information was submitted
        # -------------------------------------------------

        if name or email or department or year:

            if not name or not email:

                conn.close()

                return redirect("/profile")

            conn.execute("""
                UPDATE users

                SET
                    name = ?,
                    email = ?,
                    department = ?,
                    year = ?

                WHERE id = ?
            """, (
                name,
                email,
                department,
                year,
                user_id
            ))

        # -------------------------------------------------
        # If career information was submitted
        # -------------------------------------------------

        if any([
            "career_role" in request.form,
            "github" in request.form,
            "linkedin" in request.form,
            "phone" in request.form,
            "bio" in request.form
        ]):

            conn.execute("""
                UPDATE users

                SET
                    career_role = ?,
                    github = ?,
                    linkedin = ?,
                    phone = ?,
                    bio = ?

                WHERE id = ?
            """, (
                career_role,
                github,
                linkedin,
                phone,
                bio,
                user_id
            ))

        conn.commit()
        conn.close()

        return redirect(
            "/profile?profile_success=1"
        )

    except sqlite3.IntegrityError:

        conn.close()

        return redirect(
            "/profile?error=email_exists"
        )


# =========================================================
# CHANGE PASSWORD
# =========================================================

@app.route("/change-password", methods=["POST"])
def change_password():

    if not login_required():
        return redirect("/login")

    user_id = session["user_id"]

    current_password = request.form["current_password"]

    new_password = request.form["new_password"]

    confirm_password = request.form["confirm_password"]

    conn = get_db()

    user = conn.execute("""
        SELECT *
        FROM users
        WHERE id = ?
    """, (user_id,)).fetchone()

    # Check current password
    if (
        not user
        or not check_password_hash(
            user["password_hash"],
            current_password
        )
    ):

        conn.close()

        return redirect(
            "/profile?password_error=wrong_current"
        )

    # Check confirmation
    if new_password != confirm_password:

        conn.close()

        return redirect(
            "/profile?password_error=mismatch"
        )

    # Minimum password length
    if len(new_password) < 6:

        conn.close()

        return redirect(
            "/profile?password_error=short"
        )

    # Hash password
    new_password_hash = generate_password_hash(
        new_password
    )

    conn.execute("""
        UPDATE users

        SET password_hash = ?

        WHERE id = ?
    """, (
        new_password_hash,
        user_id
    ))

    conn.commit()
    conn.close()

    return redirect(
        "/profile?password_success=1"
    )


# =========================================================
# SKILLS PAGE
# =========================================================

@app.route("/skills")
def skills_page():

    if not login_required():
        return redirect("/login")

    user_id = session["user_id"]

    conn = get_db()

    user = conn.execute("""
        SELECT *
        FROM users
        WHERE id = ?
    """, (user_id,)).fetchone()

    skills = conn.execute("""
        SELECT *
        FROM skills
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,)).fetchall()

    # Average progress
    if skills:

        average_progress = round(
            sum(
                int(skill["progress"] or 0)
                for skill in skills
            ) / len(skills)
        )

    else:

        average_progress = 0

    programming_count = conn.execute("""
        SELECT COUNT(*)
        FROM skills
        WHERE user_id = ?
        AND category = 'Programming'
    """, (user_id,)).fetchone()[0]

    web_count = conn.execute("""
        SELECT COUNT(*)
        FROM skills
        WHERE user_id = ?
        AND category = 'Web Development'
    """, (user_id,)).fetchone()[0]

    database_count = conn.execute("""
        SELECT COUNT(*)
        FROM skills
        WHERE user_id = ?
        AND category = 'Database'
    """, (user_id,)).fetchone()[0]

    conn.close()

    return render_template(
        "skills.html",

        user=user,
        skills=skills,

        average_progress=average_progress,

        programming_count=programming_count,
        web_count=web_count,
        database_count=database_count
    )


# =========================================================
# ADD SKILL
# =========================================================

@app.route("/add-skill", methods=["POST"])
def add_skill():

    if not login_required():
        return redirect("/login")

    user_id = session["user_id"]

    skill = request.form.get(
        "skill",
        ""
    ).strip()

    category = request.form.get(
        "category",
        "Other"
    ).strip()

    try:

        progress = int(
            request.form.get(
                "progress",
                0
            )
        )

    except ValueError:

        progress = 0

    progress = max(
        0,
        min(progress, 100)
    )

    if skill:

        conn = get_db()

        conn.execute("""
            INSERT INTO skills
            (
                user_id,
                name,
                category,
                progress
            )

            VALUES (?, ?, ?, ?)
        """, (
            user_id,
            skill,
            category,
            progress
        ))

        conn.commit()
        conn.close()

    return redirect("/skills")


# =========================================================
# UPDATE SKILL
# =========================================================

@app.route("/update-skill/<int:id>", methods=["POST"])
def update_skill(id):

    if not login_required():
        return redirect("/login")

    user_id = session["user_id"]

    skill = request.form.get(
        "skill",
        ""
    ).strip()

    category = request.form.get(
        "category",
        "Other"
    ).strip()

    try:

        progress = int(
            request.form.get(
                "progress",
                0
            )
        )

    except ValueError:

        progress = 0

    progress = max(
        0,
        min(progress, 100)
    )

    if skill:

        conn = get_db()

        conn.execute("""
            UPDATE skills

            SET
                name = ?,
                category = ?,
                progress = ?

            WHERE id = ?
            AND user_id = ?
        """, (
            skill,
            category,
            progress,
            id,
            user_id
        ))

        conn.commit()
        conn.close()

    return redirect("/skills")


# =========================================================
# DELETE SKILL
# =========================================================

@app.route("/delete-skill/<int:id>")
def delete_skill(id):

    if not login_required():
        return redirect("/login")

    conn = get_db()

    conn.execute("""
        DELETE FROM skills

        WHERE id = ?
        AND user_id = ?
    """, (
        id,
        session["user_id"]
    ))

    conn.commit()
    conn.close()

    return redirect("/skills")


# =========================================================
# DSA PAGE
# =========================================================

@app.route("/dsa")
def dsa_page():

    if not login_required():
        return redirect("/login")

    user_id = session["user_id"]

    conn = get_db()

    user = conn.execute("""
        SELECT *
        FROM users
        WHERE id = ?
    """, (user_id,)).fetchone()

    problems = conn.execute("""
        SELECT *
        FROM dsa_problems
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,)).fetchall()

    total_count = conn.execute("""
        SELECT COUNT(*)
        FROM dsa_problems
        WHERE user_id = ?
    """, (user_id,)).fetchone()[0]

    solved_count = conn.execute("""
        SELECT COUNT(*)
        FROM dsa_problems
        WHERE user_id = ?
        AND status = 'Solved'
    """, (user_id,)).fetchone()[0]

    attempted_count = conn.execute("""
        SELECT COUNT(*)
        FROM dsa_problems
        WHERE user_id = ?
        AND status = 'Attempted'
    """, (user_id,)).fetchone()[0]

    easy_count = conn.execute("""
        SELECT COUNT(*)
        FROM dsa_problems
        WHERE user_id = ?
        AND difficulty = 'Easy'
        AND status = 'Solved'
    """, (user_id,)).fetchone()[0]

    medium_count = conn.execute("""
        SELECT COUNT(*)
        FROM dsa_problems
        WHERE user_id = ?
        AND difficulty = 'Medium'
        AND status = 'Solved'
    """, (user_id,)).fetchone()[0]

    hard_count = conn.execute("""
        SELECT COUNT(*)
        FROM dsa_problems
        WHERE user_id = ?
        AND difficulty = 'Hard'
        AND status = 'Solved'
    """, (user_id,)).fetchone()[0]

    conn.close()

    if total_count:

        solving_progress = int(
            (solved_count / total_count) * 100
        )

    else:

        solving_progress = 0

    return render_template(
        "dsa.html",

        user=user,
        problems=problems,

        total_count=total_count,
        solved_count=solved_count,
        attempted_count=attempted_count,

        easy_count=easy_count,
        medium_count=medium_count,
        hard_count=hard_count,

        solving_progress=solving_progress
    )


# =========================================================
# ADD DSA PROBLEM
# =========================================================

@app.route("/add-problem", methods=["POST"])
def add_problem():

    if not login_required():
        return redirect("/login")

    user_id = session["user_id"]

    problem_name = request.form[
        "problem_name"
    ].strip()

    platform = request.form[
        "platform"
    ]

    difficulty = request.form[
        "difficulty"
    ]

    status = request.form[
        "status"
    ]

    if problem_name:

        conn = get_db()

        conn.execute("""
            INSERT INTO dsa_problems
            (
                user_id,
                problem_name,
                platform,
                difficulty,
                status
            )

            VALUES (?, ?, ?, ?, ?)
        """, (
            user_id,
            problem_name,
            platform,
            difficulty,
            status
        ))

        conn.commit()
        conn.close()

    return redirect("/dsa")


# =========================================================
# UPDATE DSA PROBLEM
# =========================================================

@app.route("/update-problem/<int:id>", methods=["POST"])
def update_problem(id):

    if not login_required():
        return redirect("/login")

    conn = get_db()

    conn.execute("""
        UPDATE dsa_problems

        SET
            problem_name = ?,
            platform = ?,
            difficulty = ?,
            status = ?

        WHERE id = ?
        AND user_id = ?
    """, (
        request.form["problem_name"].strip(),
        request.form["platform"],
        request.form["difficulty"],
        request.form["status"],
        id,
        session["user_id"]
    ))

    conn.commit()
    conn.close()

    return redirect("/dsa")


# =========================================================
# DELETE DSA PROBLEM
# =========================================================

@app.route("/delete-problem/<int:id>")
def delete_problem(id):

    if not login_required():
        return redirect("/login")

    conn = get_db()

    conn.execute("""
        DELETE FROM dsa_problems

        WHERE id = ?
        AND user_id = ?
    """, (
        id,
        session["user_id"]
    ))

    conn.commit()
    conn.close()

    return redirect("/dsa")


# =========================================================
# CERTIFICATES PAGE
# =========================================================

@app.route("/certificates")
def certificates_page():

    if not login_required():
        return redirect("/login")

    user_id = session["user_id"]

    conn = get_db()

    user = conn.execute("""
        SELECT *
        FROM users
        WHERE id = ?
    """, (user_id,)).fetchone()

    certificates = conn.execute("""
        SELECT *
        FROM certificates
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,)).fetchall()

    total_certificates = conn.execute("""
        SELECT COUNT(*)
        FROM certificates
        WHERE user_id = ?
    """, (user_id,)).fetchone()[0]

    programming_certificates = conn.execute("""
        SELECT COUNT(*)
        FROM certificates
        WHERE user_id = ?
        AND category = 'Programming'
    """, (user_id,)).fetchone()[0]

    web_certificates = conn.execute("""
        SELECT COUNT(*)
        FROM certificates
        WHERE user_id = ?
        AND category = 'Web Development'
    """, (user_id,)).fetchone()[0]

    data_certificates = conn.execute("""
        SELECT COUNT(*)
        FROM certificates
        WHERE user_id = ?
        AND category = 'Data / AI'
    """, (user_id,)).fetchone()[0]

    other_certificates = conn.execute("""
        SELECT COUNT(*)
        FROM certificates
        WHERE user_id = ?
        AND category = 'Other'
    """, (user_id,)).fetchone()[0]

    conn.close()

    return render_template(
        "certificates.html",

        user=user,
        certificates=certificates,

        total_certificates=total_certificates,

        programming_certificates=programming_certificates,
        web_certificates=web_certificates,
        data_certificates=data_certificates,
        other_certificates=other_certificates
    )


# =========================================================
# ADD CERTIFICATE
# =========================================================

@app.route("/add-certificate", methods=["POST"])
def add_certificate():

    if not login_required():
        return redirect("/login")

    certificate_name = request.form[
        "certificate_name"
    ].strip()

    provider = request.form[
        "provider"
    ].strip()

    category = request.form[
        "category"
    ]

    if certificate_name and provider:

        conn = get_db()

        conn.execute("""
            INSERT INTO certificates
            (
                user_id,
                name,
                provider,
                category
            )

            VALUES (?, ?, ?, ?)
        """, (
            session["user_id"],
            certificate_name,
            provider,
            category
        ))

        conn.commit()
        conn.close()

    return redirect("/certificates")


# =========================================================
# UPDATE CERTIFICATE
# =========================================================

@app.route("/update-certificate/<int:id>", methods=["POST"])
def update_certificate(id):

    if not login_required():
        return redirect("/login")

    conn = get_db()

    conn.execute("""
        UPDATE certificates

        SET
            name = ?,
            provider = ?,
            category = ?

        WHERE id = ?
        AND user_id = ?
    """, (
        request.form["certificate_name"].strip(),
        request.form["provider"].strip(),
        request.form["category"],
        id,
        session["user_id"]
    ))

    conn.commit()
    conn.close()

    return redirect("/certificates")


# =========================================================
# DELETE CERTIFICATE
# =========================================================

@app.route("/delete-certificate/<int:id>")
def delete_certificate(id):

    if not login_required():
        return redirect("/login")

    conn = get_db()

    conn.execute("""
        DELETE FROM certificates

        WHERE id = ?
        AND user_id = ?
    """, (
        id,
        session["user_id"]
    ))

    conn.commit()
    conn.close()

    return redirect("/certificates")


# =========================================================
# INTERNSHIPS PAGE
# =========================================================

@app.route("/internships")
def internships_page():

    if not login_required():
        return redirect("/login")

    user_id = session["user_id"]

    conn = get_db()

    user = conn.execute("""
        SELECT *
        FROM users
        WHERE id = ?
    """, (user_id,)).fetchone()

    internships = conn.execute("""
        SELECT *
        FROM internships
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,)).fetchall()

    total_internships = conn.execute("""
        SELECT COUNT(*)
        FROM internships
        WHERE user_id = ?
    """, (user_id,)).fetchone()[0]

    applied_count = conn.execute("""
        SELECT COUNT(*)
        FROM internships
        WHERE user_id = ?
        AND status = 'Applied'
    """, (user_id,)).fetchone()[0]

    interview_count = conn.execute("""
        SELECT COUNT(*)
        FROM internships
        WHERE user_id = ?
        AND status = 'Interview'
    """, (user_id,)).fetchone()[0]

    selected_count = conn.execute("""
        SELECT COUNT(*)
        FROM internships
        WHERE user_id = ?
        AND status = 'Selected'
    """, (user_id,)).fetchone()[0]

    rejected_count = conn.execute("""
        SELECT COUNT(*)
        FROM internships
        WHERE user_id = ?
        AND status = 'Rejected'
    """, (user_id,)).fetchone()[0]

    saved_count = conn.execute("""
        SELECT COUNT(*)
        FROM internships
        WHERE user_id = ?
        AND status = 'Saved'
    """, (user_id,)).fetchone()[0]

    conn.close()

    return render_template(
        "internships.html",

        user=user,
        internships=internships,

        total_internships=total_internships,

        applied_count=applied_count,
        interview_count=interview_count,
        selected_count=selected_count,
        rejected_count=rejected_count,
        saved_count=saved_count
    )


# =========================================================
# ADD INTERNSHIP
# =========================================================

@app.route("/add-internship", methods=["POST"])
def add_internship():

    if not login_required():
        return redirect("/login")

    company = request.form[
        "company"
    ].strip()

    role = request.form[
        "role"
    ].strip()

    status = request.form[
        "status"
    ]

    application_date = request.form.get(
        "application_date",
        ""
    )

    if company and role:

        conn = get_db()

        conn.execute("""
            INSERT INTO internships
            (
                user_id,
                company,
                role,
                status,
                application_date
            )

            VALUES (?, ?, ?, ?, ?)
        """, (
            session["user_id"],
            company,
            role,
            status,
            application_date
        ))

        conn.commit()
        conn.close()

    return redirect("/internships")


# =========================================================
# UPDATE INTERNSHIP
# =========================================================

@app.route("/update-internship/<int:id>", methods=["POST"])
def update_internship(id):

    if not login_required():
        return redirect("/login")

    company = request.form[
        "company"
    ].strip()

    role = request.form[
        "role"
    ].strip()

    status = request.form[
        "status"
    ]

    application_date = request.form.get(
        "application_date",
        ""
    )

    if company and role:

        conn = get_db()

        conn.execute("""
            UPDATE internships

            SET
                company = ?,
                role = ?,
                status = ?,
                application_date = ?

            WHERE id = ?
            AND user_id = ?
        """, (
            company,
            role,
            status,
            application_date,
            id,
            session["user_id"]
        ))

        conn.commit()
        conn.close()

    return redirect("/internships")


# =========================================================
# DELETE INTERNSHIP
# =========================================================

@app.route("/delete-internship/<int:id>")
def delete_internship(id):

    if not login_required():
        return redirect("/login")

    conn = get_db()

    conn.execute("""
        DELETE FROM internships

        WHERE id = ?
        AND user_id = ?
    """, (
        id,
        session["user_id"]
    ))

    conn.commit()
    conn.close()

    return redirect("/internships")


# =========================================================
# SETTINGS
# =========================================================

@app.route("/settings")
def settings():

    if not login_required():
        return redirect("/login")

    conn = get_db()

    user = conn.execute("""
        SELECT *
        FROM users
        WHERE id = ?
    """, (session["user_id"],)).fetchone()

    conn.close()

    return render_template(
        "settings.html",
        user=user
    )


# The Recruitment Intelligence Lab question bank and routes are defined above.

# Recruitment routes are defined once above; keep the original handlers.

# =========================================================
# CAREERVERSE EXTENSION (preserves the existing portal)
# =========================================================
from careerverse_features import register_careerverse
register_careerverse(app, get_db, login_required)

# =========================================================
# DATABASE INITIALIZATION
# =========================================================
# Run when the module loads so Gunicorn also initializes
# the database/tables before serving requests.
init_db()


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=os.environ.get("FLASK_DEBUG", "0") == "1"
    )
