import streamlit as st
import pdfplumber
import re
import spacy
import pickle
from datetime import datetime

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResumeIQ – Resume Analyzer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f;
    color: #e8e6f0;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 20% 20%, #1a0a2e 0%, #0a0a0f 50%),
                radial-gradient(ellipse at 80% 80%, #0d1a2e 0%, transparent 60%);
    min-height: 100vh;
}

[data-testid="stHeader"] { background: transparent; }
[data-testid="stToolbar"] { display: none; }
.block-container { padding: 2rem 3rem 4rem !important; max-width: 1100px !important; }

.hero {
    text-align: center;
    padding: 3.5rem 1rem 2.5rem;
}
.hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, #7c3aed22, #06b6d422);
    border: 1px solid #7c3aed55;
    color: #a78bfa;
    font-family: 'Syne', sans-serif;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 0.35rem 1rem;
    border-radius: 100px;
    margin-bottom: 1.4rem;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.4rem, 5vw, 3.8rem);
    font-weight: 800;
    line-height: 1.1;
    background: linear-gradient(135deg, #ffffff 0%, #a78bfa 50%, #38bdf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 1rem;
}
.hero p {
    color: #94a3b8;
    font-size: 1.05rem;
    font-weight: 300;
    max-width: 520px;
    margin: 0 auto;
    line-height: 1.7;
}

.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #7c3aed44, #06b6d444, transparent);
    margin: 2rem 0;
}

.glass-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.8rem;
    backdrop-filter: blur(12px);
    margin-bottom: 1.2rem;
}
.glass-card:hover { border-color: rgba(124, 58, 237, 0.35); }

.card-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #7c3aed;
    margin-bottom: 1.2rem;
}

.info-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
}
.info-item {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 1rem 1.2rem;
}
.info-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #64748b;
    margin-bottom: 0.3rem;
}
.info-value {
    font-size: 0.95rem;
    font-weight: 500;
    color: #e2e8f0;
    word-break: break-all;
}

.score-wrapper {
    display: flex;
    align-items: center;
    gap: 2rem;
    flex-wrap: wrap;
}
.score-ring-container {
    position: relative;
    width: 110px;
    height: 110px;
    flex-shrink: 0;
}
.score-ring-container svg { transform: rotate(-90deg); }
.score-center {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
.score-number {
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 800;
    color: #e2e8f0;
    line-height: 1;
}
.score-label { font-size: 0.6rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.1em; }
.score-meta { flex: 1; }
.score-meta h3 {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #e2e8f0;
    margin-bottom: 0.4rem;
}
.score-meta p { font-size: 0.85rem; color: #94a3b8; line-height: 1.6; }

.chance-high   { background: #052e16; border: 1px solid #16a34a; color: #4ade80; }
.chance-moderate { background: #1c1917; border: 1px solid #d97706; color: #fbbf24; }
.chance-low    { background: #1c0b0b; border: 1px solid #dc2626; color: #f87171; }
.chance-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    font-family: 'Syne', sans-serif;
    font-size: 0.8rem;
    font-weight: 700;
    padding: 0.4rem 1rem;
    border-radius: 100px;
    margin-bottom: 0.8rem;
    letter-spacing: 0.05em;
}

.skills-wrap { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.5rem; }
.skill-pill {
    background: linear-gradient(135deg, #7c3aed18, #06b6d418);
    border: 1px solid #7c3aed44;
    color: #c4b5fd;
    font-size: 0.78rem;
    font-weight: 500;
    padding: 0.3rem 0.85rem;
    border-radius: 100px;
}
.skill-pill-missing {
    background: rgba(239,68,68,0.08);
    border: 1px solid rgba(239,68,68,0.25);
    color: #fca5a5;
    font-size: 0.78rem;
    font-weight: 500;
    padding: 0.3rem 0.85rem;
    border-radius: 100px;
}

.tip-item {
    display: flex;
    gap: 0.75rem;
    padding: 0.75rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    align-items: flex-start;
    font-size: 0.88rem;
    color: #94a3b8;
    line-height: 1.6;
}
.tip-item:last-child { border-bottom: none; }
.tip-icon { font-size: 1rem; flex-shrink: 0; margin-top: 1px; }

.resource-link {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px;
    padding: 0.7rem 1rem;
    margin-bottom: 0.5rem;
    text-decoration: none;
    font-size: 0.85rem;
    color: #38bdf8;
}

[data-testid="stFileUploader"] {
    background: rgba(124, 58, 237, 0.05) !important;
    border: 2px dashed rgba(124, 58, 237, 0.35) !important;
    border-radius: 14px !important;
    padding: 1.5rem !important;
}
[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}
.stProgress > div > div > div {
    background: linear-gradient(90deg, #7c3aed, #06b6d4) !important;
    border-radius: 100px !important;
}

.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: #e2e8f0;
    margin-bottom: 0.8rem;
    margin-top: 0.3rem;
}

.alt-role {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px;
    padding: 0.75rem 1.1rem;
    margin-bottom: 0.5rem;
    font-size: 0.88rem;
}
.alt-role-name { color: #e2e8f0; font-weight: 500; }
.alt-role-score { color: #a78bfa; font-family: 'Syne', sans-serif; font-weight: 700; }

.footer {
    text-align: center;
    color: #334155;
    font-size: 0.78rem;
    padding: 2.5rem 0 1rem;
    letter-spacing: 0.05em;
}
</style>
""", unsafe_allow_html=True)

# ─── Load SpaCy ──────────────────────────────────────────────────────────────
@st.cache_resource
def load_spacy_model():
    try:
        return spacy.load("en_core_web_sm")
    except Exception as e:
        st.error(f"Failed to load SpaCy model: {e}")
        raise e

try:
    nlp = load_spacy_model()
except Exception:
    st.stop()

# ─── Load Pickles ────────────────────────────────────────────────────────────
try:
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('encoder.pkl', 'rb') as f:
        encoder = pickle.load(f)
    with open('category_skills.pkl', 'rb') as f:
        CATEGORY_SKILLS = pickle.load(f)
except Exception as e:
    st.error(f"Failed to load model files: {e}")
    st.stop()

CATEGORY_SKILLS.update({
    "Frontend Developer": ["HTML","CSS","JavaScript","TypeScript","React","Next.js","Vue.js","Tailwind CSS","GSAP","Framer Motion","Figma","Jest"],
    "Backend Developer": ["Node.js","Express.js","Python","Java","Go","Spring Boot","FastAPI","Flask","MongoDB","PostgreSQL","MySQL","Redis","Docker","Kubernetes","REST API","GraphQL","Pytest"],
    "Full Stack Developer": ["HTML","CSS","JavaScript","TypeScript","React","Next.js","Vue.js","Tailwind CSS","GSAP","Framer Motion","Figma","Jest","Node.js","Express.js","Python","Java","Go","Spring Boot","FastAPI","Flask","MongoDB","PostgreSQL","MySQL","Redis","Docker","Kubernetes","REST API","GraphQL","Pytest","Git","AWS","Azure","Vercel","Netlify","Zustand"]
})

ALL_SKILLS = set()
for skills in CATEGORY_SKILLS.values():
    ALL_SKILLS.update(skill.lower() for skill in skills)
ALL_SKILLS.update(['html5','css3','react.js','express.js','framer motion','next.js','tailwind css','gsap','vercel','netlify','zustand','algorithms','data structures','software engineering'])

LEARNING_RESOURCES = {
    "python":["https://www.codecademy.com/learn/learn-python","https://www.coursera.org/learn/python"],
    "sql":["https://www.w3schools.com/sql/","https://www.sqlzoo.net/"],
    "pandas":["https://pandas.pydata.org/docs/getting_started/index.html"],
    "numpy":["https://numpy.org/learn/"],
    "scikit-learn":["https://scikit-learn.org/stable/tutorial/"],
    "pytorch":["https://pytorch.org/tutorials/"],
    "tensorflow":["https://www.tensorflow.org/learn"],
    "matplotlib":["https://matplotlib.org/stable/users/index.html"],
    "seaborn":["https://seaborn.pydata.org/"],
    "tableau":["https://www.tableau.com/learn"],
    "power bi":["https://learn.microsoft.com/en-us/power-bi/"],
    "spark":["https://spark.apache.org/docs/latest/"],
    "aws":["https://aws.amazon.com/training/"],
    "gcp":["https://cloud.google.com/learn"],
    "azure":["https://learn.microsoft.com/en-us/azure/"],
    "postgresql":["https://www.postgresqltutorial.com/"],
    "mysql":["https://dev.mysql.com/doc/"],
    "mongodb":["https://www.mongodb.com/docs/"],
    "javascript":["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide"],
    "typescript":["https://www.typescriptlang.org/docs/"],
    "java":["https://www.oracle.com/java/technologies/"],
    "go":["https://go.dev/learn/"],
    "react":["https://react.dev/learn"],
    "vue.js":["https://vuejs.org/guide/"],
    "node.js":["https://nodejs.org/en/learn"],
    "spring boot":["https://spring.io/projects/spring-boot#learn"],
    "fastapi":["https://fastapi.tiangolo.com/tutorial/"],
    "flask":["https://flask.palletsprojects.com/"],
    "git":["https://git-scm.com/doc"],
    "docker":["https://docs.docker.com/get-started/"],
    "kubernetes":["https://kubernetes.io/docs/"],
    "rest api":["https://restfulapi.net/"],
    "graphql":["https://graphql.org/learn/"],
    "figma":["https://www.figma.com/resources/learn-design/"],
    "html":["https://www.w3schools.com/html/"],
    "css":["https://developer.mozilla.org/en-US/docs/Web/CSS"],
    "framer motion":["https://www.framer.com/motion/"],
    "keras":["https://keras.io/guides/"],
    "opencv":["https://opencv.org/get-started/"],
    "mlflow":["https://mlflow.org/docs/"],
    "next.js":["https://nextjs.org/learn"],
    "tailwind css":["https://tailwindcss.com/docs"],
    "express.js":["https://expressjs.com/en/starter/installing.html"]
}

CATEGORY_ICONS = {
    "Data Science":"🔬","Data Analyst":"📊","Software Development":"💻",
    "UI/UX Designer":"🎨","AI/ML":"🤖","Frontend Developer":"🖥️",
    "Backend Developer":"⚙️","Full Stack Developer":"🚀",
}

# ─── Core Functions ──────────────────────────────────────────────────────────
def extract_text_from_pdf(pdf_file):
    try:
        text = ""
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t: text += t
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""

def extract_name(text, skills_set=ALL_SKILLS):
    try:
        text = re.sub(r'[\s\r\n]+', ' ', text.strip())
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        pat = re.compile(r'^[A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]*)*$')
        for line in lines[:2]:
            if pat.match(line) and (skills_set is None or line.lower() not in skills_set):
                return line
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ == "PERSON" and (skills_set is None or ent.text.lower() not in skills_set):
                return ent.text.strip()
        return "Unknown"
    except: return "Unknown"

def extract_birth_year(text):
    try:
        m = re.search(r'\b(19|20)\d{2}\b', text)
        if m:
            age = datetime.now().year - int(m.group())
            if 15 <= age <= 100: return age
        return None
    except: return None

def extract_email(text):
    try:
        m = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', text)
        return m.group() if m else "Not found"
    except: return "Not found"

def extract_phone_number(text):
    try:
        m = re.search(r'\b(?:\+?1\s*?)?(?:\(\d{3}\)?|\d{3})[-.\s]?\d{3}[-.\s]?\d{4}\b', text)
        return m.group() if m else "Not found"
    except: return "Not found"

def extract_skills(text, target_skills):
    try:
        found = set()
        tl = text.lower()
        mappings = {"react.js":"react","html5":"html","css3":"css","framer motion":"framer motion","next.js":"next.js","tailwind css":"tailwind css","gsap":"gsap","vercel":"vercel","netlify":"netlify","zustand":"zustand","express.js":"express.js"}
        for skill in target_skills:
            pats = [r'\b' + re.escape(skill.lower()).replace(' ', r'\s*(?:,\s*|\s+|/)') + r'\b']
            if skill.lower() in mappings.values():
                for k, v in mappings.items():
                    if v == skill.lower():
                        pats.append(r'\b' + re.escape(k.lower()).replace(' ', r'\s*(?:,\s*|\s+|/)') + r'\b')
            for p in pats:
                if re.search(p, tl):
                    found.add(skill.lower()); break
        return sorted(list(found))
    except: return []

def clean_resume(t):
    try:
        t = re.sub(r'https?://\S+', '', t)
        t = re.sub(r'\S+@\S+\.\S+', '', t)
        t = re.sub(r'\b\d{10}\b', '', t)
        return t
    except: return t

def predict_category(resume_text):
    try:
        y_pred = model.predict([clean_resume(resume_text)])
        return encoder.inverse_transform(y_pred)[0]
    except: return "Unknown"

def calculate_resume_score(extracted_skills, target_skills):
    try:
        if not target_skills: return 0
        return round((len(extracted_skills) / len(target_skills)) * 100, 2)
    except: return 0

def find_best_category(resume_text, category_skills):
    try:
        best_cat, best_score, best_ext, best_tgt = None, -1, [], []
        for cat, skills in category_skills.items():
            ext = extract_skills(resume_text, skills)
            sc = calculate_resume_score(ext, skills)
            if sc > best_score:
                best_cat, best_score, best_ext, best_tgt = cat, sc, ext, skills
        if best_cat is None:
            best_cat = predict_category(resume_text)
            best_tgt = category_skills.get(best_cat, [])
            best_ext = extract_skills(resume_text, best_tgt)
            best_score = calculate_resume_score(best_ext, best_tgt)
        return best_cat, best_score, best_ext, best_tgt
    except: return "Unknown", 0, [], []

def predict_selection_chance(score, extracted_skills, target_skills, resume_text, selected_category, category_skills):
    try:
        if score > 80:
            chance, desc = "High", "Your resume closely matches the role requirements — strong chance of selection."
        elif score >= 50:
            chance, desc = "Moderate", "Competitive resume, but a few more skills could significantly improve your odds."
        else:
            chance, desc = "Low", "Your resume lacks several critical skills for this role."

        missing = [s for s in target_skills if s.lower() not in extracted_skills]
        tips = []
        if missing:
            tips.append(f"Acquire these missing skills: {', '.join(missing)}")
            tips.append("Add projects or certifications that demonstrate these skills")
        if extracted_skills:
            preview = ', '.join(extracted_skills[:5]) + ('...' if len(extracted_skills) > 5 else '')
            tips.append(f"Prominently feature your existing skills ({preview}) in a dedicated Skills section")
        tips.append("Use ATS-friendly formatting with clear headings and role-specific keywords")

        alts = []
        for cat, skills in category_skills.items():
            if cat != selected_category:
                alt_ext = extract_skills(resume_text, skills)
                alts.append((cat, calculate_resume_score(alt_ext, skills)))
        alts = sorted(alts, key=lambda x: x[1], reverse=True)[:2]

        safer = []
        if chance in ["Moderate", "Low"]:
            better = [(c, s) for c, s in alts if s > score]
            if better:
                safer.append("Consider these better-matching roles:")
                for c, s in better:
                    safer.append(f"__ALT__{c}|{s}%")
            else:
                safer.append(f"No better-matching roles found — focus on upskilling for {selected_category}")
            safer.append(f"Apply for entry-level or internship positions in {selected_category}")
            safer.append("Network with industry professionals to boost visibility")
        else:
            safer.append(f"Your profile aligns well with {selected_category} — tailor your resume to each job posting")

        return {"chance": chance, "chance_description": desc, "improvement_tips": tips, "safer_side": safer, "missing_skills": missing}
    except:
        return {"chance": "Unknown", "chance_description": "Error.", "improvement_tips": [], "safer_side": [], "missing_skills": []}

def score_ring_html(score):
    r = 44
    circ = 2 * 3.14159 * r
    offset = circ * (1 - score / 100)
    color = "#4ade80" if score > 80 else ("#fbbf24" if score >= 50 else "#f87171")
    return f"""<div class="score-ring-container">
        <svg width="110" height="110" viewBox="0 0 110 110">
            <circle cx="55" cy="55" r="{r}" fill="none" stroke="rgba(255,255,255,0.07)" stroke-width="8"/>
            <circle cx="55" cy="55" r="{r}" fill="none" stroke="{color}" stroke-width="8"
                stroke-dasharray="{circ}" stroke-dashoffset="{offset}" stroke-linecap="round"/>
        </svg>
        <div class="score-center">
            <span class="score-number">{score}%</span>
            <span class="score-label">Score</span>
        </div>
    </div>"""

# ══════════════════════════════════════════════════════════════════════════════
#  UI
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="hero">
    <div class="hero-badge">⚡ AI-Powered Resume Intelligence</div>
    <h1>ResumeIQ</h1>
    <p>Upload your resume and get instant insights — skill matching, score, and personalized career recommendations.</p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)

col_cat, col_upload = st.columns([1, 1.4], gap="large")
with col_cat:
    st.markdown('<div class="section-label">🎯 Job Category</div>', unsafe_allow_html=True)
    category_option = st.selectbox("Select a category", options=["Predict (Auto-detect)","Data Science","Data Analyst","Software Development","UI/UX Designer","AI/ML","Frontend Developer","Backend Developer","Full Stack Developer"], label_visibility="collapsed")

with col_upload:
    st.markdown('<div class="section-label">📄 Your Resume</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"], accept_multiple_files=False, label_visibility="collapsed")

if uploaded_file:
    with st.spinner("Analyzing your resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    if resume_text:
        name  = extract_name(resume_text, ALL_SKILLS)
        age   = extract_birth_year(resume_text)
        email = extract_email(resume_text)
        phone = extract_phone_number(resume_text)

        if category_option.startswith("Predict"):
            category, score, extracted_skills, target_skills = find_best_category(resume_text, CATEGORY_SKILLS)
            mode_label = "(Auto-detected)"
        else:
            category = category_option
            target_skills = CATEGORY_SKILLS.get(category, [])
            extracted_skills = extract_skills(resume_text, target_skills)
            score = calculate_resume_score(extracted_skills, target_skills)
            mode_label = "(Selected)"

        sel = predict_selection_chance(score, extracted_skills, target_skills, resume_text, category, CATEGORY_SKILLS)
        cat_icon = CATEGORY_ICONS.get(category, "💼")
        chance = sel["chance"]
        chance_class = f"chance-{chance.lower()}"
        chance_icon = "🟢" if chance == "High" else ("🟡" if chance == "Moderate" else "🔴")

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-label">📊 Analysis Results</div>', unsafe_allow_html=True)

        # Row 1
        c1, c2 = st.columns([1.1, 1], gap="large")
        with c1:
            age_row = f'<div class="info-item"><div class="info-label">Estimated Age</div><div class="info-value">{age} yrs</div></div>' if age else ''
            st.markdown(f"""<div class="glass-card">
                <div class="card-title">👤 Profile</div>
                <div class="info-grid">
                    <div class="info-item"><div class="info-label">Name</div><div class="info-value">{name}</div></div>
                    <div class="info-item"><div class="info-label">Email</div><div class="info-value">{email}</div></div>
                    <div class="info-item"><div class="info-label">Phone</div><div class="info-value">{phone}</div></div>
                    <div class="info-item"><div class="info-label">Detected Role</div><div class="info-value">{cat_icon} {category} {mode_label}</div></div>
                    {age_row}
                </div>
            </div>""", unsafe_allow_html=True)

        with c2:
            st.markdown(f"""<div class="glass-card" style="height:100%">
                <div class="card-title">🏆 Resume Score</div>
                <div class="score-wrapper">
                    {score_ring_html(score)}
                    <div class="score-meta">
                        <div class="chance-badge {chance_class}">{chance_icon} {chance} Chance</div>
                        <p>{sel['chance_description']}</p>
                        <p style="margin-top:0.5rem;font-size:0.8rem;color:#64748b">{len(extracted_skills)} of {len(target_skills)} required skills matched</p>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

        # Row 2
        c3, c4 = st.columns(2, gap="large")
        with c3:
            pills = ''.join([f'<span class="skill-pill">{s}</span>' for s in extracted_skills]) or '<span style="color:#64748b;font-size:0.85rem">No matching skills found</span>'
            st.markdown(f"""<div class="glass-card">
                <div class="card-title">✅ Matched Skills</div>
                <div class="skills-wrap">{pills}</div>
            </div>""", unsafe_allow_html=True)

        with c4:
            missing = sel["missing_skills"]
            mpills = ''.join([f'<span class="skill-pill-missing">{s}</span>' for s in missing]) or '<span style="color:#4ade80;font-size:0.85rem">🎉 All required skills matched!</span>'
            st.markdown(f"""<div class="glass-card">
                <div class="card-title">⚠️ Missing Skills</div>
                <div class="skills-wrap">{mpills}</div>
            </div>""", unsafe_allow_html=True)

        # Row 3
        c5, c6 = st.columns(2, gap="large")
        with c5:
            tips_html = ''.join([f'<div class="tip-item"><span class="tip-icon">→</span><span>{t}</span></div>' for t in sel["improvement_tips"]])
            st.markdown(f"""<div class="glass-card">
                <div class="card-title">🚀 Improvement Tips</div>
                {tips_html}
            </div>""", unsafe_allow_html=True)

        with c6:
            strategy_items = []
            for s in sel["safer_side"]:
                if s.startswith("__ALT__"):
                    parts = s.replace("__ALT__","").split("|")
                    aname, ascore = parts[0], (parts[1] if len(parts)>1 else "")
                    strategy_items.append(f'<div class="alt-role"><span class="alt-role-name">{CATEGORY_ICONS.get(aname,"💼")} {aname}</span><span class="alt-role-score">{ascore}</span></div>')
                else:
                    strategy_items.append(f'<div class="tip-item"><span class="tip-icon">→</span><span>{s}</span></div>')
            st.markdown(f"""<div class="glass-card">
                <div class="card-title">🛡️ Safer Side Strategy</div>
                {''.join(strategy_items)}
            </div>""", unsafe_allow_html=True)

        # Learning Resources
        if missing:
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="section-label">📚 Recommended Learning Resources</div>', unsafe_allow_html=True)
            seen = set()
            res_cols = st.columns(2, gap="large")
            idx = 0
            for skill in missing:
                for url in LEARNING_RESOURCES.get(skill.lower(), []):
                    if url not in seen:
                        with res_cols[idx % 2]:
                            st.markdown(f'<a class="resource-link" href="{url}" target="_blank">🔗 Learn {skill.title()}</a>', unsafe_allow_html=True)
                        seen.add(url)
                        idx += 1
    else:
        st.error("Could not extract text. Please upload a text-based (non-scanned) PDF.")

st.markdown("""
<div class="divider"></div>
<div class="footer">ResumeIQ · Powered by Machine Learning · Built with Streamlit</div>
""", unsafe_allow_html=True)