import streamlit as st
import requests
import html
import io
import textwrap
try:
    from PyPDF2 import PdfReader
    from PyPDF2.errors import PdfReadError
except ModuleNotFoundError:
    from pypdf import PdfReader
    from pypdf.errors import PdfReadError
try:
    from reportlab.lib.pagesizes import LETTER
    from reportlab.pdfgen import canvas
except ModuleNotFoundError:
    LETTER = (612.0, 792.0)
    canvas = None
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

if "optimized_resume_result" not in st.session_state:
    st.session_state.optimized_resume_result = ""

if "optimized_resume_error" not in st.session_state:
    st.session_state.optimized_resume_error = ""

if "selected_section" not in st.session_state:
    st.session_state.selected_section = "Resume Analyzer"


def optimizer_backend_is_live() -> bool:
    try:
        response = requests.get("http://localhost:8000/health", timeout=1.2)
        return response.status_code == 200
    except requests.RequestException:
        return False


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

.api-badge {
    display: inline-block;
    background: #F0FDF4;
    color: #16A34A;
    font-size: 11px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
    border: 1px solid #BBF7D0;
    margin-bottom: 10px;
}

.status-pill {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    border-radius: 999px;
    padding: 4px 11px;
    border: 1px solid #E5E7EB;
    background: #FFFFFF;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.2px;
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 999px;
    display: inline-block;
}

.status-ok {
    background: #22C55E;
    box-shadow: 0 0 0 4px rgba(34,197,94,0.16);
}

.status-down {
    background: #EF4444;
    box-shadow: 0 0 0 4px rgba(239,68,68,0.16);
}

.side-card {
    margin-top: 10px;
    border: 1px solid #E5E7EB;
    border-radius: 14px;
    padding: 12px 13px;
    background: #FFFFFF;
}

.side-card h4 {
    margin: 0;
    font-size: 13px;
    color: #111827;
}

.side-card p {
    margin: 6px 0 0 0;
    color: #6B7280;
    font-size: 12px;
    line-height: 1.5;
}

.switch-title {
    text-align: center;
    margin-top: 6px;
    margin-bottom: 16px;
}

.switch-title h2 {
    margin: 0;
    font-size: 28px;
    font-weight: 700;
    color: #111827;
}

.switch-title p {
    margin-top: 8px;
    color: #6B7280;
    font-size: 14px;
}

.service-card {
    border-radius: 20px;
    padding: 22px;
    border: 1px solid #E5E7EB;
    background: linear-gradient(180deg, #FFFFFF 0%, #FAFAFB 100%);
    box-shadow: 0 6px 22px rgba(0,0,0,0.05);
    transition: all 0.28s ease;
    min-height: 180px;
}

.service-card-link {
    display: block;
    text-decoration: none !important;
    color: inherit !important;
    border-radius: 20px;
}

.service-card-link:focus,
.service-card-link:active,
.service-card-link:hover {
    text-decoration: none !important;
}

.service-card.active {
    border: 1px solid #2563EB;
    box-shadow: 0 12px 34px rgba(37,99,235,0.22);
    transform: translateY(-2px);
    background: linear-gradient(180deg, #EFF6FF 0%, #FFFFFF 100%);
}

.service-badge {
    display: inline-block;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.3px;
    color: #1D4ED8;
    background: #DBEAFE;
    border: 1px solid #BFDBFE;
    border-radius: 999px;
    padding: 4px 10px;
    margin-bottom: 12px;
}

.service-card h3 {
    margin: 0;
    color: #111827;
    font-size: 20px;
    font-weight: 700;
}

.service-card p {
    margin-top: 10px;
    color: #4B5563;
    font-size: 14px;
    line-height: 1.55;
}

.section-banner {
    margin-top: 6px;
    padding: 18px 22px;
    border-radius: 16px;
    border: 1px solid #E5E7EB;
    background: #FFFFFF;
    box-shadow: 0 4px 16px rgba(0,0,0,0.04);
}

.section-banner h3 {
    margin: 0;
    color: #111827;
    font-size: 24px;
    font-weight: 700;
}

.section-banner p {
    margin-top: 8px;
    margin-bottom: 0;
    color: #6B7280;
    font-size: 14px;
}

.optimized-preview {
    border: 1px solid #E5E7EB;
    border-radius: 14px;
    background: #FFFFFF;
    padding: 16px;
    font-size: 14px;
    color: #111827;
    line-height: 1.7;
    max-height: 460px;
    overflow-y: auto;
    white-space: normal;
}
</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR — API INFO ----------------
with st.sidebar:
    backend_live = optimizer_backend_is_live()
    status_label = "ONLINE" if backend_live else "OFFLINE"
    status_class = "status-ok" if backend_live else "status-down"

    st.markdown("### Workspace Overview")
    st.markdown(
        f"""
        <div class='status-pill'>
            <span class='status-dot {status_class}'></span>
            Optimizer API {status_label}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class='side-card'>
            <h4>Resume Analyzer</h4>
            <p>Role discovery, skill-gap insights, 90-day roadmap, and growth simulation.</p>
        </div>
        <div class='side-card'>
            <h4>Resume Optimization</h4>
            <p>Uses FastAPI on localhost:8000 to optimize resume content for target roles.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("Advanced API details"):
        st.markdown("""
| Method | Endpoint |
|--------|----------|
| `GET` | `/health` |
| `POST` | `/analyze` |
        """)
        st.markdown("Backend URL: `http://localhost:8000`")

    st.divider()
    st.markdown("<span style='font-size:12px;color:#9CA3AF;'>Built by Aditya Agarwal</span>", unsafe_allow_html=True)


# ---------------- HEADER ----------------
st.markdown("<h1 style='text-align:center;'>Career Intelligence V2</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#6B7280;'>Align your skills with meaningful career paths</p>", unsafe_allow_html=True)
st.divider()

# ---------------- APP SECTION SWITCH ----------------
st.markdown(
    """
    <div class='switch-title'>
        <h2>Select Your Experience</h2>
        <p>Choose one module below to continue.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

col_left, col_right = st.columns(2)

with col_left:
    analyzer_active = st.session_state.selected_section == "Resume Analyzer"
    st.markdown(
        f"""
        <div class='service-card {'active' if analyzer_active else ''}'>
            <div class='service-badge'>SIMPLE.FAST</div>
            <h3>Resume Analyzer</h3>
            <p>Analyze skills, discover role matches, run gap analysis, and generate roadmap + growth simulation.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Use Resume Analyzer", use_container_width=True, key="switch_resume_analyzer"):
        st.session_state.selected_section = "Resume Analyzer"
        st.rerun()

with col_right:
    optimizer_active = st.session_state.selected_section == "Resume Optimization"
    st.markdown(
        f"""
        <div class='service-card {'active' if optimizer_active else ''}'>
            <div class='service-badge'>SECURE.SAFE</div>
            <h3>Resume Optimization</h3>
            <p>Upload resume + target job description and get optimized, ATS-friendly content from the optimizer API.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Use Resume Optimization", use_container_width=True, key="switch_resume_optimization"):
        st.session_state.selected_section = "Resume Optimization"
        st.rerun()

selected_section = st.session_state.selected_section

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


def parse_pdf_text(uploaded_pdf):
    try:
        reader = PdfReader(uploaded_pdf)
        extracted_text = "\n".join((page.extract_text() or "") for page in reader.pages).strip()
        if not extracted_text:
            return None, "Could not extract text from this PDF. Please upload a valid text-based PDF."
        return extracted_text, None
    except PdfReadError:
        return None, "Invalid PDF file. Please upload a valid PDF resume."
    except Exception as exc:
        return None, f"Failed to parse PDF: {exc}"


def build_pdf_bytes(text: str) -> bytes:
    if canvas is None:
        raise RuntimeError("PDF generator not installed.")

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=LETTER)
    width, height = LETTER
    left_margin = 48
    right_margin = 48
    top_margin = 52
    bottom_margin = 48
    max_chars = 95
    line_height = 14

    text_obj = pdf.beginText(left_margin, height - top_margin)
    text_obj.setFont("Helvetica", 11)

    for para in text.splitlines() or [""]:
        wrapped_lines = textwrap.wrap(para, width=max_chars) if para.strip() else [""]
        for line in wrapped_lines:
            if text_obj.getY() <= bottom_margin:
                pdf.drawText(text_obj)
                pdf.showPage()
                text_obj = pdf.beginText(left_margin, height - top_margin)
                text_obj.setFont("Helvetica", 11)
            text_obj.textLine(line)
        text_obj.moveCursor(0, -2)

    pdf.drawText(text_obj)
    pdf.save()
    buffer.seek(0)
    return buffer.getvalue()


# ---------------- MAIN LOGIC ----------------

if selected_section == "Resume Analyzer":
    st.markdown(
        """
        <div class='section-banner'>
            <h3>Resume Analyzer</h3>
            <p>Use your profile or resume to discover role pathways and strategic career actions.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)

    mode = st.radio(
        "Input Method",
        ["Text Query", "Upload Resume"],
        horizontal=True,
        key="resume_analyzer_input_mode"
    )

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
        uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"], key="analyzer_resume_pdf")

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

else:
    st.markdown(
        """
        <div class='section-banner'>
            <h3>Resume Optimization</h3>
            <p>Send your resume content to the optimizer backend and receive an improved version ready for download.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)

    optimizer_pdf = st.file_uploader(
        "Upload Resume (PDF)",
        type=["pdf"],
        key="resume_optimizer_pdf"
    )

    optimizer_job_description = st.text_area(
        "Job Description",
        height=180,
        key="resume_optimizer_jd"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Mode Selector with Radio (mutually exclusive)
    st.markdown("### 🎯 Optimization Mode")
    optimization_mode = st.radio(
        "Choose one mode:",
        options=["🤖 AI Match", "📁 My Dataset"],
        horizontal=True,
        help="AI Match = Full freedom | My Dataset = Use your 14 projects",
        key="optimization_mode_radio"
    )
    
    # Convert display name to mode value
    mode_value = "ai_match" if "AI Match" in optimization_mode else "my_dataset"
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Disable button logic
    can_optimize = optimizer_pdf is not None and optimizer_job_description.strip() != ""
    
    if st.button(
        "Optimize Resume", 
        use_container_width=True, 
        key="optimize_resume_btn",
        disabled=not can_optimize
    ):
        st.session_state.optimized_resume_result = ""
        st.session_state.optimized_resume_error = ""

        if optimizer_pdf is None:
            st.session_state.optimized_resume_error = "Please upload a resume PDF before optimizing."
        elif not optimizer_job_description.strip():
            st.session_state.optimized_resume_error = "Please enter a job description before optimizing."
        else:
            resume_text, parse_error = parse_pdf_text(optimizer_pdf)

            if parse_error:
                st.session_state.optimized_resume_error = parse_error
            else:
                try:
                    with st.spinner(f"Optimizing resume using {optimization_mode}..."):
                        response = requests.post(
                            "http://localhost:8000/analyze",
                            json={
                                "resume": resume_text,
                                "job_description": optimizer_job_description.strip(),
                                "mode": mode_value
                            },
                            timeout=45
                        )
                    response.raise_for_status()

                    payload = response.json()
                    optimized_result = (payload.get("result") or "").strip()

                    if optimized_result:
                        st.session_state.optimized_resume_result = optimized_result
                    else:
                        st.session_state.optimized_resume_error = "Optimizer API returned an empty result."

                except requests.exceptions.ConnectionError:
                    st.session_state.optimized_resume_error = (
                        "Could not connect to optimizer backend at http://localhost:8000. "
                        "Please make sure the FastAPI server is running."
                    )
                except requests.exceptions.Timeout:
                    st.session_state.optimized_resume_error = "Request timed out while contacting optimizer backend."
                except requests.exceptions.HTTPError:
                    try:
                        error_detail = response.json().get("detail", "Unknown server error")
                    except Exception:
                        error_detail = response.text or "Unknown server error"
                    st.session_state.optimized_resume_error = f"Optimizer API error: {error_detail}"
                except requests.exceptions.RequestException as exc:
                    st.session_state.optimized_resume_error = f"Request failed: {exc}"
                except Exception as exc:
                    st.session_state.optimized_resume_error = f"Unexpected error: {exc}"

    if st.session_state.optimized_resume_error:
        st.error(st.session_state.optimized_resume_error)

    if st.session_state.optimized_resume_result:
        st.success("Resume optimized successfully.")

        preview_tab, copy_tab = st.tabs(["Web View", "Copy/Edit"])

        with preview_tab:
            rendered_text = html.escape(st.session_state.optimized_resume_result).replace("\n", "<br>")
            st.markdown(
                f"<div class='optimized-preview'>{rendered_text}</div>",
                unsafe_allow_html=True,
            )

        with copy_tab:
            st.text_area(
                "Optimized Resume Content (You can edit and copy)",
                value=st.session_state.optimized_resume_result,
                height=420,
                key="optimized_resume_copy_box"
            )

        download_col_1, download_col_2 = st.columns(2)

        with download_col_1:
            st.download_button(
                "Download as TXT",
                data=st.session_state.optimized_resume_result,
                file_name="optimized_resume.txt",
                mime="text/plain",
                key="optimized_resume_download_txt"
            )

        with download_col_2:
            try:
                pdf_bytes = build_pdf_bytes(st.session_state.optimized_resume_result)
                st.download_button(
                    "Download as PDF",
                    data=pdf_bytes,
                    file_name="optimized_resume.pdf",
                    mime="application/pdf",
                    key="optimized_resume_download_pdf"
                )
            except Exception:
                st.info("PDF download unavailable. Install reportlab to enable this option.")


# ---------------- FOOTER ----------------
st.markdown(
    """
    <div class='footer'>
        <div style="margin-bottom:6px;">
            Designed with <span style="color:#EF4444;">♥</span> by 
            <span style="font-weight:500;">Aditya Agarwal</span>
        </div>
        Semantic intelligence • Structured AI reasoning • REST API
    </div>
    """,
    unsafe_allow_html=True
)