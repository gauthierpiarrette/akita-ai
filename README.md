# Welcome to Akita AI: Your AI-Enhanced Development Tool 🤖

[![CI](https://github.com/gauthierpiarrette/akita-ai/workflows/CI/badge.svg)](https://github.com/gauthierpiarrette/akita-ai/actions?query=workflow:"CI")

Akita is a command-line interface designed to streamline your development workflow leveraging the power of AI. From generating docs to offering in-depth code reviews and real time assistance, Akita helps making development faster, smarter, and more efficient.

[![Intro Video](https://img.youtube.com/vi/Cd49D3M5qlM/maxresdefault.jpg)](https://www.youtube.com/watch?v=Cd49D3M5qlM)

## Installation

```bash
pip install akita-ai
```

Set your OPENAI_API_KEY environment variable:
```bash
export OPENAI_API_KEY=<your-openai-api-key>
```

*Note: Requires SQLite > 3.35*

## 🚀 Quick Example: 

### Using Akita Assistant for real-time assistance

```bash
akita assistant path/to/your/repo
```

Run this command to run Akita Assistant, a GPT-like chatbot, for real-time AI suggestions on improving your code. It's accessible directly via the terminal or through a dedicated UI, offering tailored advice to streamline your development workflow.

### Generating a Code Review

```bash
akita review your_file.py
```

This command reviews `your_file.py`, offering AI-powered insights and improvement suggestions.

## Core Features

- **🤖 Interactive AI Chat for Code**: Directly converse with the Akita Assistant, a ChatGPT-like tool tailored for your local codebase. It offers instant, interactive guidance and documentation, making it easier to navigate and understand your projects. Available through both terminal and a specialized UI.
- **📄 Effortless Documentation Generation**: Automatically create comprehensive READMEs and documentation to enhance code readability and maintainability.
- **🔍 In-depth Code Reviews**: Receive detailed, constructive reviews with specific suggestions to elevate the quality of your code.
- **📖 File Explainer**: Instantly uncover the functionality and purpose behind any piece of code, eliminating confusion and streamlining project navigation.
- **⚙️ Customizable Plugins**: Akita AI features a flexible plugin system, allowing you to tailor its capabilities to fit your unique workflow. Enhance functionality and integrate seamlessly with tools you already use.

## Extensible Plugin System 

- **📝 `Git` Plugin**: Simplify your Git workflow with automated commit message generation. Use this plugin and let Akita AI craft concise, meaningful commit messages based on your code changes, streamlining your version control process.

- **🛠️ Your Plugin Here**

## Command Overview

Akita AI offers a comprehensive set of commands tailored for various development needs:

- `add`: Add files for AI processing and analysis.
- `rm`: Remove files from Akita's scope.
- `show`: Display stored files or AI-generated content.
- `init`: Prepare your workspace for Akita AI.
- `review`, `describe`, `readme`: Generate reviews, descriptions, and READMEs for your code.
- `assistant`: Invoke the Akita Assistant for interactive AI help.

For detailed usage and options, refer to the [Akita CLI Commands Overview](docs/Commands_Documentation.md).

## Contributing

Contributions are welcome! Whether it's adding new features, fixing bugs, or improving documentation, your input helps make Akita AI better for everyone.

[Contributors Guide](docs/contributors/README.md)

## Feedback and Support

Encountered a bug? Have suggestions? Let us know through our [GitHub issues page](https://github.com/gauthierpiarrette/akita-ai/issues) or contact us directly via our [homepage](https://akita.ai).

## License

Akita AI is open-source, licensed under the Apache 2.0 license.
