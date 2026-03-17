import os
import json
import numpy as np
from numpy.linalg import norm
import pandas as pd
import pdfplumber
from openai import OpenAI
from dotenv import load_dotenv

# ------------------ LOAD ENV ------------------
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ------------------ LOAD DATA ------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

df = pd.read_pickle(os.path.join(BASE_DIR, "data1.pkl"))
df2 = pd.read_pickle(os.path.join(BASE_DIR, "data2.pkl"))

# Prepare embedding matrix once
embedding_matrix = np.vstack(df["embedding"].values)
embedding_matrix = embedding_matrix / np.linalg.norm(
    embedding_matrix, axis=1, keepdims=True
)

# ------------------ EMBEDDING ------------------
def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


# ------------------ PDF TEXT EXTRACTION ------------------
def extract_text_from_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


# ------------------ SKILL RELEVANT EXTRACTION ------------------
def extract_skill_relevant_content(text):
    text_lower = text.lower()
    keywords = ["skills", "projects", "technologies", "tools"]
    content = ""

    for keyword in keywords:
        if keyword in text_lower:
            start = text_lower.index(keyword)
            content += text[start:start + 1000]

    if content.strip() == "":
        return text[:1500]

    return content


# ------------------ GPT ROLE GENERATION ------------------
def rag_gpt_json(skill, joblist):

    # Guard: if joblist is empty, return safe fallback
    if len(joblist) == 0:
        return {
            "skill_cluster": "No matching cluster found",
            "roles": [
                {"role": "No Role Found", "path": ["Please enter a more detailed description of your skills"]},
                {"role": "No Role Found", "path": ["Try adding specific technologies or tools you know"]},
                {"role": "No Role Found", "path": ["Example: Python, Machine Learning, Data Analysis"]}
            ]
        }

    joblist = joblist[:3]

    # Safety if less than 3 roles exist
    while len(joblist) < 3:
        joblist.append(joblist[-1])

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.3,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "Return ONLY valid JSON."},
            {"role": "user", "content": f"""
Best Matched Skill: {skill}
Top 3 Roles: {joblist[0]}, {joblist[1]}, {joblist[2]}

Return JSON:

{{
  "skill_cluster": "refined skill cluster",
  "roles": [
    {{
      "role": "{joblist[0]}",
      "path": ["bullet 1", "bullet 2", "bullet 3"]
    }},
    {{
      "role": "{joblist[1]}",
      "path": ["bullet 1", "bullet 2", "bullet 3"]
    }},
    {{
      "role": "{joblist[2]}",
      "path": ["bullet 1", "bullet 2", "bullet 3"]
    }}
  ]
}}
"""}
        ]
    )

    return json.loads(response.choices[0].message.content)


# ------------------ CORE MATCHING ENGINE ------------------
def generate_from_embedding(query_embedding):

    query_embedding = np.array(query_embedding)
    query_embedding = query_embedding / norm(query_embedding)

    similarities = np.dot(embedding_matrix, query_embedding)
    best_index = np.argmax(similarities)

    confidence = round(float(similarities[best_index]) * 100, 2)

    idvalue = df.iloc[best_index]["id"]
    skillvalue = df.iloc[best_index]["skills"]

    joblist = df2[df2["myskills_id"] == idvalue]["jobs"].tolist()

    # Guard: if no jobs found for this skill ID
    if len(joblist) == 0:
        return {
            "confidence": confidence,
            "data": {
                "skill_cluster": "No matching roles found",
                "roles": [
                    {"role": "No Role Found", "path": ["Please enter a more detailed description of your skills"]},
                    {"role": "No Role Found", "path": ["Try adding specific technologies or tools you know"]},
                    {"role": "No Role Found", "path": ["Example: Python, Machine Learning, Data Analysis"]}
                ]
            }
        }

    json_data = rag_gpt_json(skillvalue, joblist)

    return {
        "confidence": confidence,
        "data": json_data
    }


def match_skill(skill_text):
    query_embedding = get_embedding(skill_text)
    return generate_from_embedding(query_embedding)


# ------------------ AGENT ENTRY POINT ------------------
def career_agent_pipeline(query=None, resume_file=None):

    if resume_file:
        resume_text = extract_text_from_pdf(resume_file)
        skill_text = extract_skill_relevant_content(resume_text)
    else:
        skill_text = query

    # Guard: empty or too short input
    if not skill_text or len(skill_text.strip()) < 5:
        return {
            "confidence": 0,
            "skill_cluster": "Input too short",
            "roles": [
                {"role": "No Role Found", "path": ["Please enter a more detailed description"]},
                {"role": "No Role Found", "path": ["Try adding specific technologies or tools you know"]},
                {"role": "No Role Found", "path": ["Example: Python, Machine Learning, Data Analysis"]}
            ],
            "skill_text": skill_text
        }

    base_result = match_skill(skill_text)

    return {
        "confidence": base_result["confidence"],
        "skill_cluster": base_result["data"]["skill_cluster"],
        "roles": base_result["data"]["roles"],
        "skill_text": skill_text
    }


# ------------------ SKILL GAP AGENT ------------------
def analyze_gap(selected_job, skill_text, query):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You are a career skill gap analysis assistant. Return ONLY valid JSON. Be concise."
            },
            {
                "role": "user",
                "content": f"""
User Background:
{query}

Detected Skill Context:
{skill_text}

Target Role:
{selected_job}

Return JSON in this format:

{{
  "role": "{selected_job}",
  "readiness_score": 0-100,
  "missing_skills": [
    {{
      "skill": "skill name",
      "priority": "High/Medium/Low",
      "action": "short action step"
    }}
  ]
}}

Rules:
- Max 5 missing skills
- Action under 12 words
- No explanations
"""
            }
        ]
    )

    return json.loads(response.choices[0].message.content)


# ------------------ ROADMAP AGENT ------------------
def generate_roadmap(selected_job, query, skill_text):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.3,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You are a career planning assistant. Return ONLY valid JSON."
            },
            {
                "role": "user",
                "content": f"""
User Background:
{query}

Detected Skill Context:
{skill_text}

Target Role:
{selected_job}

Return JSON.
Each roadmap phase must be an array of plain strings.
Do NOT return objects. Only simple strings.

{{
  "role": "{selected_job}",
  "roadmap": {{
    "phase_1_foundation_days_1_15": [],
    "phase_2_core_building_days_16_30": [],
    "phase_3_projects_days_31_60": [],
    "phase_4_interview_prep_days_61_90": []
  }}
}}
"""
            }
        ]
    )

    return json.loads(response.choices[0].message.content)


# ------------------ CAREER SIMULATION AGENT ------------------
def simulate_career_path(selected_job, skill_text, query):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.4,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You are a strategic career growth simulation assistant. Return ONLY valid JSON."
            },
            {
                "role": "user",
                "content": f"""
User Background:
{query}

Current Skill Context:
{skill_text}

Target Role:
{selected_job}

Simulate a realistic 2-year career progression.

Return JSON in this format:

{{
  "starting_role": "{selected_job}",
  "year_1": {{
    "position": "job title",
    "focus": ["skill 1", "skill 2", "skill 3"],
    "milestone": "major achievement"
  }},
  "year_2": {{
    "position": "advanced job title",
    "focus": ["skill 1", "skill 2", "skill 3"],
    "milestone": "major achievement"
  }},
  "maturity_shift": "How the candidate evolves strategically"
}}

Rules:
- Be realistic
- No fluff
- No long explanations
"""
            }
        ]
    )

    return json.loads(response.choices[0].message.content)