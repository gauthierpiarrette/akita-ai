from akita.plugins.base_plugin import BasePlugin
from akita.cli.command_factory import CommandFactory
from argparse import _SubParsersAction


class TemplatePlugin(BasePlugin):
    def __init__(self, command_factory: CommandFactory):
        super().__init__(command_factory)

    def load_subparsers(self, subparsers: _SubParsersAction):
        # Define your subparsers here
        pass
