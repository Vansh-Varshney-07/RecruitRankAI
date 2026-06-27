from recruit_ai.ranking.semantic_matcher import semantic_similarity


pairs = [

    ("Machine Learning", "ML"),

    ("Python", "Python"),

    ("Docker", "Kubernetes"),

    ("SQL", "PostgreSQL"),

    ("PyTorch", "TensorFlow"),

    ("Machine Learning", "Cooking"),

]


for a, b in pairs:

    score = semantic_similarity(a, b)

    print(f"{a:25} <-> {b:20} = {score:.3f}")