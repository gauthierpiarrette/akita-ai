import subprocess
from akita.utils.console import console
from akita.assistant.app_terminal import TerminalChat
from akita.assistant.config import ENV
from typing import NoReturn
import os


def run_chainlit_app(repo_path: str) -> NoReturn:
    ENV["REPO_PATH"] = repo_path
    console.log(f"Launching Akita Assistant with repository path: {repo_path}")

    current_file_path = os.path.realpath(__file__)
    package_root = os.path.dirname(os.path.dirname(current_file_path))
    app_directory = os.path.join(package_root, "assistant")

    try:
        process = subprocess.Popen(
            ["chainlit", "run", "app.py"], env=ENV, cwd=app_directory
        )
        process.wait()  # Wait for the process to terminate
    except KeyboardInterrupt:
        console.log("Stopping the app...")
        process.terminate()
        try:
            process.wait(timeout=5)  # Wait for the process to terminate
        except subprocess.TimeoutExpired:
            console.log("Forcing the app to stop...")
            process.kill()  # Forcefully kill the process if it doesn't terminate
        console.log("App has been stopped.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running the app: {e}")


def run_terminal_app(repo_path: str) -> NoReturn:
    ENV["REPO_PATH"] = repo_path
    console.log(f"Launching Akita Assistant with repository path: {repo_path}...")

    try:
        chat_app = TerminalChat()
        chat_app.run()
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while launching Akita Assistant: {e}")
    except KeyboardInterrupt:
        console.log("Launching of Akita Assistant was interrupted by user.")
