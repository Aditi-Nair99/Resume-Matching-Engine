from __future__ import annotations

import re
from pathlib import Path
from typing import Dict

from PyPDF2 import PdfReader
from docx import Document


def extract_text_from_resume(file_path: Path) -> str:
    suffix = file_path.suffix.lower()
    if suffix == ".pdf":
        return extract_pdf_text(file_path)
    if suffix == ".docx":
        return extract_docx_text(file_path)
    return file_path.read_text(encoding="utf-8", errors="ignore")


def extract_pdf_text(file_path: Path) -> str:
    reader = PdfReader(str(file_path))
    parts = []
    for page in reader.pages:
        parts.append(page.extract_text() or "")
    return "\n".join(parts)


def extract_docx_text(file_path: Path) -> str:
    doc = Document(str(file_path))
    return "\n".join([p.text for p in doc.paragraphs])


EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_PATTERN = re.compile(r"(?:\+91[-\s]?)?[6-9]\d{9}")


def extract_basic_fields(text: str, fallback_name: str = "") -> Dict[str, str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    probable_name = fallback_name or (lines[0] if lines else "Candidate")
    email = EMAIL_PATTERN.search(text)
    phone = PHONE_PATTERN.search(text)
    return {
        "full_name": probable_name[:255],
        "email": email.group(0) if email else "",
        "phone": phone.group(0) if phone else "",
    }
