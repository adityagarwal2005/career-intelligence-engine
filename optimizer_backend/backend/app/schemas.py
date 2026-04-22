from __future__ import annotations

from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    job_description: str = Field(..., min_length=40)
    resume: str = Field(..., min_length=40)
    mode: str = Field(default="ai_match", description="Optimization mode: 'ai_match' or 'my_dataset'")


class AnalyzeResponse(BaseModel):
    result: str
    mode: str = Field(default="ai_match", description="Which mode was used for optimization")


class AnalysisArtifacts(BaseModel):
    resume_format_signature: str
    resume_tone_signature: str
    jd_priority_keywords: list[str]
    jd_required_tools_frameworks: list[str]
    jd_responsibility_map: list[str]
    skills_gap_high_value: list[str]
    project_themes_ranked: list[str]
    weak_projects_candidates: list[dict[str, str]]
    constraints_checklist: list[str]
