import pytest
from unittest.mock import patch
from AI.Ollama import process_text_with_llm, process_text_with_llm_and_schema


@pytest.fixture
def mock_ollama_response():
    class MockResponse:
        class Message:
            content = '{"message": "mock response"}'
        message = Message()
    return MockResponse()


@patch("AI.Ollama.ollama.chat")
def test_process_text_with_llm(mock_chat, mock_ollama_response):
    mock_chat.return_value = mock_ollama_response

    user_prompt = "Tell me a fact about space."
    response = process_text_with_llm(user_prompt)

    assert response == '{"message": "mock response"}'
    mock_chat.assert_called_once()


@patch("AI.Ollama.ollama.chat")
def test_process_text_with_llm_and_schema(mock_chat, mock_ollama_response):
    mock_chat.return_value = mock_ollama_response

    user_prompt = "Extract financial data."
    response = process_text_with_llm_and_schema(user_prompt)

    assert response == '{"message": "mock response"}'
    mock_chat.assert_called_once()
