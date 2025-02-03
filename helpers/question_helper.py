from models.profile import Profile
from models.question import Question
from typing import List
import random

def get_random_questions(profile, questions: List[Question], k: int = 1) -> Question:
    weighted_questions = []
    weights = []
    for q in questions:
        if not q.enabled:
            continue
        stats = profile.get_statistics_for_question(q.id)
        # if question stats for this question do not exist, set 1.0 as the value
        weight = stats.weight if stats else 1.0
        weighted_questions.append(q)
        weights.append(weight)
    
    return random.choices(weighted_questions, weights, k=k)