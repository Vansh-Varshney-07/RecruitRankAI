import fitz


def _extract_document_text(document) -> str:
    text = ""

    for page in document:
        text += page.get_text()

    return text.strip()


def extract_text(pdf_path: str) -> str:
    """
    Extract text from a PDF file path.
    """

    document = fitz.open(pdf_path)

    try:
        return _extract_document_text(document)
    finally:
        document.close()


def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    """
    Extract text from uploaded PDF bytes.
    """

    document = fitz.open(
        stream=pdf_bytes,
        filetype="pdf",
    )

    try:
        return _extract_document_text(document)
    finally:
        document.close()
