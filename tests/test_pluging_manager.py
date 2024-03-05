import pytest
from akita.cli.plugin_manager import PluginManager
from akita.cli.command_factory import CommandFactory
from argparse import ArgumentParser
from akita.plugins.template.template_plugin import TemplatePlugin


@pytest.fixture
def command_factory():
    return CommandFactory()


@pytest.fixture
def subparsers():
    parser = ArgumentParser()
    return parser.add_subparsers()


@pytest.fixture
def plugin_manager(command_factory, subparsers):
    return PluginManager(command_factory, subparsers)


def test_fixture_plugin_load_subparsers_called(plugin_manager, subparsers):
    # Pre-test setup: Store the original method to restore it later
    original_method = TemplatePlugin.load_subparsers

    # Attempt to track if the method was called
    was_called = False

    def mock_load_subparsers(self, subparsers):
        nonlocal was_called
        was_called = True
        original_method(self, subparsers)  # Call the original to maintain behavior

    # Temporarily replace the method with mock
    TemplatePlugin.load_subparsers = mock_load_subparsers

    plugin_manager.load_plugins()

    assert was_called, "TemplatePlugin's load_subparsers method was not called"

    # Restore the original method
    TemplatePlugin.load_subparsers = original_method


def test_template_plugin_error_handling(plugin_manager, subparsers):
    # Introduce an error in the load_subparsers method
    def mock_load_subparsers_with_error(self, subparsers):
        raise Exception("Test error during load_subparsers")

    original_method = TemplatePlugin.load_subparsers
    TemplatePlugin.load_subparsers = mock_load_subparsers_with_error

    # Load plugins and expect no unhandled exceptions
    with pytest.raises(Exception, match="Test error during load_subparsers"):
        plugin_manager.load_plugins()

    # Cleanup
    TemplatePlugin.load_subparsers = original_method
