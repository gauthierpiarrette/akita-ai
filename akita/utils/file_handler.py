import json
import os
import fnmatch
import datetime
import chardet
from typing import Optional, Set, List, Union
from akita.utils.console import console
from akita.cli.config import Config


class FileHandler:
    """Manages file operations such as reading, writing,
    and tracking files within a specified directory."""

    def __init__(
        self,
        akita_dir: str = Config.AKITA_DIR,
        akita_data_file: str = Config.AKITA_DATA_FILE,
        akita_ignore_file: str = Config.AKITA_IGNORE_FILE,
        max_content_entries: int = Config.MAX_CONTENT_ENTRIES,
    ) -> None:
        """
        Initializes the FileHandler with the specified directory and file settings.

        Args:
            akita_dir: The directory where Akita data and configurations are stored.
            akita_data_file: The file name for storing Akita data.
            akita_ignore_file: The file name for storing patterns of files to ignore.
            max_content_entries: The maximum number of content entries to store.
        """
        self.akita_dir = akita_dir
        self.max_content_entries = max_content_entries
        self.akita_data_file = os.path.join(self.akita_dir, akita_data_file)
        self.akita_ignore_file = akita_ignore_file
        self.ensure_akita_dir_exists()
        self._init_akitaignore_file()

    def ensure_akita_dir_exists(self) -> None:
        """Ensures the Akita directory exists, creating it if necessary."""
        if not os.path.exists(self.akita_dir):
            os.makedirs(self.akita_dir)

    def get_stored_data(self) -> dict:
        """Retrieves stored data from the Akita data file.

        Returns:
            A dictionary containing the stored data.
            Returns an empty dictionary if the file does not exist.
        """
        if not os.path.exists(self.akita_data_file):
            return {}
        with open(self.akita_data_file, "r", encoding="utf-8") as file:
            return json.load(file)

    def store_data(self, data: dict) -> None:
        """Stores the given data in the Akita data file.

        Args:
            data: A dictionary containing the data to be stored.
        """
        with open(self.akita_data_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def remove_files(self, files: Optional[Set[str]] = None) -> None:
        """Removes specified files from the stored data or all files if none are specified.

        Args:
            files: An optional set of file paths to remove.
                   If None, all files will be removed after confirmation.
        """
        data = self.get_stored_data()
        removed_count = 0

        if files is None:
            user_input = input("Are you sure you want to remove all files? (y/n): ")
            if user_input.lower() == "y":
                removed_count = len(data.get("files", []))
                data["files"] = []
                print(f"All files have been removed. Total removed: {removed_count}")
            else:
                print("File removal cancelled.")
        else:
            existing_files = set(data.get("files", []))
            files_to_remove = set(files)
            removed_count = len(files_to_remove.intersection(existing_files))

            if not files_to_remove.issubset(existing_files):
                print("Some files were not found and could not be removed.")

            data["files"] = list(existing_files - files_to_remove)
            print(f"Removed files: {files_to_remove}. Total removed: {removed_count}")

        self.store_data(data)

    def get_stored_files(self) -> List[str]:
        """Retrieves a list of stored file paths.

        Returns:
            A list of file paths stored in the Akita data file.
        """
        data = self.get_stored_data()
        return data.get("files", [])

    def add_content(self, content_type: str, text: str, files: List[str]) -> None:
        """Appends new content to the stored data,
           ensuring the total does not exceed the maximum entries.

        Args:
            content_type: The type of content being added (e.g., "commit_message").
            text: The text content to add.
            files: A list of file paths associated with the content.
        """
        data = self.get_stored_data()

        if "history" not in data:
            data["history"] = {"content": []}

        data["history"]["content"].append(
            {"type": content_type, "text": text, "files": files}
        )

        if len(data["history"]["content"]) > self.max_content_entries:
            data["history"]["content"] = data["history"]["content"][
                -self.max_content_entries :
            ]

        self.store_data(data)

    def add_files(self, files: List[str]) -> None:
        """Adds a list of files to the stored data,
           ignoring duplicates and files matching ignore patterns.

        Args:
            files: A list of file paths to add.
        """
        data = self.get_stored_data()
        if "files" not in data:
            data["files"] = []

        ignored_files = self._read_ignore_file()
        ignored_patterns = [pattern for pattern in ignored_files if "*" in pattern]

        added_files = set()
        for file in files:
            if os.path.isdir(file):
                for root, dirs, files_in_dir in os.walk(file):
                    for name in files_in_dir:
                        file_path = os.path.join(root, name)
                        if not self._is_ignored(
                            file_path, ignored_files, ignored_patterns
                        ):
                            added_files.add(file_path)
            elif file == ".":
                for root, dirs, files_in_dir in os.walk("."):
                    for name in files_in_dir:
                        file_path = os.path.join(root, name)
                        if not self._is_ignored(
                            file_path, ignored_files, ignored_patterns
                        ):
                            added_files.add(file_path)
            elif os.path.exists(file) and not self._is_ignored(
                file, ignored_files, ignored_patterns
            ):
                added_files.add(file)
            else:
                print(f"File not found or ignored: {file}")

        data["files"] = list(
            set(data["files"]).union({os.path.relpath(f) for f in added_files})
        )
        self.store_data(data)

        if added_files:
            print(f"Added {len(added_files)} files:")
            for f in added_files:
                print(f"  {f}")
        else:
            print("No new files were added.")

    def _is_ignored(
        self, file_path: str, ignored_files: List[str], ignored_patterns: List[str]
    ) -> bool:
        """Determines if a given file path matches any of the ignore patterns.

        Args:
            file_path: The path of the file to check.
            ignored_files: A list of ignored file names.
            ignored_patterns: A list of ignored file name patterns.

        Returns:
            True if the file path matches an ignore pattern or name, False otherwise.
        """
        relative_path = os.path.relpath(file_path)
        path_components = relative_path.split(os.sep)

        for component in path_components:
            if component in ignored_files or any(
                fnmatch.fnmatch(component, pattern) for pattern in ignored_patterns
            ):
                return True

        return False

    def _read_ignore_file(self) -> List[str]:
        """Reads the ignore file and returns a list of ignored files and patterns.

        Returns:
            A list of file names and patterns to ignore.
        """
        ignore_file_path = os.path.join(self.akita_dir, self.akita_ignore_file)
        ignored_files = []
        if os.path.exists(ignore_file_path):
            with open(ignore_file_path, "r", encoding="utf-8") as file:
                ignored_files = [
                    line.strip() for line in file.readlines() if line.strip()
                ]

        return ignored_files

    def show_files(self) -> None:
        """Displays a list of currently stored file paths."""
        data = self.get_stored_data()
        if not data.get("files"):
            print("No files are currently stored.")
            return
        print(f"Stored files: {data['files']}")

    def show_all(self) -> None:
        """Displays all stored data, including files and content history."""
        data = self.get_stored_data()

        if not data:
            print("No data is currently stored in Akita.")
            return

        if "files" in data:
            print(f"Stored files: {data['files']}")
        else:
            print("No files are currently stored.")

        if "history" in data and "content" in data["history"]:
            for item in data["history"]["content"]:
                console.print(
                    f"{item['type']}: {item['text']} for files: {item['files']}"
                )
        else:
            print("No content history found.")

    def show_content(self, content_type: Optional[str] = None) -> None:
        """Displays stored content of a specific type, or all content if no type is specified.

        Args:
            content_type: The specific type of content to display.
                          If None, all content is displayed.
        """
        data = self.get_stored_data()
        if "history" in data and "content" in data["history"]:
            for item in data["history"]["content"]:
                if content_type is None or item["type"] == content_type:
                    print(f"{item['type']}: {item['text']} for files: {item['files']}")
        else:
            print("No content history found.")

    def init_files(self) -> None:
        """Initializes the file storage, resetting all stored data."""
        if os.path.exists(self.akita_data_file):
            user_input = input(
                "This will reset all data in .akita_data.json. \
                 Are you sure you want to continue? (y/n): "
            )
            if user_input.lower() != "y":
                print("Initialization cancelled.")
                return

        initial_data = {"files": [], "history": {"content": []}}
        if not os.path.exists(self.akita_dir):
            os.makedirs(self.akita_dir)
        self._init_akitaignore_file()

        with open(self.akita_data_file, "w", encoding="utf-8") as file:
            json.dump(initial_data, file, indent=4)

        print("Initialization completed.")

    def _init_akitaignore_file(self) -> None:
        """Initializes the ignore file with default settings if it does not exist."""
        ignore_file_path = os.path.join(self.akita_dir, self.akita_ignore_file)
        if not os.path.exists(ignore_file_path):
            with open(ignore_file_path, "w", encoding="utf-8") as file:
                file.write("# Add filenames to ignore when running 'akita add .'\n")
                file.write("# Each filename or pattern should be on a new line\n")
                file.write("*.git*\n")
                file.write(".akita*\n")

    def show_content_by_type(self, content_type: str) -> None:
        """Displays stored content filtered by a specific type.

        Args:
            content_type: The type of content to display.
        """
        data = self.get_stored_data()
        if "history" in data and "content" in data["history"]:
            for item in data["history"]["content"]:
                if item["type"] == content_type:
                    print(f"{item['type']}: {item['text']} for files: {item['files']}")
        else:
            print(f"No content found for type: {content_type}")

    def show_recent_content(self, count: Optional[int] = None) -> None:
        """Displays the most recent content entries, limited by count if specified.

        Args:
            count: The maximum number of content entries to display.
                   If None, all entries are displayed.
        """
        data = self.get_stored_data()
        if "history" in data and "content" in data["history"]:
            content_history = reversed(data["history"]["content"])
            if count is not None and count > 0:
                content_history = list(content_history)[:count]

            for item in content_history:
                print(f"{item['type']}: {item['text']} for files: {item['files']}")
        else:
            print("No content history found.")

    def show_recent_content_by_type(self, content_type: str, count: int) -> None:
        """Displays the most recent content entries of a specific type, limited by count.

        Args:
            content_type: The type of content to display.
            count: The maximum number of content entries to display.
        """
        data = self.get_stored_data()
        if "history" in data and "content" in data["history"]:
            content_history = [
                item
                for item in reversed(data["history"]["content"])
                if item["type"] == content_type
            ]
            if count > 0:
                content_history = content_history[:count]

            for item in content_history:
                print(f"{item['type']}: {item['text']} for files: {item['files']}")
        else:
            print(f"No recent content found for type: {content_type}")

    def read_files(self, files: List[str]) -> str:
        """Reads the content of multiple files, concatenating their content.

        Args:
            files: A list of file paths to read.

        Returns:
            A string containing the concatenated content of the files.
        """
        combined_content = ""
        for file_path in files:
            if self.is_binary_file(file_path):
                print(f"Skipping binary file: {file_path}")
                continue
            file_content = self.read_file_content(file_path)
            if file_content:
                combined_content += file_content
            else:
                print(f"No content read from {file_path}")
        return combined_content

    def read_file_content(self, file_path: str) -> Optional[str]:
        """Reads the content of a single file, handling various encodings.

        Args:
            file_path: The path to the file.

        Returns:
            The content of the file as a string, or None if the file could not be read.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read() + "\n"
        except UnicodeDecodeError as e:
            print(f"Unicode decode error in file {file_path}: {e}")
            detected_encoding = chardet.detect(open(file_path, "rb").read())["encoding"]
            if detected_encoding:
                try:
                    with open(file_path, "r", encoding=detected_encoding) as file:
                        return file.read() + "\n"
                except Exception as e:
                    print(
                        f"Error reading file {file_path} with detected encoding \
                            {detected_encoding}: {e}"
                    )
            else:
                print(f"Could not detect encoding for file {file_path}")
        except IOError as e:
            print(f"Error reading file {file_path}: {e}")
        return None

    @staticmethod
    def is_binary_file(file_path: str) -> bool:
        """Determines if the specified file is binary or text.

        Args:
            file_path: The path to the file to check.

        Returns:
            True if the file is binary, False otherwise.
        """
        textchars = bytearray(
            {7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7F}
        )
        try:
            with open(file_path, "rb") as file:
                if bool(file.read(1024).translate(None, textchars)):
                    return True
        except IOError as e:
            print(f"IOError when checking if file is binary: {file_path}: {e}")
        return False

    def export_command_output(
        self,
        input_data: Union[List[str], str],
        text: str,
        directory: str,
        type: str = ".txt",
        is_batch: bool = False,
        prefix_text: Optional[str] = None,
    ) -> str:
        """Saves generated command output to a file in the specified directory.

        Args:
            input_data: Either a list of files or text data
                        used for generating the output.
            text: The generated text to save.
            directory: The directory where the output file will be saved.
            type: The file extension for the output file. Defaults to ".txt".
            is_batch: Specifies if the operation involves multiple files
                      or batch processing.
            prefix_text: Optional text to prepend to the generated output.

        Returns:
            The path to the saved output file.
        """

        if isinstance(input_data, list):
            # Input is a list of files
            prefix_text_content = "Files provided: " + ", ".join(input_data)
            if len(input_data) == 1 and not is_batch:
                # For a single file, create a filename based on the original file name
                filename = (
                    input_data[0].replace("/", "_").replace(".", "_").lower() + type
                )
            else:
                # For multiple files or batch mode, use a timestamp
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"batch_output_{timestamp}{type}"
        else:
            # Input is other text data (e.g., code diffs)
            prefix_text_content = prefix_text if prefix_text else ""
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"content_{timestamp}{type}"

        # Prepend the additional text (if any) to the final output
        final_text = (
            prefix_text_content + "\n\n" if prefix_text_content else ""
        ) + text

        # Save the file
        filepath = os.path.join(directory, filename)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(filepath, "w") as file:
            file.write(final_text)

        return filepath
