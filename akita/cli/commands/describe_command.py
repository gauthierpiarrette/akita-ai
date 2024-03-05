from akita.cli.commands.base_command import BaseCommand
from akita.plugins.git.utils.utils import get_staged_files, get_staged_diff, get_diff
from akita.utils.console import print_markdown, console


class DescribeCommand(BaseCommand):
    def __init__(self, file_handler, text_generator):
        self.file_handler = file_handler
        self.text_generator = text_generator

    def execute(self, args):
        # Determine the source of input data
        if args.use_git_staged:
            input_data = get_staged_files()
            input_type = "files"
            input_details = None
        elif args.use_git_staged_diff:
            input_data = get_staged_diff()
            input_type = "content"
            input_details = "Git Staged Code Diff"
        elif args.use_git_diff:
            input_data = get_diff()
            input_type = "content"
            input_details = "Git Code Diff"
        elif args.filename:
            input_data = args.filename
            input_type = "files"
            input_details = None
        else:
            input_data = self.file_handler.get_stored_files()
            input_type = "files"
            input_details = None

        if not input_data:
            console.print("[error]No files or data provided.[/error]")
            return

        function = "generate_description"
        prefix_text = input_details
        language = getattr(args, "lang", None)
        verbosity = getattr(args, "verbose", None)

        if input_type == "content" and "diff" in input_details.lower():
            text = self.text_generator.generate_description_code_diff(
                input_data=input_data, verbosity=verbosity, language=language
            )
        else:
            text = self.text_generator.generate_description_files(
                input_data=input_data, verbosity=verbosity, language=language
            )

        self.file_handler.add_content(function, text, input_data)

        content = (
            f"Files provided: {str(input_data)}\n\n" + text
            if input_type == "files"
            else prefix_text + "\n" + text
        )
        print_markdown(content)
