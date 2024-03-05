from akita.cli.commands.base_command import BaseCommand
from akita.plugins.git.utils.utils import get_staged_files, get_staged_diff, get_diff
from akita.utils.console import print_markdown, console
from akita.cli.config import Config


class ReviewCommand(BaseCommand):
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
            input_details = "Git staged code diff"
        elif args.use_git_diff:
            input_data = get_diff()
            input_type = "content"
            input_details = "Git code diff"
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

        # Generate review text
        function = "generate_review"
        language = getattr(args, "lang", None)
        verbosity = getattr(args, "verbose", None)
        text = self.text_generator.generate_review(
            input_data=input_data, verbosity=verbosity, language=language
        )

        self.file_handler.add_content(function, text, input_data)

        # Prepare for exporting the output
        file_extension = ".md"
        prefix_text = input_details
        is_batch = isinstance(input_data, list) and len(input_data) > 1
        file_path = self.file_handler.export_command_output(
            input_data,
            text,
            Config.AKITA_REVIEWS_DIR,
            type=file_extension,
            is_batch=is_batch,
            prefix_text=prefix_text,
        )

        console.print(f"Saved to: [path]{file_path}[/path]")

        review_content = (
            f"Files provided: {str(input_data)}\n\n" + text
            if input_type == "files"
            else prefix_text + "\n" + text
        )
        print_markdown(review_content)
