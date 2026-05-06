from __future__ import annotations

import json

from ..config import Settings
from ..prompts import (
    ANALYSIS_SYSTEM_PROMPT,
    COMPOSITION_SYSTEM_PROMPT,
    COMPOSITION_DATASET_PROMPT,
    QA_SYSTEM_PROMPT,
)
from ..schemas import AnalysisArtifacts
from ..utils.formatter import has_required_sections
from .llm_service import LLMService
from .project_scorer import ProjectScorer


class ResumeOptimizerService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.llm = LLMService(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
            max_retries=settings.max_retries,
        )
        self.project_scorer = ProjectScorer()

    def optimize(self, job_description: str, resume: str, mode: str = "ai_match") -> str:
        """
        Optimize resume for job description.
        
        Args:
            job_description: Job description text
            resume: Resume text
            mode: "ai_match" for full AI optimization or "my_dataset" for dataset-based scoring
            
        Returns:
            Optimized resume suggestions
        """
        if mode not in ["ai_match", "my_dataset"]:
            mode = "ai_match"
        
        # Stage 1: Analysis (same for both modes)
        analysis_user_prompt = (
            "Analyze the following JD and resume. Return JSON only.\n\n"
            f"JOB DESCRIPTION:\n{job_description}\n\n"
            f"RESUME:\n{resume}"
        )
        analysis_json = self.llm.generate_json(
            system_prompt=ANALYSIS_SYSTEM_PROMPT,
            user_prompt=analysis_user_prompt,
            temperature=self.settings.temperature_analysis,
        )

        artifacts = AnalysisArtifacts.model_validate(analysis_json)

        # Stage 2: Composition (different based on mode)
        if mode == "ai_match":
            composition_user_prompt = (
                "Use these artifacts and generate final output.\n\n"
                f"ANALYSIS_ARTIFACTS_JSON:\n{json.dumps(artifacts.model_dump(), indent=2)}\n\n"
                f"JOB DESCRIPTION:\n{job_description}\n\n"
                f"RESUME:\n{resume}"
            )
            composition_prompt = COMPOSITION_SYSTEM_PROMPT
        else:  # my_dataset mode
            # Score projects from dataset
            scored_projects = self.project_scorer.score_projects(job_description)
            top_projects = self.project_scorer.get_projects_for_optimizer(job_description)
            
            projects_context = json.dumps(top_projects, indent=2)
            
            composition_user_prompt = (
                "Use these artifacts and pre-selected projects to generate final output.\n\n"
                f"ANALYSIS_ARTIFACTS_JSON:\n{json.dumps(artifacts.model_dump(), indent=2)}\n\n"
                f"PRE_SELECTED_PROJECTS_FROM_DATASET:\n{projects_context}\n\n"
                f"JOB DESCRIPTION:\n{job_description}\n\n"
                f"RESUME:\n{resume}"
            )
            composition_prompt = COMPOSITION_DATASET_PROMPT

        drafted_output = self.llm.generate_text(
            system_prompt=composition_prompt,
            user_prompt=composition_user_prompt,
            temperature=self.settings.temperature_composition,
        )

        # Stage 3: QA (same for both modes)
        qa_user_prompt = (
            "Validate and repair if required.\n\n"
            f"RESUME STYLE SIGNATURE:\n{artifacts.resume_format_signature}\n\n"
            f"CANDIDATE_OUTPUT:\n{drafted_output}"
        )
        final_output = self.llm.generate_text(
            system_prompt=QA_SYSTEM_PROMPT,
            user_prompt=qa_user_prompt,
            temperature=self.settings.temperature_qa,
        )

        if not has_required_sections(final_output):
            raise RuntimeError("Generated output missing required section headers.")

        return final_output
