from typing import Callable, Dict


class CommandFactory:
    """
    A factory for registering and retrieving command methods.

    Attributes:
        commands (Dict[str, Callable[[], None]]): A dictionary mapping command names
                                                  to their callable methods.
    """

    def __init__(self) -> None:
        """Initializes the command factory with an empty command registry."""
        self.commands: Dict[str, Callable[[], None]] = {}

    def register_command(
        self, command_name: str, command_method: Callable[[], None]
    ) -> None:
        """
        Register a command method with the factory.

        This method associates a command name with a callable command method
        in the factory's registry.
        If the command name already exists, it will overwrite the existing command
        method with the new one.

        Args:
            command_name: The name of the command (as a string).
                          This is the key used to retrieve the command method.
            command_method: The callable command method to be registered.
                            This method should not take any parameters
                            and should not return anything.
        """
        self.commands[command_name] = command_method

    def get_command(self, command_name: str) -> Callable[[], None]:
        """
        Retrieves a registered command method by its name.

        This method looks up the command name in the factory's registry and
        returns the associated command method if found.
        If the command name is not found, it raises a ValueError
        indicating that the command is unknown.

        Args:
            command_name: The name of the command to retrieve.

        Returns:
            The callable command method associated with the given command name.

        Raises:
            ValueError: If the command name is not found in the factory's registry.
        """
        command_method = self.commands.get(command_name)
        if command_method is None:
            print(f"Unknown command: {command_name}")
            raise ValueError(f"Unknown command: {command_name}")
        return command_method
