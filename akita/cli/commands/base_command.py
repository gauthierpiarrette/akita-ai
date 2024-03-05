from abc import ABC, abstractmethod


class BaseCommand(ABC):
    """
    Abstract base class for all command classes.
    Each specific command class should inherit from this class and
    implement the `execute` method.
    """

    @abstractmethod
    def execute(self, args):
        """
        Executes the command.

        Args:
            args: The command-line arguments specific to the command.
        """
        pass
