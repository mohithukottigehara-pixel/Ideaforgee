"""Input validation and text extraction for PDFs."""
from pathlib import Path
import fitz

MAX_UPLOAD_BYTES = 10 * 1024 * 1024


def extract_pdf_text(uploaded_file) -> str:
    name = getattr(uploaded_file, "name", "document.pdf")
    if Path(name).suffix.lower() != ".pdf":
        raise ValueError("Please upload a PDF file.")
    raw = uploaded_file.getvalue()
    if not raw:
        raise ValueError("The selected PDF is empty.")
    if len(raw) > MAX_UPLOAD_BYTES:
        raise ValueError("The PDF exceeds the 10 MB upload limit.")
    if not raw.startswith(b"%PDF"):
        raise ValueError("This file does not appear to be a valid PDF.")
    try:
        with fitz.open(stream=raw, filetype="pdf") as doc:
            if doc.needs_pass:
                raise ValueError("This PDF is password-protected. Upload an unlocked copy.")
            text = "\n\n".join(page.get_text("text") for page in doc)
    except ValueError:
        raise
    except Exception as exc:
        raise ValueError("The PDF could not be read. Try another copy of the file.") from exc
    if not text.strip():
        raise ValueError("No readable text was found. This may be a scanned PDF; OCR is not included in this MVP.")
    return text.strip()
