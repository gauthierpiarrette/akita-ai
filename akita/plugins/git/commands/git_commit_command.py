from typing import Any, Dict, List, Optional
from akita.cli.commands.base_command import BaseCommand
from akita.utils.file_handler import FileHandler
from akita.services.text_generation.text_generator import TextGenerator
from akita.plugins.git.utils.utils import get_staged_files
import subprocess


class GitCommitCommand(BaseCommand):
    def __init__(self) -> None:
        self.file_handler: FileHandler = FileHandler()
        self.text_generator: TextGenerator = TextGenerator()

    def execute(self, args: Any) -> None:
        args: Dict[str, Any] = vars(args)

        try:
            files_to_commit: List[
                str
            ] = get_staged_files()  # Retrieves files staged for commit.

            if "message" in args and args["message"]:
                # Directly use the provided commit message if available.
                commit_message: str = args["message"]
                subprocess.run(["git", "commit", "-m", commit_message], check=True)

                self.file_handler.add_content(
                    "commit_message", commit_message, files_to_commit
                )
                print(f"Committed with message: {commit_message}")
                return  # Exit after committing with provided message.

            while True:
                # Generate or get a commit message, then ask the user for confirmation
                # or action.
                commit_message: Optional[
                    str
                ] = self.text_generator.generate_commit_message(
                    input_data=files_to_commit
                )

                if commit_message:
                    user_acceptance: str = input(
                        f"Commit message generated: '{commit_message}'.\
                        Use this? [y/n/edit/regen]: "
                    ).lower()

                    # Execute git commit with the generated message or based on user's
                    # choice.
                    if user_acceptance in ["y", "edit"]:
                        if user_acceptance == "edit":
                            commit_message = input("Enter your commit message: ")
                        subprocess.run(
                            ["git", "commit", "-m", commit_message], check=True
                        )
                        self.file_handler.add_content(
                            "commit_message", commit_message, files_to_commit
                        )
                        print(f"Committed with message: {commit_message}")
                        break
                    elif user_acceptance == "regen":
                        continue  # Regenerate the commit message.
                    elif user_acceptance == "n":
                        print("Commit aborted by user.")
                        break
                    else:
                        print("Invalid input. Commit aborted.")
                        break
                else:
                    print("No commit message was generated.")
                    break

        except subprocess.CalledProcessError as e:
            print(f"Error during 'git commit': {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
