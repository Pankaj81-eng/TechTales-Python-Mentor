from abc import ABC, abstractmethod

from techtales.models import EvaluationResult, Topic


class Evaluator(ABC):
    @abstractmethod
    def evaluate(self, topic: Topic, submitted_code: str) -> EvaluationResult:
        """Evaluate a submission without coupling the app to a specific evaluator."""


class SaveOnlyEvaluator(Evaluator):
    def evaluate(self, topic: Topic, submitted_code: str) -> EvaluationResult:
        return EvaluationResult(
            status="saved_for_review",
            message=(
                f"Your {topic.title} challenge was saved. Automated mentor feedback "
                "will be added in a future version."
            ),
        )
