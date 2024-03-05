from akita.cli.command_factory import CommandFactory
from akita.plugins.base_plugin import BasePlugin
from argparse import ArgumentParser, _SubParsersAction


class GitPlugin(BasePlugin):
    def __init__(self, command_factory: CommandFactory) -> None:
        super().__init__(command_factory)

    def load_subparsers(self, subparsers: _SubParsersAction) -> None:
        # Add a new 'git' command parser and its subcommands ('add', 'commit').
        git_parser: ArgumentParser = subparsers.add_parser("git", help="Git Commands")
        git_subparsers: _SubParsersAction = git_parser.add_subparsers(
            dest="git_command", help="Available git operations"
        )
        git_parser.set_defaults(func=lambda args: git_parser.print_help())

        # Add 'git add' subcommand
        git_add_parser: ArgumentParser = git_subparsers.add_parser(
            "add", help="Add files to git"
        )
        git_add_parser.add_argument("files", nargs="*", help="Files to git add")
        git_add_parser.set_defaults(
            func=lambda args: self.command_factory.get_command("git_add")().execute(
                args=args
            )
        )

        # Add 'git commit' subcommand
        git_commit_parser: ArgumentParser = git_subparsers.add_parser(
            "commit", help="Commit changes"
        )
        git_commit_parser.add_argument("-m", "--message", help="Commit message")
        git_commit_parser.set_defaults(
            func=lambda args: self.command_factory.get_command("git_commit")().execute(
                args=args
            )
        )
