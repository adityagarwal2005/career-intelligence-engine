from __future__ import annotations


REQUIRED_HEADERS = (
    "1) PROJECTS TO ADD",
    "2) SKILLS TO ADD",
    "3) PROJECTS TO REMOVE",
)


def has_required_sections(text: str) -> bool:
    if not text:
        return False
    return all(header in text for header in REQUIRED_HEADERS)
