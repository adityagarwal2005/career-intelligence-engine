from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import io

from pipeline import (
    career_agent_pipeline,
    analyze_gap,
    generate_roadmap,
    simulate_career_path
)

app = FastAPI(
    title="Career Intelligence API",
    description="API layer for the Career Intelligence Engine by Aditya Agarwal",
    version="1.0.0"
)

# Allow Streamlit frontend to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


# ------------------ REQUEST MODELS ------------------

class TextInput(BaseModel):
    query: str

class GapRequest(BaseModel):
    selected_role: str
    skill_text: str
    query: str

class RoadmapRequest(BaseModel):
    selected_role: str
    skill_text: str
    query: str

class SimulationRequest(BaseModel):
    selected_role: str
    skill_text: str
    query: str


# ------------------ ROUTES ------------------

@app.get("/")
def root():
    return {"message": "Career Intelligence API is live. Visit /docs to explore endpoints."}


@app.post("/api/analyze/text")
def analyze_from_text(body: TextInput):
    """
    Takes a text description of skills and returns matched roles + skill cluster.
    """
    result = career_agent_pipeline(query=body.query)
    return result


@app.post("/api/analyze/resume")
async def analyze_from_resume(file: UploadFile = File(...)):
    """
    Takes a PDF resume and returns matched roles + skill cluster.
    """
    contents = await file.read()
    file_like = io.BytesIO(contents)
    result = career_agent_pipeline(resume_file=file_like)
    return result


@app.post("/api/gap")
def gap_analysis(body: GapRequest):
    """
    Returns skill gap analysis for a selected role.
    """
    result = analyze_gap(body.selected_role, body.skill_text, body.query)
    return result


@app.post("/api/roadmap")
def roadmap(body: RoadmapRequest):
    """
    Returns a 90-day learning roadmap for a selected role.
    """
    result = generate_roadmap(body.selected_role, body.query, body.skill_text)
    return result


@app.post("/api/simulate")
def simulate(body: SimulationRequest):
    """
    Returns a 2-year career simulation for a selected role.
    """
    result = simulate_career_path(body.selected_role, body.skill_text, body.query)
    return result