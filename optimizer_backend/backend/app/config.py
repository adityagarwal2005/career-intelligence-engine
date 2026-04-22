from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / "backend" / ".env")
FORCED_OPENAI_MODEL = "gpt-4o-mini"


@dataclass(frozen=True)
class Settings:
    openai_api_key: str
    openai_model: str
    temperature_analysis: float
    temperature_composition: float
    temperature_qa: float
    max_retries: int


def get_settings() -> Settings:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is missing. Add it to backend/.env before running the server."
        )

    configured_model = os.getenv("OPENAI_MODEL", "").strip()
    if configured_model and configured_model != FORCED_OPENAI_MODEL:
        raise RuntimeError(
            f"Only {FORCED_OPENAI_MODEL} is allowed. Update OPENAI_MODEL in backend/.env."
        )

    return Settings(
        openai_api_key=api_key,
        openai_model=FORCED_OPENAI_MODEL,
        temperature_analysis=float(os.getenv("TEMP_ANALYSIS", "0.2")),
        temperature_composition=float(os.getenv("TEMP_COMPOSITION", "0.35")),
        temperature_qa=float(os.getenv("TEMP_QA", "0.1")),
        max_retries=int(os.getenv("MAX_RETRIES", "2")),
    )
