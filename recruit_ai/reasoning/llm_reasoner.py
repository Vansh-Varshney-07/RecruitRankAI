import ollama

from recruit_ai.reasoning.prompts import SYSTEM_PROMPT


def generate_report(
    candidate_text: str,
    job_text: str,
):
    response = ollama.chat(
        model="qwen2.5-coder:7b-instruct",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": f"""
Candidate Resume

{candidate_text}


Job Description

{job_text}
""",
            },
        ],
    )

    return response["message"]["content"]