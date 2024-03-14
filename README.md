<p align="center"><a href="https://github.com/gauthierpiarrette/akita-ai"><img src="https://github.com/gauthierpiarrette/akita-ai/assets/28540426/6029074f-e8f8-423d-8415-a5bd3c255e2c" alt="Akita AI Logo" height="60"/></a></p>

<h1 align="center">Akita AI</h1>
<p align="center">Your command-line, context-aware chatbot for instant codebase insights.</p>
<p align="center">
  <a href="https://pypi.org/project/akita-ai/"><img src="https://img.shields.io/pypi/v/akita-ai.svg" alt="PyPI Version"></a>
  <a href="https://github.com/gauthierpiarrette/akita-ai/blob/main/LICENSE"><img src="https://img.shields.io/github/license/gauthierpiarrette/akita-ai" alt="License"></a>
  <a href="https://pypi.org/project/akita-ai/"><img src="https://img.shields.io/pypi/pyversions/akita-ai.svg" alt="Python Version"></a>
  <a href="https://github.com/gauthierpiarrette/akita-ai/actions?query=workflow:%22CI%22"><img src="https://github.com/gauthierpiarrette/akita-ai/workflows/CI/badge.svg" alt="CI"></a>
</p>

<p align="center"><a href="https://github.com/gauthierpiarrette/akita-ai"><img src="https://github.com/gauthierpiarrette/akita-ai/assets/28540426/37d52939-c2bd-4041-b19c-ac1df7eba835" width="80%"/></a></p><br/>

## Installation

```bash
pip install akita-ai
export OPENAI_API_KEY=<your-openai-api-key>
```

*Note: Requires SQLite > 3.35*

## 🚀 Quick Example: 

### Using Akita Assistant for real-time assistance

```bash
akita assistant path/to/your/repo
```

Run this command to run Akita Assistant, a GPT-like chatbot, for real-time AI suggestions on improving your code. It's accessible directly via the terminal or through a dedicated UI.

### Generating a Code Review

```bash
akita review your_file.py
akita review your_file.js your_file.py
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
