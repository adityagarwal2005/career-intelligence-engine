from __future__ import annotations

from io import BytesIO

from fastapi import UploadFile
from PyPDF2 import PdfReader
from docx import Document


class ResumeParsingError(ValueError):
    pass


SUPPORTED_EXTENSIONS = {".txt", ".pdf", ".docx", ".md"}


async def extract_resume_text(resume_file: UploadFile) -> str:
    if not resume_file.filename:
        raise ResumeParsingError("Resume file name is missing.")

    filename = resume_file.filename.lower()
    extension = "." + filename.rsplit(".", 1)[-1] if "." in filename else ""

    if extension not in SUPPORTED_EXTENSIONS:
        raise ResumeParsingError(
            "Unsupported resume format. Upload .txt, .md, .pdf, or .docx"
        )

    content = await resume_file.read()
    if not content:
        raise ResumeParsingError("Uploaded resume file is empty.")

    if extension in {".txt", ".md"}:
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            text = content.decode("latin-1", errors="ignore")
        return text.strip()

    if extension == ".pdf":
        try:
            reader = PdfReader(BytesIO(content))
            pages = [page.extract_text() or "" for page in reader.pages]
            return "\n".join(pages).strip()
        except Exception as exc:
            raise ResumeParsingError(f"Unable to parse PDF resume: {exc}") from exc

    if extension == ".docx":
        try:
            doc = Document(BytesIO(content))
            lines = [p.text for p in doc.paragraphs if p.text and p.text.strip()]
            return "\n".join(lines).strip()
        except Exception as exc:
            raise ResumeParsingError(f"Unable to parse DOCX resume: {exc}") from exc

    raise ResumeParsingError("Unsupported resume format.")
