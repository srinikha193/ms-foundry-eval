# AI Agent Evaluation

A small Python application for evaluating an AI agent's responses against expected answers. It currently uses a mocked agent and exact string matching, with a CLI report for each test case and the overall accuracy.

## Purpose

The project provides a minimal foundation for testing agent behavior:

1. Define questions and expected answers.
2. Ask an agent for a response to each question.
3. Grade each response.
4. Report pass/fail results and aggregate accuracy.

## Architecture

```text
app.py
  -> mock_agent() in agent.py
  -> evaluate() in evaluator.py
       -> Grader.grade()
  -> calculate_accuracy()
  -> CLI output
```

### `agent.py`

Contains `mock_agent()`, a deterministic stand-in for a real AI agent. It maps the sample questions to canned responses and returns `"I don't know."` for unknown questions.

### `evaluator.py`

Contains the evaluation domain and workflow:

- `TestCase` stores a question and expected answer.
- `EvaluationResult` stores the question, expected answer, actual answer, and pass/fail status.
- `Grader` defines the minimal grading contract: `grade(expected, actual) -> bool`.
- `ExactMatchGrader` implements exact string comparison.
- `evaluate()` runs test cases through an agent and grader.
- `calculate_accuracy()` returns the fraction of passing results.

### `app.py`

The command-line entry point. It defines sample test cases, injects the mocked agent and exact-match grader into `evaluate()`, and prints each result followed by overall accuracy.

### `tests/test_evaluator.py`

Unit tests covering exact-match success, exact-match failure, evaluation of multiple cases, and accuracy calculation.

## Evaluation Flow

For each `TestCase`, `evaluate()`:

1. Passes the question to the injected agent function.
2. Receives the actual response.
3. Passes the expected and actual responses to the injected grader.
4. Creates an `EvaluationResult` containing the outcome.

After all cases finish, `calculate_accuracy()` computes:

```text
number of passed cases / total number of cases
```

An empty result list produces an accuracy of `0.0`.

## Grader Abstraction

The `Grader` protocol keeps the evaluation workflow independent from the grading strategy. A new grader only needs to provide a compatible `grade(expected, actual)` method; `evaluate()` does not need to change.

`ExactMatchGrader` returns `True` only when the expected and actual strings are identical. Differences in capitalization, whitespace, or punctuation cause a failure.

## Dependency Injection

`evaluate()` receives both dependencies as arguments:

```python
results = evaluate(
    test_cases=test_cases,
    agent=mock_agent,
    grader=ExactMatchGrader(),
)
```

This allows the agent and grader to be replaced independently. The tests use small lambda functions as injected agents, while future versions can supply a real LLM client or a different grader.

## Running the Application

From the project directory:

```bash
python3 app.py
```

The application prints the status, expected answer, and actual answer for each sample case, followed by the overall accuracy.

## Running the Tests

```bash
python3 -m unittest discover -s tests
```

## Current Limitations

- The agent is mocked and uses a fixed in-memory response map.
- Test cases are defined directly in `app.py` rather than loaded from a file or service.
- Grading is limited to exact string comparison.
- There is no persistence, structured output, retry handling, or parallel execution.
- The CLI is the only reporting interface.

## Logical Future Improvements

- Add normalized or semantic evaluation for responses that are equivalent but not textually identical.
- Add an LLM-as-a-judge grader with a defined rubric and safeguards for inconsistent judgments.
- Integrate a real LLM-backed agent behind the existing callable interface.
- Support multiple graders per test case and report each score separately.
- Load test cases from JSON, CSV, or another reusable test-set format.
- Export evaluation results as JSON or CSV for analysis and CI workflows.
