from recruit_ai.ingestion.pdf_loader import extract_text

text = extract_text("data/raw/resumes/resume1.pdf")

print(text[:1000])