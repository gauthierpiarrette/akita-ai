import pytest
from unittest.mock import Mock, patch
from akita.api.openai_client import OpenAIClient


class TestOpenAIClient:
    @pytest.fixture
    def mock_openai_client(self):
        """Fixture to mock the OpenAI client."""
        with patch("akita.api.openai_client.OpenAI") as mock:
            yield mock()

    @pytest.fixture
    def mock_rich_console(self):
        """Fixture to mock the rich Console."""
        with patch("akita.api.openai_client.console") as mock:
            yield mock

    def test_initialization_with_defaults(self):
        """Test that the client initializes with default values correctly."""
        client = OpenAIClient()
        assert client.openai_client is not None
        assert client.console is not None

    def test_initialization_with_custom_params(self):
        """Test initialization with custom OpenAI client and console."""
        custom_client = Mock()
        custom_console = Mock()
        client = OpenAIClient(openai_client=custom_client, rich_console=custom_console)
        assert client.openai_client == custom_client
        assert client.console == custom_console

    def test_call_openai_api_success(self, mock_openai_client):
        """Test successful API call."""
        expected_response = "Test response"
        mock_openai_client.chat.completions.create.return_value = Mock(
            choices=[Mock(message=Mock(content=expected_response))]
        )

        client = OpenAIClient(openai_client=mock_openai_client)
        response = client.call_openai_api(prompt="Test prompt", max_tokens=50)

        assert response == expected_response

    def test_call_openai_api_failure_invalid_response(self, mock_openai_client):
        """Test handling of an invalid response structure."""
        mock_openai_client.chat.completions.create.return_value = Mock(choices=[])

        client = OpenAIClient(openai_client=mock_openai_client)
        response = client.call_openai_api(prompt="Test prompt", max_tokens=50)

        assert response is None

    def test_call_openai_api_exception_handling(self, mock_openai_client):
        """Test handling of exceptions during API call."""
        mock_openai_client.chat.completions.create.side_effect = Exception(
            "Test exception"
        )

        client = OpenAIClient(openai_client=mock_openai_client)
        response = client.call_openai_api(prompt="Test prompt", max_tokens=50)

        assert response is None
