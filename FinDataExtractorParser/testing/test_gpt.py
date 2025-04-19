import unittest
from unittest.mock import patch, MagicMock
from AI.gpt import extract_structured_data

class TestExtractStructuredData(unittest.TestCase):

    @patch('AI.gpt.ChatOpenAI')  # Mock the ChatOpenAI class
    @patch('AI.gpt.RunnableSequence')  # Mock the RunnableSequence class
    def test_extract_structured_data(self, MockRunnableSequence, MockChatOpenAI):
        # Mock ChatOpenAI response, try to avoid api calls, gotta save that dough ya know
        mock_llm_instance = MagicMock()
        mock_llm_instance.invoke.return_value = {"response": "3 space facts."}
        MockChatOpenAI.return_value = mock_llm_instance

        # Mock RunnableSequence
        mock_sequence_instance = MagicMock()
        mock_sequence_instance.invoke.return_value = {"response": "3 space facts."}
        MockRunnableSequence.return_value = mock_sequence_instance

        # Test without page_number argument
        prompt = "give me 3 space facts."
        result = extract_structured_data(prompt)
        self.assertEqual(result, {"response": "3 space facts."})

        # Test with page_number argument, we never use page number arg. pdfs are spliced in front end
        # prompt_with_page = "give me facts about Mars."
        # result = extract_structured_data(prompt_with_page, page_number=1)
        # self.assertEqual(result, {"response": "3 space facts."})

        # check if mocked classes were called
        MockChatOpenAI.assert_called_once_with(temperature=0, model="gpt-3.5-turbo-1106")
        MockRunnableSequence.assert_called_once()

# if __name__ == '__main__':
#     unittest.main()
