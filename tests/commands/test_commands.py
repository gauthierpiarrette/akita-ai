import pytest
from unittest.mock import MagicMock, patch


@pytest.fixture
def mock_command_factory():
    with patch("akita.cli.command_factory.CommandFactory") as MockFactory:
        mock_factory = MockFactory()
        mock_factory.get_command.return_value = MagicMock()
        yield mock_factory


def test_add_command_execution(mock_command_factory):
    args = MagicMock()
    args.files = ["file1.py", "file2.py"]
    mock_command_factory.get_command("add").execute(args)
    mock_command_factory.get_command("add").execute.assert_called_once_with(args)


def test_remove_command_execution(mock_command_factory):
    args = MagicMock()
    args.files = ["file1.py"]
    mock_command_factory.get_command("rm").execute(args)
    mock_command_factory.get_command("rm").execute.assert_called_once_with(args)


@pytest.mark.parametrize("all_flag", [True, False])
def test_show_command_execution(all_flag, mock_command_factory):
    args = MagicMock()
    args.all = all_flag
    args.type = None
    args.recent = None
    mock_command_factory.get_command("show").execute(args)
    mock_command_factory.get_command("show").execute.assert_called_once_with(args)


def test_review_command_execution(mock_command_factory):
    args = MagicMock()
    args.filename = ["review_file.py"]
    args.verbose = "moderate"
    args.lang = "en"
    args.use_git_staged = False
    args.use_git_staged_diff = False
    args.use_git_diff = False
    mock_command_factory.get_command("review").execute(args)
    mock_command_factory.get_command("review").execute.assert_called_once_with(args)


def test_assistant_command_execution(mock_command_factory):
    args = MagicMock()
    args.repo_path = "/path/to/repo"
    args.terminal = False
    mock_command_factory.get_command("assistant").execute(args)
    mock_command_factory.get_command("assistant").execute.assert_called_once_with(args)