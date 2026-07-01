def recommend(score):

    if score>=0.85:
        return "Strong Hire"

    if score>=0.70:
        return "Hire"

    if score>=0.55:
        return "Maybe"

    return "Reject"