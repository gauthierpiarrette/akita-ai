from akita.cli.commands.base_command import BaseCommand
from akita.assistant.run import run_chainlit_app, run_terminal_app


class AssistantCommand(BaseCommand):
    def execute(self, args):
        if args.terminal:
            run_terminal_app(args.repo_path)
        else:
            run_chainlit_app(args.repo_path)
