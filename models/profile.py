from dataclasses import dataclass
from typing import Dict, List
from models.question import Question
from models.question_statistics import QuestionStatistics

@dataclass
class Profile:
    id: int
    name: str
    question_statistics: Dict[int, QuestionStatistics] # Dict structure: [QuestionID, QuestionStatistics]
    
    def init_statistics(self, questions: List[Question]) -> None:
        # Ensures that statistics are set for all available questions
        if not self.question_statistics:
            self.question_statistics = {}
        if not questions:
            return
        for q in questions:
            if q.id not in self.question_statistics.keys():
                self.question_statistics[q.id] = QuestionStatistics()
    
    def get_statistics_for_question(self, question_id: int) -> QuestionStatistics:
        return self.question_statistics.get(question_id)
