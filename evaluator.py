"""Core models, graders, and evaluation functions."""

from dataclasses import dataclass
from typing import Callable, Protocol


@dataclass
class TestCase:
    question: str
    expected_answer: str


@dataclass
class EvaluationResult:
    question: str
    expected_answer: str
    actual_answer: str
    passed: bool


class Grader(Protocol):
    """Minimal interface implemented by response graders."""

    def grade(self, expected: str, actual: str) -> bool:
        ...


class ExactMatchGrader:
    """Grade a response by comparing it exactly with the expected answer."""

    def grade(self, expected: str, actual: str) -> bool:
        return expected == actual


def evaluate(
    test_cases: list[TestCase],
    agent: Callable[[str], str],
    grader: Grader,
) -> list[EvaluationResult]:
    """Run test cases through an agent and grader."""
    results = []

    for test_case in test_cases:
        actual_answer = agent(test_case.question)
        passed = grader.grade(test_case.expected_answer, actual_answer)
        results.append(
            EvaluationResult(
                question=test_case.question,
                expected_answer=test_case.expected_answer,
                actual_answer=actual_answer,
                passed=passed,
            )
        )

    return results


def calculate_accuracy(results: list[EvaluationResult]) -> float:
    """Return the fraction of evaluation results that passed."""
    if not results:
        return 0.0

    return sum(result.passed for result in results) / len(results)
