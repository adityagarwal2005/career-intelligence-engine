from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import get_router
from .config import get_settings
from .services.optimizer_service import ResumeOptimizerService


def create_app() -> FastAPI:
    settings = get_settings()
    optimizer_service = ResumeOptimizerService(settings)

    app = FastAPI(title="Resume Optimiser API", version="2.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(get_router(optimizer_service))
    return app
