from typing import List
from akita.cli.commands.base_command import BaseCommand
from akita.utils.file_handler import FileHandler
from akita.plugins.git.utils.utils import get_staged_files
import subprocess


class GitAddCommand(BaseCommand):
    def __init__(self) -> None:
        self.file_handler: FileHandler = FileHandler()

    def execute(self, args: List[str]) -> None:
        # Convert Namespace to a list of arguments.
        args: List[str] = vars(args).get("files", [])

        try:
            # Get the list of staged files before running git add to compare later.
            before_add: List[str] = get_staged_files()

            # Run git add with all arguments provided to the command.
            subprocess.run(["git", "add"] + args, check=True)
            print("Git add command executed.")

            # Get the list of staged files after running git add to find newly staged
            # files.
            after_add: List[str] = get_staged_files()

            # Determine which files were newly staged by comparing before and after
            # lists.
            new_files: List[str] = [
                file for file in after_add if file not in before_add
            ]

            # Update the file handler with newly staged files, if any.
            if new_files:
                self.file_handler.add_files(new_files)
                print(f"Newly staged files added to file handler: {new_files}")
            else:
                print("No new files were staged.")

        except subprocess.CalledProcessError as e:
            # Log subprocess-specific errors, for example, if the 'git add' command
            # fails.
            print(f"Error during 'git add': {e}")
