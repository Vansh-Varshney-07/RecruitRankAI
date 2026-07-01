from recruit_ai.candidate.repository import load_candidates

candidates = load_candidates()

print()
print("=" * 40)
print("Candidate Repository")
print("=" * 40)

print()

print(f"Loaded {len(candidates)} candidates")

print()

for c in candidates:

    print(c.name)