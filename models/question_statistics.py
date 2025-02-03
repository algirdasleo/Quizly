from dataclasses import dataclass

@dataclass
class QuestionStatistics:
    times_answered: int = 0
    times_answered_correctly: int = 0
    weight: float = 1.0

    WEIGHT_INCREMENT: float = 0.2
    MAX_WEIGHT: float = 1.0
    MIN_WEIGHT: float = 0.1

    def update_statistics(self, answered_correctly: bool) -> None:
        self.weight += self.WEIGHT_INCREMENT if answered_correctly else -self.WEIGHT_INCREMENT
        if self.weight > self.MAX_WEIGHT:
            self.weight = self.MAX_WEIGHT
        elif self.weight < self.MIN_WEIGHT:
            self.weight = self.MIN_WEIGHT
        
        self.times_answered += 1
        if answered_correctly:
            self.times_answered_correctly += 1
    
    def to_dict(self, profile_id: int, question_id: int) -> dict:
        # Create dictionary for saving to CSV
        return {
            "profile_id": profile_id,
            "question_id": question_id,
            "times_answered": self.times_answered,
            "times_answered_correctly": self.times_answered_correctly,
            "weight": round(self.weight, 2)
        }