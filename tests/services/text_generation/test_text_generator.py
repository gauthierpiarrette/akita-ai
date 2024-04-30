import pytest
from unittest.mock import MagicMock
from akita.services.text_generation.text_generator import TextGenerator
from akita.api.base_ai_provider import AIProvider


@pytest.fixture(autouse=True)
def mock_dependencies(mocker):
    mocker.patch("akita.services.text_generation.text_generator.FileHandler")
    mocker.patch("akita.services.text_generation.text_generator.PromptBuilder")
    mocker.patch(
        "akita.api.provider_factory.ProviderFactory.get_provider",
        return_value=MagicMock(spec=AIProvider),
    )
    mocker.patch(
        "akita.services.text_generation.text_generator.Settings.DEFAULT_PROMPT_DIR",
        "./prompts",
    )
    mocker.patch(
        "akita.services.text_generation.text_generator.Settings.MODEL_CONFIG_FILE",
        "./model_config.json",
    )
    mocker.patch(
        "akita.services.text_generation.text_generator.Settings.DEFAULT_VERBOSITY",
        "moderate",
    )
    mocker.patch(
        "akita.services.text_generation.text_generator.Settings.DEFAULT_LANGUAGE", "en"
    )
    mocker.patch("os.path.isfile", return_value=True)


@pytest.fixture
def text_generator():
    return TextGenerator()


def test_initialization(text_generator):
    assert isinstance(text_generator.file_handler, MagicMock)
    assert isinstance(text_generator.prompt_builder, MagicMock)
    assert isinstance(text_generator.ai_provider, MagicMock)


def test_generate_docstring_calls_api_with_correct_params(text_generator, mocker):
    mocker.patch.object(
        text_generator.ai_provider, "call_api", return_value="Mocked API Response"
    )
    text_generator.prompt_builder.get_prompt.return_value = "test prompt"
    result = text_generator.generate_docstring("def add(x, y): return x + y")

    text_generator.prompt_builder.get_prompt.assert_called_with(
        "docstring", "def add(x, y): return x + y"
    )
    text_generator.ai_provider.call_api.assert_called_with(
        "test prompt", max_tokens=3000
    )
    assert result == "Mocked API Response"


def test_generate_inline_comments_calls_api_with_correct_params(text_generator, mocker):
    mocker.patch.object(
        text_generator.ai_provider, "call_api", return_value="Mocked Inline Comments"
    )
    text_generator.prompt_builder.get_prompt.return_value = "inline comment prompt"
    result = text_generator.generate_inline_comments("def add(x, y): return x + y")

    text_generator.prompt_builder.get_prompt.assert_called_with(
        "inline_comments", "def add(x, y): return x + y"
    )
    text_generator.ai_provider.call_api.assert_called_with(
        "inline comment prompt", max_tokens=4000
    )
    assert result == "Mocked Inline Comments"


def test_generate_description_files_calls_api_with_correct_params(text_generator):
    text_generator.file_handler.read_files.return_value = "Combined file content"
    text_generator.prompt_builder.get_prompt.return_value = "describe files prompt"
    text_generator.ai_provider.call_api.return_value = "Mocked Description Files"
    files = ["path/to/file1.py", "path/to/file2.py"]
    result = text_generator.generate_description_files(files)
    text_generator.file_handler.read_files.assert_called_with(files)
    text_generator.prompt_builder.get_prompt.assert_called_with(
        "describe_files", "Combined file content"
    )
    assert result == "Mocked Description Files"


def test_generate_description_code_diff_calls_api_with_correct_params(text_generator):
    text_generator.prompt_builder.get_prompt.return_value = "code diff prompt"
    text_generator.ai_provider.call_api.return_value = "Mocked Code Diff Description"
    diff = "def add(x, y): return x + y"
    result = text_generator.generate_description_code_diff(diff)
    text_generator.prompt_builder.get_prompt.assert_called_with(
        "describe_code_diff", diff
    )
    text_generator.ai_provider.call_api.assert_called_with(
        "code diff prompt", max_tokens=500
    )
    assert result == "Mocked Code Diff Description"


def test_generate_commit_message_calls_api_with_correct_params(text_generator):
    text_generator.prompt_builder.get_prompt.return_value = "commit message prompt"
    text_generator.ai_provider.call_api.return_value = "Mocked Commit Message"
    code_changes = "Added new feature"
    result = text_generator.generate_commit_message(code_changes)
    text_generator.prompt_builder.get_prompt.assert_called_with(
        "commit_message", code_changes
    )
    text_generator.ai_provider.call_api.assert_called_with(
        "commit message prompt", max_tokens=60
    )
    assert result == "Mocked Commit Message"


def test_generate_readme_calls_api_with_correct_params(text_generator):
    text_generator.prompt_builder.get_prompt.return_value = "readme prompt"
    text_generator.ai_provider.call_api.return_value = "Mocked README"
    project_overview = "This project is a sample."
    result = text_generator.generate_readme(project_overview)
    text_generator.prompt_builder.get_prompt.assert_called_with(
        "readme", project_overview
    )
    text_generator.ai_provider.call_api.assert_called_with(
        "readme prompt", max_tokens=3000
    )
    assert result == "Mocked README"


def test_generate_review_calls_api_with_correct_params(text_generator):
    text_generator.prompt_builder.get_prompt.return_value = "review prompt"
    text_generator.ai_provider.call_api.return_value = "Mocked Review"
    code_for_review = "def add(x, y): return x + y"
    result = text_generator.generate_review(code_for_review)
    text_generator.prompt_builder.get_prompt.assert_called_with(
        "review", code_for_review
    )
    text_generator.ai_provider.call_api.assert_called_with(
        "review prompt", max_tokens=3000
    )
    assert result == "Mocked Review"


def test_generate_tests_calls_api_with_correct_params(text_generator):
    text_generator.prompt_builder.get_prompt.return_value = "tests prompt"
    text_generator.ai_provider.call_api.return_value = "Mocked Tests"
    code_to_test = "def add(x, y): return x + y"
    result = text_generator.generate_tests(code_to_test)
    text_generator.prompt_builder.get_prompt.assert_called_with("tests", code_to_test)
    text_generator.ai_provider.call_api.assert_called_with(
        "tests prompt", max_tokens=3000
    )
    assert result == "Mocked Tests"


def test_generate_docstring_with_list_input(text_generator):
    text_generator.file_handler.read_files.return_value = "Combined file content"
    text_generator.ai_provider.call_api.return_value = "Mocked API Response"
    files = ["path/to/file1.py", "path/to/file2.py"]
    result = text_generator.generate_docstring(files)
    text_generator.file_handler.read_files.assert_called_with(files)
    text_generator.prompt_builder.get_prompt.assert_called_with(
        "docstring", "Combined file content"
    )
    assert result == "Mocked API Response"


def test_generate_inline_comments_with_list_input(text_generator):
    text_generator.file_handler.read_files.return_value = (
        "Combined inline comment content"
    )
    text_generator.ai_provider.call_api.return_value = "Mocked Inline Comments"
    files = ["path/to/file1.py", "path/to/file2.py"]
    result = text_generator.generate_inline_comments(files)
    text_generator.file_handler.read_files.assert_called_with(files)
    text_generator.prompt_builder.get_prompt.assert_called_with(
        "inline_comments", "Combined inline comment content"
    )
    assert result == "Mocked Inline Comments"


def test_generate_readme_with_list_input(text_generator):
    text_generator.file_handler.read_files.return_value = "Combined README content"
    text_generator.ai_provider.call_api.return_value = "Mocked README"
    files = ["path/to/file1.md", "path/to/file2.md"]
    result = text_generator.generate_readme(files)
    text_generator.file_handler.read_files.assert_called_with(files)
    text_generator.prompt_builder.get_prompt.assert_called_with(
        "readme", "Combined README content"
    )
    assert result == "Mocked README"


def test_generate_review_with_list_input(text_generator):
    text_generator.file_handler.read_files.return_value = "Combined review content"
    text_generator.ai_provider.call_api.return_value = "Mocked Review"
    files = ["path/to/file1.py", "path/to/file2.py"]
    result = text_generator.generate_review(files)
    text_generator.file_handler.read_files.assert_called_with(files)
    text_generator.prompt_builder.get_prompt.assert_called_with(
        "review", "Combined review content"
    )
    assert result == "Mocked Review"


def test_generate_docstring_with_optional_params(text_generator):
    text_generator.generate_docstring("input", verbosity="high", language="fr")
    assert text_generator.prompt_builder.verbosity == "high"
    assert text_generator.prompt_builder.language == "fr"


def test_generate_inline_comments_with_optional_params(text_generator):
    input_code = "def add(x, y): return x + y"
    text_generator.generate_inline_comments(input_code, verbosity="high", language="fr")
    assert text_generator.prompt_builder.verbosity == "high"
    assert text_generator.prompt_builder.language == "fr"
    text_generator.prompt_builder.get_prompt.assert_called_with(
        "inline_comments", input_code
    )


def test_generate_description_files_with_optional_params(text_generator):
    input_data = ["path/to/file1.py", "path/to/file2.py"]
    text_generator.generate_description_files(
        input_data, verbosity="low", language="fr"
    )
    assert text_generator.prompt_builder.verbosity == "low"
    assert text_generator.prompt_builder.language == "fr"
    text_generator.file_handler.read_files.assert_called_with(input_data)


def test_generate_description_code_diff_with_optional_params(text_generator):
    code_diff = "diff --git a/file1.py b/file1.py"
    text_generator.generate_description_code_diff(
        code_diff, verbosity="moderate", language="fr"
    )
    assert text_generator.prompt_builder.verbosity == "moderate"
    assert text_generator.prompt_builder.language == "fr"
    text_generator.prompt_builder.get_prompt.assert_called_with(
        "describe_code_diff", code_diff
    )


def test_generate_commit_message_with_optional_params(text_generator):
    code_changes = "Added new feature"
    text_generator.generate_commit_message(code_changes, verbosity="low", language="es")
    assert text_generator.prompt_builder.verbosity == "low"
    assert text_generator.prompt_builder.language == "es"
    text_generator.prompt_builder.get_prompt.assert_called_with(
        "commit_message", code_changes
    )


def test_generate_readme_with_optional_params(text_generator):
    project_overview = "This project is a sample."
    text_generator.generate_readme(project_overview, verbosity="low", language="pt")
    assert text_generator.prompt_builder.verbosity == "low"
    assert text_generator.prompt_builder.language == "pt"
    text_generator.prompt_builder.get_prompt.assert_called_with(
        "readme", project_overview
    )


def test_generate_review_with_optional_params(text_generator):
    code_for_review = "def subtract(x, y): return x - y"
    text_generator.generate_review(code_for_review, verbosity="moderate", language="fr")
    assert text_generator.prompt_builder.verbosity == "moderate"
    assert text_generator.prompt_builder.language == "fr"
    text_generator.prompt_builder.get_prompt.assert_called_with(
        "review", code_for_review
    )


def test_generate_tests_with_optional_params(text_generator):
    code_to_test = "def multiply(x, y): return x * y"
    text_generator.generate_tests(code_to_test, verbosity="moderate", language="fr")
    assert text_generator.prompt_builder.verbosity == "moderate"
    assert text_generator.prompt_builder.language == "fr"
    text_generator.prompt_builder.get_prompt.assert_called_with("tests", code_to_test)


def test_process_input_with_invalid_input(text_generator):
    with pytest.raises(ValueError) as exc_info:
        text_generator.generate_docstring(123)
    assert "Input data must be a list of file paths or a string" in str(exc_info.value)
