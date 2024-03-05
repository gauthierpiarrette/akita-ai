from akita.cli.commands.base_command import BaseCommand


class RemoveCommand(BaseCommand):
    def __init__(self, file_handler):
        self.file_handler = file_handler

    def execute(self, args):
        self.file_handler.remove_files(args.files if args.files else None)
