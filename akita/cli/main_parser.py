import os
from argparse import _SubParsersAction
from akita.cli.command_factory import CommandFactory


def setup_main_parser(command_factory: CommandFactory, subparsers: _SubParsersAction):
    # Add Command
    parser_add = subparsers.add_parser("add", help="Add files for processing")
    parser_add.add_argument("files", nargs="+", help="Files to add")
    parser_add.set_defaults(
        func=lambda args: command_factory.get_command("add").execute(args)
    )

    # Remove Command
    parser_rm = subparsers.add_parser("rm", help="Remove files from storage")
    parser_rm.add_argument("files", nargs="*", help="Files to remove")
    parser_rm.set_defaults(
        func=lambda args: command_factory.get_command("rm").execute(args)
    )

    # Show Command
    parser_show = subparsers.add_parser("show", help="Show stored files or contents")
    parser_show.add_argument(
        "--type",
        "-t",
        choices=[
            "generate_summary",
            "generate_commit_message",
            "generate_docstring",
            "generate_readme",
            "generate_folder_structure",
        ],
        help="Specific content type to show",
    )
    parser_show.add_argument("--all", "-a", action="store_true", help="Show all")
    parser_show.add_argument(
        "--recent", "-r", type=int, help="Show the most recent 'n' content entries"
    )
    parser_show.set_defaults(
        func=lambda args: command_factory.get_command("show").execute(args)
    )

    # Init Command
    parser_init = subparsers.add_parser("init", help="Initialize or reset Akita data")
    parser_init.set_defaults(
        func=lambda args: command_factory.get_command("init").execute(args)
    )

    # Review Command
    parser_review = subparsers.add_parser(
        "review", help="Generate code review for given file(s) or code diff"
    )
    parser_review.add_argument(
        "filename", type=str, nargs="*", help="Path to the file to review"
    )
    parser_review.add_argument(
        "-v",
        "--verbose",
        choices=["high", "moderate", "low"],
        default="moderate",
        help="Level of detail in output",
    )
    parser_review.add_argument(
        "-l",
        "--lang",
        default="en",
        choices=["en", "es", "de", "fr", "pt", "cn", "ru", "jp"],
        help="Language for the review",
    )
    parser_review.add_argument(
        "-s", "--use-git-staged", action="store_true", help="Use Git staged files"
    )
    parser_review.add_argument(
        "-sd", "--use-git-staged-diff", action="store_true", help="Use Git staged diff"
    )
    parser_review.add_argument(
        "-d", "--use-git-diff", action="store_true", help="Use Git staged diff"
    )
    parser_review.add_argument(
        "--export",
        nargs="?",
        choices=["txt", "html"],
        default=None,
        const="txt",
        help="Export the file",
    )
    parser_review.add_argument(
        "--preview", action="store_true", help="Display review generated"
    )
    parser_review.set_defaults(
        func=lambda args: command_factory.get_command("review").execute(args)
    )

    # Describe Command
    parser_describe = subparsers.add_parser(
        "describe", help="Generate description for a file"
    )
    parser_describe.add_argument(
        "filename", type=str, nargs="*", help="Path to the file to summarize"
    )
    parser_describe.add_argument(
        "-v",
        "--verbose",
        choices=["high", "moderate", "low"],
        default="moderate",
        help="Level of detail in output",
    )
    parser_describe.add_argument(
        "-l",
        "--lang",
        default="en",
        choices=["en", "es", "de", "fr", "pt", "cn", "ru", "jp"],
        help="Language for the review",
    )
    parser_describe.add_argument(
        "-s", "--use-git-staged", action="store_true", help="Use Git staged files"
    )
    parser_describe.add_argument(
        "-sd", "--use-git-staged-diff", action="store_true", help="Use Git staged diff"
    )
    parser_describe.add_argument(
        "-d", "--use-git-diff", action="store_true", help="Use Git staged diff"
    )
    parser_describe.set_defaults(
        func=lambda args: command_factory.get_command("describe").execute(args)
    )

    # Readme Command
    parser_readme = subparsers.add_parser(
        "readme", help="Generate README.md for given file(s) or code diff"
    )
    parser_readme.add_argument(
        "filename", type=str, nargs="*", help="Path to the file to summarize"
    )
    parser_readme.add_argument(
        "-v",
        "--verbose",
        choices=["high", "moderate", "low"],
        default="moderate",
        help="Level of detail in output",
    )
    parser_readme.add_argument(
        "-l",
        "--lang",
        default="en",
        choices=["en", "es", "de", "fr", "pt", "cn", "ru", "jp"],
        help="Language for the review",
    )
    parser_readme.add_argument(
        "-s", "--use-git-staged", action="store_true", help="Use Git staged files"
    )
    parser_readme.add_argument(
        "-sd", "--use-git-staged-diff", action="store_true", help="Use Git staged diff"
    )
    parser_readme.add_argument(
        "-d", "--use-git-diff", action="store_true", help="Use Git staged diff"
    )
    parser_readme.set_defaults(
        func=lambda args: command_factory.get_command("readme").execute(args)
    )

    # Assistant Command
    parser_assistant = subparsers.add_parser("assistant", help="Run Akita Assistant")
    parser_assistant.add_argument(
        "repo_path",
        nargs="?",
        default=os.getcwd(),
        help="Path to the repository/files to add to the context\
        (defaults to current directory)",
    )
    parser_assistant.add_argument(
        "-t", "--terminal", action="store_true", help="Run assistant in the terminal"
    )
    parser_assistant.set_defaults(
        func=lambda args: command_factory.get_command("assistant").execute(args)
    )
