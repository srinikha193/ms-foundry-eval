"""Command-line entry point for the evaluation example."""

from agent import mock_agent
from evaluator import ExactMatchGrader, TestCase, calculate_accuracy, evaluate


def main() -> None:
    test_cases = [
        TestCase("What is 2 + 2?", "4"),
        TestCase("What is the capital of France?", "Paris"),
        TestCase("Say hello.", "Hello"),
        TestCase("What is the capital of Spain?", "Madrid"),
    ]

    results = evaluate(
        test_cases=test_cases,
        agent=mock_agent,
        grader=ExactMatchGrader(),
    )

    for result in results:
        status = "PASS" if result.passed else "FAIL"
        print(f"{status}: {result.question}")
        print(f"  Expected: {result.expected_answer}")
        print(f"  Actual:   {result.actual_answer}")

    print(f"\nAccuracy: {calculate_accuracy(results):.1%}")


if __name__ == "__main__":
    main()
