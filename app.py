import streamlit as st
import recommender_engine as re
import time

# Page configuration
st.set_page_config(
    page_title="Internship Finder",
    layout="wide",
    page_icon="💼",
    initial_sidebar_state="collapsed"
)

# ---------- CUSTOM CSS (Apple-style UI with a new look) ----------
st.markdown("""
<style>
/* New font for a more creative look */
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
* {
    font-family: 'Montserrat', sans-serif;
}

/* Page fade-in */
.stApp {
    animation: pageFadeIn 0.8s ease;
}
@keyframes pageFadeIn {
    from {opacity:0; transform:translateY(10px);}
    to {opacity:1; transform:translateY(0);}
}

/* Header with a new gradient */
.main-header {
    text-align:center;
    padding:2rem 0;
    background: linear-gradient(135deg,#6a11cb 0%,#2575fc 100%);
    color:white;
    border-radius:15px;
    margin-bottom:2rem;
    box-shadow:0 8px 30px rgba(0,0,0,0.2);
    animation: slideDown 0.8s ease;
}
@keyframes slideDown {
    from {transform:translateY(-30px); opacity:0;}
    to {transform:translateY(0); opacity:1;}
}
.main-header h1 { font-weight:700; font-size:2.5em; }
.main-header p { font-size:1.2em; margin-top:0.5rem; }

/* Feature cards with a little more depth */
.feature-card {
    background:white;
    padding:1.5rem;
    border-radius:15px;
    margin:1rem 0;
    border:1px solid #eee;
    box-shadow:0 5px 20px rgba(0,0,0,0.1);
    color:#333;
    transition: all 0.3s ease;
    opacity:0;
    animation: fadeInUp 0.6s forwards;
}
.feature-card:hover {
    transform: scale(1.05) translateY(-8px);
    box-shadow:0 12px 30px rgba(0,0,0,0.15);
}

/* Recommendation cards */
.recommendation-card {
    background:white;
    padding:1.5rem;
    border-radius:15px;
    margin:1rem 0;
    border:1px solid #f0f0f0;
    box-shadow:0 6px 20px rgba(0,0,0,0.1);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
    opacity:0;
    animation: fadeInUp 0.6s forwards;
}
.recommendation-card:hover {
    transform: scale(1.03) translateY(-8px);
    box-shadow:0 12px 30px rgba(0,0,0,0.2);
}

/* Fade-in up animation */
@keyframes fadeInUp {
    from {opacity:0; transform:translateY(15px);}
    to {opacity:1; transform:translateY(0);}
}

/* Score badge with a more vibrant gradient */
.score-badge {
    background: linear-gradient(45deg,#ff6b6b 0%,#ffc76b 100%);
    color:white;
    padding:0.6rem 1.2rem;
    border-radius:30px;
    font-weight:bold;
    text-align:center;
    font-size:1.1em;
    box-shadow:0 3px 8px rgba(0,0,0,0.1);
}

/* Skill tags with a new color scheme */
.skill-tag {
    background:#e0f7fa;
    color:#00796b;
    padding:0.35rem 0.9rem;
    border-radius:20px;
    margin:0.2rem;
    font-size:0.85em;
    display:inline-block;
    border:1px solid #b2dfdb;
    transition: background 0.2s, transform 0.2s;
}
.skill-tag:hover { background:#b2dfdb; transform: scale(1.05); }

/* Match indicator */
.match-indicator {
    background:#e8f5e8;
    color:#2e7d32;
    padding:0.35rem 0.9rem;
    border-radius:20px;
    margin:0.2rem;
    font-size:0.85em;
    display:inline-block;
    border:1px solid #c8e6c9;
}

/* Form container */
.form-container {
    background:white;
    padding:2rem;
    border-radius:15px;
    box-shadow:0 4px 20px rgba(0,0,0,0.08);
    margin:2rem 0;
    opacity:0;
    animation: fadeInUp 0.8s forwards;
}

/* Buttons with a more pronounced hover effect */
.stButton>button {
    border-radius:12px;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    transform: scale(1.05);
    background-color:#0056b3;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

/* Footer */
.footer {
    text-align:center;
    color:#666;
    padding:2rem;
    font-size:0.9em;
}
</style>
""", unsafe_allow_html=True)

# ---------- DATA LOADING ----------
@st.cache_data
def load_data_with_progress():
    with st.spinner('🔄 Loading internship database...'):
        time.sleep(1)
        return re.load_and_preprocess_data()

if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

internships_df = load_data_with_progress()

# ---------- HEADER ----------
st.markdown("""
<div class="main-header">
    <h1>💼 Internship Matchmaker</h1>
    <p>Find the perfect internship tailored just for you!</p>
</div>
""", unsafe_allow_html=True)

# ---------- FEATURE CARDS ----------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="feature-card">🎯 <strong>Smart Matching</strong><br>AI matches your skills with the best opportunities</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="feature-card">📍 <strong>Location-Based</strong><br>Find internships by city or remote</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="feature-card">🚀 <strong>Instant Results</strong><br>Personalized matches in seconds</div>', unsafe_allow_html=True)

# ---------- FORM ----------
st.markdown('<div class="form-container">', unsafe_allow_html=True)

with st.form("user_input_form", clear_on_submit=False):
    st.subheader("👋 Tell Us About You")
    skills = st.text_input("✨ Your Skills", placeholder="e.g., Python, ML, Communication")
    col1, col2 = st.columns(2)
    with col1:
        location = st.selectbox("📍 Preferred Location", ["All"] + sorted(internships_df['Location'].unique()))
    with col2:
        sector = st.selectbox("🎯 Sector", ["All"] + sorted(internships_df['Sector'].unique()))
    submit_button = st.form_submit_button("🔍 Find My Internships", use_container_width=True, type="primary")

st.markdown('</div>', unsafe_allow_html=True)

# ---------- HANDLE SUBMISSION ----------
if submit_button:
    if not skills.strip():
        st.warning("⚠️ Please enter at least one skill")
    else:
        st.session_state.form_submitted = True
        with st.spinner("Analyzing your profile..."):
            time.sleep(1.2)
            loc = None if location == "All" else location
            sec = None if sector == "All" else sector
            recommendations = re.get_recommendations(skills, loc, sec, internships_df)
            st.session_state.recommendations = recommendations

# ---------- SHOW RESULTS ----------
if st.session_state.form_submitted:
    # Use st.session_state to access recommendations across reruns
    recommendations = st.session_state.get('recommendations', None)
    if recommendations is not None and not recommendations.empty:
        st.success(f"🎉 Found {len(recommendations)} matches for you!")
        user_skills_list = [s.strip().lower() for s in skills.split(',')]

        for _, row in recommendations.iterrows():
            st.markdown(f"""
            <div class="recommendation-card">
                <div style="display:flex; justify-content:space-between; align-items:start;">
                    <div>
                        <h3 style="margin:0;">{row['Internship_Title']}</h3>
                        <p style="color:#555;">📍 {row['Location']} | 🏢 {row['Sector']}</p>
                    </div>
                    <div class="score-badge">⭐ {int(row['score'])}</div>
                </div>
                <div style="margin-top:1rem;">
                    <strong>💡 Why this match?</strong><br>
            """, unsafe_allow_html=True)

            tags = []
            if loc and row['Location'].lower() == loc.lower():
                tags.append('<span class="match-indicator">📍 Perfect Location</span>')
            if sec and row['Sector'].lower() == sec.lower():
                tags.append('<span class="match-indicator">🎯 Ideal Sector</span>')

            matched_skills = [
                f'<span class="skill-tag">{skill.strip()}</span>'
                for skill in row['Required_Skills'].split(',')
                if skill.strip().lower() in user_skills_list
            ]

            if tags or matched_skills:
                st.markdown(f"""
                    {' '.join(tags)}
                    {' '.join(matched_skills)}
                </div>
            </div>
            """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <p style="color:#888;">This internship matches your profile but doesn't have a direct skills or location/sector match listed.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("😞 No internships found with the specified criteria. Try broadening your search!")

# ---------- FOOTER ----------
st.markdown('<div class="footer">Internship Matchmaker 2023 | Powered by AI</div>', unsafe_allow_html=True)
