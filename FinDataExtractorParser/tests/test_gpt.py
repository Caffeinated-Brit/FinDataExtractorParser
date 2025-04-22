import pytest
from AI import gpt

def test_extract_structured_data_inner_mock(mocker):
    # Mock ChatOpenAI
    mock_llm = mocker.patch("AI.gpt.ChatOpenAI")
    mock_llm_instance = mock_llm.return_value

    # Mock JsonOutputParser
    mock_parser = mocker.patch("AI.gpt.JsonOutputParser")
    mock_parser_instance = mock_parser.return_value
    mock_parser_instance.get_format_instructions.return_value = "Format Instructions"

    # Mock PromptTemplate so it returns a callable when used with |
    mock_template = mocker.patch("AI.gpt.PromptTemplate")
    mock_template_instance = mock_template.return_value

    # Patch the sequence pipeline: prompt_template | llm | parser
    mock_sequence = mocker.MagicMock()
    mock_sequence.invoke.return_value = {"data": "exists"}

    # Chain the | operators by overriding __or__
    # prompt_template | llm returns another mock that will be | parser
    mock_template_instance.__or__.return_value = mock_sequence
    mock_sequence.__or__.return_value = mock_sequence

    # Run actual function
    result = gpt.extract_structured_data("test prompt", "test model")

    # Assert result is what we mocked
    assert result == {"data": "exists"}
