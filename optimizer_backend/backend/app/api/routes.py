from __future__ import annotations

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from ..schemas import AnalyzeRequest, AnalyzeResponse
from ..services.optimizer_service import ResumeOptimizerService
from ..utils.resume_parser import ResumeParsingError, extract_resume_text


def get_router(optimizer_service: ResumeOptimizerService) -> APIRouter:
    router = APIRouter()

    @router.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @router.post("/analyze", response_model=AnalyzeResponse)
    def analyze(payload: AnalyzeRequest) -> AnalyzeResponse:
        try:
            result = optimizer_service.optimize(
                job_description=payload.job_description,
                resume=payload.resume,
                mode=payload.mode,
            )
            return AnalyzeResponse(result=result, mode=payload.mode)
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"Analysis failed: {exc}") from exc

    @router.post("/analyze-upload", response_model=AnalyzeResponse)
    async def analyze_upload(
        job_description: str = Form(...),
        resume_file: UploadFile = File(...),
        mode: str = Form(default="ai_match"),
    ) -> AnalyzeResponse:
        if len(job_description.strip()) < 40:
            raise HTTPException(
                status_code=400,
                detail="Please provide a complete Job Description (minimum 40 characters).",
            )

        if mode not in ["ai_match", "my_dataset"]:
            mode = "ai_match"

        try:
            resume_text = await extract_resume_text(resume_file)
            if len(resume_text.strip()) < 40:
                raise HTTPException(
                    status_code=400,
                    detail="Extracted resume text is too short. Upload a complete resume.",
                )

            result = optimizer_service.optimize(
                job_description=job_description,
                resume=resume_text,
                mode=mode,
            )
            return AnalyzeResponse(result=result, mode=mode)
        except ResumeParsingError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"Analysis failed: {exc}") from exc

    return router
