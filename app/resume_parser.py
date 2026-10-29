import fitz


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract readable text from a PDF resume."""

    with fitz.open(stream=file_bytes, filetype="pdf") as pdf:
        text = "\n".join(page.get_text() for page in pdf).strip()

    if not text:
        raise ValueError(
            "No readable text found. The PDF may be scanned or image-based."
        )

    return text