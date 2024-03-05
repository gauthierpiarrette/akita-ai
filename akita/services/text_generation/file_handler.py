import chardet
from typing import List, Optional


class FileHandler:
    def __init__(self) -> None:
        pass

    def read_files(self, files: List[str]) -> str:
        """Reads multiple files, concatenating their content if they are text files.

        Args:
            files: A list of file paths to be read.

        Returns:
            A single string containing the concatenated content of all text files.
        """
        combined_content: str = ""
        for file_path in files:
            if self.is_binary_file(file_path):
                print(f"Skipping binary file: {file_path}")
                continue
            file_content: Optional[str] = self.read_file_content(file_path)
            if file_content:
                combined_content += file_content
            else:
                print(f"No content read from {file_path}")
        return combined_content

    def read_file_content(self, file_path: str) -> Optional[str]:
        """Attempts to read the content of a file, handling different encodings.

        Args:
            file_path: The path to the file to be read.

        Returns:
            The content of the file as a string, or an empty string if an error occurs.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read() + "\n"
        except UnicodeDecodeError as e:
            print(f"Unicode decode error in file {file_path}: {e}")
            detected_encoding: Optional[str] = chardet.detect(
                open(file_path, "rb").read()
            )["encoding"]
            if detected_encoding:
                try:
                    with open(file_path, "r", encoding=detected_encoding) as file:
                        return file.read() + "\n"
                except Exception as e:
                    print(
                        f"Error reading file {file_path}\
                        with detected encoding {detected_encoding}: {e}"
                    )
            else:
                print(f"Could not detect encoding for file {file_path}")
        except IOError as e:
            print(f"Error reading file {file_path}: {e}")
        return ""

    @staticmethod
    def is_binary_file(file_path: str) -> bool:
        """Determines if a file is binary or text.

        Args:
            file_path: The path to the file to be checked.

        Returns:
            True if the file is binary, False otherwise.
        """
        textchars = bytearray(
            {7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7F}
        )
        try:
            with open(file_path, "rb") as file:
                return bool(file.read(1024).translate(None, textchars))
        except IOError as e:
            print(f"IOError when checking if file is binary: {file_path}: {e}")
            return False
