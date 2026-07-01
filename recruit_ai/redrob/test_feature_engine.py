from recruit_ai.redrob.loader import load_candidates
from recruit_ai.redrob.feature_engine import build_candidate

candidate_json = next(
    load_candidates(
        "data/redrob/candidates.jsonl"
    )
)

# ===== DEBUG =====
print("Candidate Keys:")
print(candidate_json.keys())

print("\nFirst Raw Skill:")
print(candidate_json["skills"][0])
print(type(candidate_json["skills"][0]))

candidate = build_candidate(candidate_json)

print("\nType of candidate.skills[0].name:")
print(type(candidate.skills[0].name))

print("\nValue:")
print(candidate.skills[0].name)

print("\nFirst 5 Parsed Skills:")
for skill in candidate.skills[:5]:
    print(skill)