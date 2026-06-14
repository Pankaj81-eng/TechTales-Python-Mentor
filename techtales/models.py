from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class MentorCard:
    opening: str = ""
    pass_message: str = ""
    hints: tuple[tuple[str, str], ...] = ()

    def hint_for(self, label: str) -> str | None:
        for req_label, hint in self.hints:
            if req_label == label:
                return hint
        return None


@dataclass(frozen=True)
class Topic:
    key: str
    title: str
    summary: str
    lesson: str
    example_code: str
    challenge: str
    starter_code: str
    mentor: MentorCard = field(default_factory=MentorCard)
    expected_output: str | None = None


@dataclass(frozen=True)
class Progress:
    topic_key: str
    viewed: bool
    completed: bool
    viewed_at: str | None
    completed_at: str | None
    updated_at: str

    def to_dict(self) -> dict[str, object]:
        return {
            "topic_key": self.topic_key,
            "viewed": self.viewed,
            "completed": self.completed,
            "viewed_at": self.viewed_at,
            "completed_at": self.completed_at,
            "updated_at": self.updated_at,
        }


@dataclass(frozen=True)
class Submission:
    id: int
    topic_key: str
    code: str
    evaluator_status: str
    evaluator_message: str
    submitted_at: str
    challenge_passed: bool
    validation_details: str | None
    xp_awarded: int
    stdout: str
    runtime_error: str | None


@dataclass(frozen=True)
class EvaluationResult:
    status: str
    message: str


@dataclass(frozen=True)
class ExecutionResult:
    stdout: str
    error: str | None = None

    @property
    def succeeded(self) -> bool:
        return self.error is None


@dataclass(frozen=True)
class RequirementResult:
    label: str
    passed: bool
    suggestion: str = ""


@dataclass(frozen=True)
class ValidationResult:
    passed: bool
    requirements: tuple[RequirementResult, ...]
    feedback: str

    @property
    def status(self) -> str:
        return "passed" if self.passed else "needs_improvement"
