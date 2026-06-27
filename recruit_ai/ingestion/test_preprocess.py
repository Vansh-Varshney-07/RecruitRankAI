from recruit_ai.ingestion.pdf_loader import extract_text
from recruit_ai.ingestion.preprocess import clean_text

text = extract_text("data/raw/resumes/resume1.pdf")

cleaned = clean_text(text)

print("=" * 50)
print(cleaned[:1000])
print("=" * 50)

print(f"\nCharacters: {len(cleaned)}")