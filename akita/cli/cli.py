from akita.cli.commands.assistant_command import AssistantCommand
from akita.cli.commands.readme_command import ReadmeCommand
from akita.cli.commands.describe_command import DescribeCommand
from akita.cli.commands.review_command import ReviewCommand
from akita.cli.commands.init_command import InitCommand
from akita.cli.commands.show_command import ShowCommand
from akita.cli.commands.remove_command import RemoveCommand
from akita.cli.commands.add_command import AddCommand
from akita.services.text_generation.text_generator import TextGenerator
from akita.utils.file_handler import FileHandler
from akita.cli.plugin_manager import PluginManager
from akita.cli.command_factory import CommandFactory
from akita.cli.main_parser import setup_main_parser
import sys
import os
import argparse


current_dir = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, project_dir)


def main():
    parser = argparse.ArgumentParser(description="Akita - AI-enhanced development tool")
    subparsers = parser.add_subparsers(dest="command")

    # Initialize dependencies for main commands
    file_handler = FileHandler()
    text_generator = TextGenerator()

    # Initialize the command factory
    command_factory = CommandFactory()

    # Register non-plugin commands with the command factory
    command_factory.register_command("add", AddCommand(file_handler))
    command_factory.register_command("rm", RemoveCommand(file_handler))
    command_factory.register_command("show", ShowCommand(file_handler))
    command_factory.register_command("init", InitCommand(file_handler))
    command_factory.register_command(
        "review", ReviewCommand(file_handler, text_generator)
    )
    command_factory.register_command(
        "describe", DescribeCommand(file_handler, text_generator)
    )
    command_factory.register_command(
        "readme", ReadmeCommand(file_handler, text_generator)
    )
    command_factory.register_command("assistant", AssistantCommand())

    setup_main_parser(command_factory, subparsers)

    plugin_manager = PluginManager(command_factory, subparsers)
    plugin_manager.load_plugins()

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()
