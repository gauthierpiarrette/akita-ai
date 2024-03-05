import os
import importlib
from argparse import _SubParsersAction

from akita.cli.command_factory import CommandFactory


class PluginManager:
    """Manages the loading of plugins and integrates them into the application.

    Attributes:
        command_factory: A CommandFactory instance for creating command instances.
        subparsers: The argparse subparsers collection for adding command subparsers.
    """

    def __init__(
        self, command_factory: CommandFactory, subparsers: _SubParsersAction
    ) -> None:
        """Initializes the PluginManager with a command factory and subparsers.

        Args:
            command_factory: A CommandFactory instance used
                             to create instances of commands.
            subparsers: The argparse subparsers to which
                        plugin subparsers will be added.
        """
        self.command_factory = command_factory
        self.subparsers = subparsers

    def load_plugins(self) -> None:
        """Loads plugins by discovering them in the predefined plugins directory.

        This method dynamically imports each discovered plugin module, instantiates
        the plugin class, and registers its subparsers with the main application's
        argument parser.

        Raises:
            Exception: If there is an error loading a plugin or its subparsers.
        """
        # Path to the plugins directory based on the project structure
        base_dir = os.path.dirname(
            os.path.dirname(__file__)
        )  # Go up one level to the 'akita' directory
        plugins_dir = os.path.join(base_dir, "plugins")

        # Iterate over each directory in the plugins directory
        for plugin in os.listdir(plugins_dir):
            plugin_path = os.path.join(plugins_dir, plugin)

            if os.path.isdir(plugin_path) and not plugin.startswith(("__", ".")):
                try:
                    # Dynamically import the plugin module from each plugin
                    plugin_module_path = f"akita.plugins.{plugin}.{plugin}_plugin"
                    plugin_module = importlib.import_module(plugin_module_path)

                    # Convention: Plugin class name follows <Name>Plugin
                    plugin_class_name = f"{plugin.capitalize()}Plugin"
                    plugin_class = getattr(plugin_module, plugin_class_name)

                    # Instantiate the plugin class and load its subparsers
                    plugin_instance = plugin_class(self.command_factory)
                    plugin_instance.load_subparsers(self.subparsers)

                except Exception as e:
                    print(f"Error loading plugin '{plugin}': {e}")
                    raise
