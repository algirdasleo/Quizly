from dataclasses import dataclass
from typing import List

@dataclass
class Question:
    id: int
    title: str
    answer: str
    enabled: bool = True
    # Stores possible choices for multiple choice questions
    choices: List[str] = None
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "answer": self.answer,
            "enabled": self.enabled,
            "choices": self.to_choices_string()
        }
    
    def is_quiz(self) -> bool:
        return self.choices is not None and len(self.choices) > 0
    
    def to_choices_string(self):
        return "|".join(self.choices) if self.choices else ""
        