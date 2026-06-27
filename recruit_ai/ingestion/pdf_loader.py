import fitz


def extract_text(pdf_path: str) -> str:
    """
    Extract text from a PDF resume.
    """

    document = fitz.open(pdf_path)

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text.strip()