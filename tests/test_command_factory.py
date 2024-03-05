import pytest
from akita.cli.command_factory import CommandFactory


def test_initialization():
    factory = CommandFactory()
    assert isinstance(factory.commands, dict)
    assert len(factory.commands) == 0


def a_command_method():
    return "Test command executed"


def another_command_method():
    return "Another command executed"


def test_register_command():
    factory = CommandFactory()
    command_name = "test_command"
    factory.register_command(command_name, a_command_method)

    assert command_name in factory.commands
    assert factory.commands[command_name] == a_command_method


def test_register_command_overwrites_existing_command():
    factory = CommandFactory()
    command_name = "test_command"

    factory.register_command(command_name, a_command_method)
    factory.register_command(command_name, another_command_method)

    assert factory.commands[command_name] == another_command_method


def test_get_command_success():
    factory = CommandFactory()
    command_name = "test_command"
    factory.register_command(command_name, a_command_method)

    retrieved_command = factory.get_command(command_name)
    assert retrieved_command == a_command_method


def test_get_command_unknown_raises_value_error():
    factory = CommandFactory()
    command_name = "unknown_command"

    with pytest.raises(ValueError) as exc_info:
        factory.get_command(command_name)

    assert str(exc_info.value) == f"Unknown command: {command_name}"


def test_get_command_logs_error_for_unknown_command(caplog):
    factory = CommandFactory()
    command_name = "unknown_command"

    with pytest.raises(ValueError):
        factory.get_command(command_name)
