import streamlit as st
from pipeline import (
    career_agent_pipeline,
    analyze_gap,
    generate_roadmap,
    simulate_career_path
)

st.set_page_config(
    page_title="Career Intelligence",
    layout="centered"
)

# ---------------- SESSION STATE ----------------
if "agent_data" not in st.session_state:
    st.session_state.agent_data = None

if "selected_role" not in st.session_state:
    st.session_state.selected_role = None

if "gap_data" not in st.session_state:
    st.session_state.gap_data = None

if "roadmap_data" not in st.session_state:
    st.session_state.roadmap_data = None

if "simulation_data" not in st.session_state:
    st.session_state.simulation_data = None


# ---------------- PREMIUM STYLING ----------------
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, "San Francisco", sans-serif;
    background-color: #F7F7F8;
}

.block-container {
    padding-top: 4rem;
    padding-bottom: 4rem;
    max-width: 820px;
}

.section-title {
    font-size: 13px;
    color: #6B7280;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-bottom: 12px;
}

.skill-card {
    padding: 28px;
    border-radius: 20px;
    background: white;
    border: 1px solid #ECECEC;
    font-size: 20px;
    font-weight: 500;
    line-height: 1.6;
    box-shadow: 0 6px 20px rgba(0,0,0,0.04);
}

.role-card {
    padding: 22px;
    border-radius: 18px;
    background: white;
    border: 1px solid #ECECEC;
    margin-bottom: 18px;
    transition: all 0.25s ease;
}

.role-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 30px rgba(0,0,0,0.06);
}

.role-title {
    font-size: 17px;
    font-weight: 600;
    margin-bottom: 12px;
}

ul {
    padding-left: 18px;
    margin: 0;
}

li {
    margin-bottom: 8px;
    color: #4B5563;
    font-size: 14px;
}

.footer {
    text-align:center;
    color:#9CA3AF;
    font-size:13px;
    margin-top:70px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<h1 style='text-align:center;'>Career Intelligence</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#6B7280;'>Align your skills with meaningful career paths</p>", unsafe_allow_html=True)
st.divider()

# ---------------- MODE ----------------
mode = st.radio(
    "Input Method",
    ["Text Query", "Upload Resume"],
    horizontal=True
)

st.divider()

# ---------------- RENDER FUNCTIONS ----------------

def render_base_output(data):
    st.markdown("<div class='section-title'>Skill Focus</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='skill-card'>{data['skill_cluster']}</div>",
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("<div class='section-title'>Suggested Roles</div>", unsafe_allow_html=True)

    for role_data in data["roles"]:
        bullets = "".join([f"<li>{p}</li>" for p in role_data["path"]])
        st.markdown(
            f"""
            <div class='role-card'>
                <div class='role-title'>{role_data['role']}</div>
                <ul>{bullets}</ul>
            </div>
            """,
            unsafe_allow_html=True
        )


def render_gap_analysis(gap_data):
    st.divider()
    st.markdown("<div class='section-title'>Skill Gap Analysis</div>", unsafe_allow_html=True)

    score = gap_data["readiness_score"]

    st.markdown(
        f"""
        <div class='skill-card'>
            <div style='font-size:14px;color:#6B7280;'>Readiness Score</div>
            <div style='font-size:32px;font-weight:600;margin-top:6px;'>{score}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    for skill in gap_data["missing_skills"]:
        priority_color = {
            "High": "#EF4444",
            "Medium": "#F59E0B",
            "Low": "#10B981"
        }.get(skill["priority"], "#6B7280")

        st.markdown(
            f"""
            <div class='role-card'>
                <div style='display:flex;justify-content:space-between;'>
                    <div style='font-weight:600;'>{skill['skill']}</div>
                    <div style='color:{priority_color};font-size:13px;font-weight:500;'>
                        {skill['priority']}
                    </div>
                </div>
                <div style='margin-top:8px;color:#4B5563;font-size:14px;'>
                    {skill['action']}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


def render_roadmap(roadmap_data):
    st.divider()
    st.markdown("<div class='section-title'>90 Day Roadmap</div>", unsafe_allow_html=True)

    phases = roadmap_data["roadmap"]

    phase_titles = {
        "phase_1_foundation_days_1_15": "Phase 1 — Foundation (Days 1–15)",
        "phase_2_core_building_days_16_30": "Phase 2 — Core Building (Days 16–30)",
        "phase_3_projects_days_31_60": "Phase 3 — Projects (Days 31–60)",
        "phase_4_interview_prep_days_61_90": "Phase 4 — Interview Prep (Days 61–90)"
    }

    for key, title in phase_titles.items():
        if key in phases:
            clean_items = []
            for item in phases[key]:
                if isinstance(item, dict):
                    clean_items.append(list(item.values())[0])
                else:
                    clean_items.append(item)

            bullets = "".join([f"<li>{i}</li>" for i in clean_items])

            st.markdown(
                f"""
                <div class='role-card'>
                    <div class='role-title'>{title}</div>
                    <ul>{bullets}</ul>
                </div>
                """,
                unsafe_allow_html=True
            )


def render_simulation(sim_data):
    st.divider()
    st.markdown("<div class='section-title'>2-Year Career Simulation</div>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class='role-card'>
            <div class='role-title'>Year 1 — {sim_data['year_1']['position']}</div>
            <ul>
                <li>{sim_data['year_1']['focus'][0]}</li>
                <li>{sim_data['year_1']['focus'][1]}</li>
                <li>{sim_data['year_1']['focus'][2]}</li>
            </ul>
            <div style='margin-top:10px;color:#4B5563;font-size:14px;'>
                Milestone: {sim_data['year_1']['milestone']}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class='role-card'>
            <div class='role-title'>Year 2 — {sim_data['year_2']['position']}</div>
            <ul>
                <li>{sim_data['year_2']['focus'][0]}</li>
                <li>{sim_data['year_2']['focus'][1]}</li>
                <li>{sim_data['year_2']['focus'][2]}</li>
            </ul>
            <div style='margin-top:10px;color:#4B5563;font-size:14px;'>
                Milestone: {sim_data['year_2']['milestone']}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class='skill-card'>
            <div style='font-size:15px;color:#6B7280;'>Strategic Evolution</div>
            <div style='margin-top:6px;font-size:15px;'>
                {sim_data['maturity_shift']}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------- MAIN LOGIC ----------------

query = None
uploaded_file = None

if mode == "Text Query":
    query = st.text_input("Describe your experience or interests")

    if st.button("Generate Insights", use_container_width=True) and query.strip():
        st.session_state.agent_data = career_agent_pipeline(query=query)
        st.session_state.gap_data = None
        st.session_state.roadmap_data = None
        st.session_state.simulation_data = None

else:
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

    if st.button("Analyze Resume", use_container_width=True) and uploaded_file:
        st.session_state.agent_data = career_agent_pipeline(resume_file=uploaded_file)
        st.session_state.gap_data = None
        st.session_state.roadmap_data = None
        st.session_state.simulation_data = None


if st.session_state.agent_data:

    render_base_output(st.session_state.agent_data)

    roles = [r["role"] for r in st.session_state.agent_data["roles"]]

    st.session_state.selected_role = st.selectbox(
        "Choose a role to explore deeper",
        roles,
        index=roles.index(st.session_state.selected_role)
        if st.session_state.selected_role in roles else 0
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Analyze Skill Gap", use_container_width=True):
            st.session_state.gap_data = analyze_gap(
                st.session_state.selected_role,
                st.session_state.agent_data["skill_text"],
                query if query else "Resume-based"
            )
            st.session_state.roadmap_data = None
            st.session_state.simulation_data = None

    with col2:
        if st.button("Generate 90 Day Roadmap", use_container_width=True):
            st.session_state.roadmap_data = generate_roadmap(
                st.session_state.selected_role,
                query if query else "Resume-based",
                st.session_state.agent_data["skill_text"]
            )
            st.session_state.gap_data = None
            st.session_state.simulation_data = None

    with col3:
        if st.button("Simulate 2-Year Growth", use_container_width=True):
            st.session_state.simulation_data = simulate_career_path(
                st.session_state.selected_role,
                st.session_state.agent_data["skill_text"],
                query if query else "Resume-based"
            )
            st.session_state.gap_data = None
            st.session_state.roadmap_data = None

    if st.session_state.gap_data:
        render_gap_analysis(st.session_state.gap_data)

    if st.session_state.roadmap_data:
        render_roadmap(st.session_state.roadmap_data)

    if st.session_state.simulation_data:
        render_simulation(st.session_state.simulation_data)


# ---------------- FOOTER ----------------
st.markdown(
    """
    <div class='footer'>
        <div style="margin-bottom:6px;">
            Designed with <span style="color:#EF4444;"></span> by 
            <span style="font-weight:500;">Aditya Agarwal</span>
        </div>
        Semantic intelligence • Structured AI reasoning
    </div>
    """,
    unsafe_allow_html=True
)