from abc import ABC, abstractmethod
import os
import importlib


class BasePlugin(ABC):
    """
    Abstract base class for all plugins.
    Each plugin should extend this class and implement the load_subparsers method.
    """

    def __init__(self, command_factory):
        super().__init__()
        self.command_factory = command_factory
        self.load_commands()

    def load_commands(self):
        plugin_name = self.__class__.__name__.replace("Plugin", "").lower()
        commands_module = f"{self.__module__.rsplit('.', 1)[0]}.commands"
        commands_path = os.path.join(os.path.dirname(__file__), plugin_name, "commands")

        for filename in os.listdir(commands_path):
            if (
                filename.endswith(".py")
                and not filename.startswith("__")
                and "command" in filename
            ):
                class_file_name = filename[:-3]  # Strip .py from filename
                command_name = filename[:-11]  # Strip .py and command from filename
                module_path = f"{commands_module}.{class_file_name}"
                command_module = importlib.import_module(module_path)

                # Construct the class name based on the convention.
                # Assuming your class names are CamelCase and match the command name
                class_name = "".join(
                    word.capitalize() for word in class_file_name.split("_")
                )

                # Retrieve the command class from the module
                command_class = getattr(command_module, class_name)

                # Register the command with the command factory
                self.command_factory.register_command(command_name, command_class)

    @abstractmethod
    def load_subparsers(self, subparsers, command_factory):
        """
        Load subparsers into the main parser.

        Args:
            subparsers: The subparsers to load into.
            command_factory: The factory for creating command instances.
        """
        pass
