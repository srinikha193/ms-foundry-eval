import unittest

from evaluator import ExactMatchGrader, TestCase, calculate_accuracy, evaluate


class TestEvaluator(unittest.TestCase):
    def setUp(self) -> None:
        self.grader = ExactMatchGrader()

    def test_exact_match_success(self) -> None:
        self.assertTrue(self.grader.grade("Paris", "Paris"))

    def test_exact_match_failure(self) -> None:
        self.assertFalse(self.grader.grade("Paris", "paris"))

    def test_evaluating_multiple_cases(self) -> None:
        test_cases = [TestCase("one", "1"), TestCase("two", "2")]
        responses = {"one": "1", "two": "wrong"}

        results = evaluate(
            test_cases,
            agent=lambda question: responses[question],
            grader=self.grader,
        )

        self.assertEqual(len(results), 2)
        self.assertTrue(results[0].passed)
        self.assertFalse(results[1].passed)

    def test_accuracy_calculation(self) -> None:
        test_cases = [
            TestCase("one", "1"),
            TestCase("two", "2"),
            TestCase("three", "3"),
        ]
        responses = {"one": "1", "two": "wrong", "three": "3"}

        results = evaluate(
            test_cases,
            agent=lambda question: responses[question],
            grader=self.grader,
        )

        self.assertEqual(calculate_accuracy(results), 2 / 3)


if __name__ == "__main__":
    unittest.main()
