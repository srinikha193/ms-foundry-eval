"""Mock agent used by the evaluation application."""


def mock_agent(question: str) -> str:
    """Return a canned response for a question."""
    responses = {
        "What is 2 + 2?": "4",
        "What is the capital of France?": "Paris",
        "What is the capital of Spain?": "Madrid",
        "Say hello.": "Hello",
    }
    return responses.get(question, "I don't know.")
