from akita.cli.commands.base_command import BaseCommand


class ShowCommand(BaseCommand):
    def __init__(self, file_handler):
        self.file_handler = file_handler

    def execute(self, args):
        if args.all:
            self.file_handler.show_all()
        elif args.type and args.recent:
            self.file_handler.show_recent_content_by_type(args.type, args.recent)
        elif args.type:
            self.file_handler.show_content_by_type(args.type)
        elif args.recent is not None:
            self.file_handler.show_recent_content(args.recent)
        else:
            self.file_handler.show_files()
