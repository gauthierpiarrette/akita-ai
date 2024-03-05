import os

# Configuration settings for the application

# Global pattern for file matching
GLOB_PATTERN = "**/*"

# List of file types accepted
SUFFIXES = [
    ".py",
    ".cpp",
    ".go",
    ".java",
    ".kt",
    ".js",
    ".ts",
    ".php",
    ".rb",
    ".rs",
    ".scala",
    ".swift",
    ".sol",
    ".cs",
    ".cob",
    ".proto",
    ".rst",
    ".md",
    ".tex",
    ".html",
]

# Patterns to exclude from processing
EXCLUDE_PATTERNS = [
    "**/non-utf8-encoding.py",
    "**/node_modules/**",
    "**/vendor/**",
    "**/.git/**",
    "**/build/**",
    "**/__pycache__/**",
    "**/*.min.js",
    "**/*.min.css",
    "**/dist/**",
    "**/bin/**",
    "**/obj/**",
    "**/out/**",
    "**/*.class",
    "**/generated/**",
    "**/*.log",
    "**/*.dll",
    "**/*.exe",
    "**/*.so",
    "**/*.dylib",
    "**/.*",
    "**/venv/**",
    "**/env/**",
]

# Threshold for parser selection
PARSER_THRESHOLD = 500

# Text splitting settings
CHUNK_SIZE = 2000
CHUNK_OVERLAP = 200

# Model and search configuration
MODEL_NAME = "gpt-4-0125-preview"
SEARCH_TYPE = "mmr"
SEARCH_K = 15

# Optional database persistence directory
DB_PERSIST_DIRECTORY = ".akita/db"

ENV = os.environ.copy()

HELP_MESSAGE = (
    "Akita Commands:\n"
    "- '<query>': Ask about your code or Akita usage.\n"
    "- 'exit' or 'quit': Close Akita Playground.\n"
)
