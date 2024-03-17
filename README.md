<p align="center"><a href="https://github.com/gauthierpiarrette/akita-ai"><img src="https://github.com/gauthierpiarrette/akita-ai/assets/28540426/6029074f-e8f8-423d-8415-a5bd3c255e2c" alt="Akita AI Logo" height="60"/></a></p>

<h1 align="center">Akita AI</h1>
<p align="center">Your command-line, context-aware chatbot for instant codebase insights.</p>
<p align="center">
  <a href="https://pypi.org/project/akita-ai/"><img src="https://img.shields.io/pypi/v/akita-ai.svg" alt="PyPI Version"></a>
  <a href="https://github.com/gauthierpiarrette/akita-ai/blob/main/LICENSE"><img src="https://img.shields.io/github/license/gauthierpiarrette/akita-ai" alt="License"></a>
  <a href="https://pypi.org/project/akita-ai/"><img src="https://img.shields.io/pypi/pyversions/akita-ai.svg" alt="Python Version"></a>
  <a href="https://github.com/gauthierpiarrette/akita-ai/actions?query=workflow:%22CI%22"><img src="https://github.com/gauthierpiarrette/akita-ai/workflows/CI/badge.svg" alt="CI"></a>
</p>

<p align="center"><a href="https://github.com/gauthierpiarrette/akita-ai"><img src="https://github.com/gauthierpiarrette/akita-ai/assets/28540426/37d52939-c2bd-4041-b19c-ac1df7eba835" width="70%"/></a></p><br/>

## 🌟 Key Features

- **✅ Personal Code Assistant**: Engage with Akita directly from your terminal for real-time codebase insights.
- **✅ Automated Documentation**: Instantly generate comprehensive documentation for your entire project.
- **✅ Tailored Code Reviews**: Receive AI-powered suggestions to improve your code quality.
- **✅ Quick Code Explainer**: Understand any piece of code with a simple command.
- **✅ Flexible Plugin System**: Customize Akita AI to fit perfectly into your development workflow.

## 🚀 Getting Started

### 1. Installation

Ensure you have Python 3.9+. Open a terminal and run:

```bash
$ pip install akita-ai
```

Set up your OpenAI API key (find it on your [OpenAI](https://openai.com) account):

```bash
$ export OPENAI_API_KEY=<your-api-key>
```

### 2. Engage with Your Personal Code Assistant

Start interacting with Akita Assistant for insights:

```bash
$ cd path/to/your/project
$ akita assistant
```

Ask Akita anything about your codebase for instant assistance.

## Integrations

Connect Akita AI with your preferred providers for enhanced coding assistance.

![akita_integration_long](https://github.com/gauthierpiarrette/akita-ai/assets/28540426/19e698f1-cbf0-4745-b833-731d61ee8953)
*More integrations coming soon.*

## 🔍 Explore More Features

Dive into the additional features, designed to streamline your development workflow.

### File Selector
**Effortlessly select files** for Akita AI's analysis to focus enhancements where you need them.

- **Initiate with Akita**: Prepare your project.
  ```bash
  $ akita init
  ```
- **Choose Files for Analysis**: Highlight specific files.
  ```bash
  $ akita add <file_path>
  ```
- **Exclude Files**: Easily remove files from the queue.
  ```bash
  $ akita rm <file_path>
  ```

### Documentation in a Snap
**Automatically generate comprehensive documentation** for your selected files, enhancing readability and maintainability.

```bash
$ akita describe <file_path>
```

### Targeted Code Reviews
Receive **targeted, AI-driven feedback** on your code to identify improvements quickly.

```bash
$ akita review <file_path>
```

### Quick README Creation
Generate **engaging READMEs** effortlessly, making your projects more accessible and understandable.

```bash
$ akita readme <file_path>
```

See our detailed [commands documentation](https://github.com/gauthierpiarrette/akita-ai/blob/main/docs/Commands_Documentation.md) for more details.

## 💡 Contributing

Join our community of contributors! Whether you're fixing bugs, adding features, or improving documentation, your contributions make Akita AI better for everyone. See our [Contributors Guide](CONTRIBUTING.md) for how to get started.

## 📢 Feedback and Support

Your feedback shapes the future of Akita AI. Encounter a bug or have a feature suggestion? Open an issue on our [GitHub issues page](https://github.com/gauthierpiarrette/akita-ai/issues). For more support, contact us through our [homepage](https://akita.ai).

## 📜 License

Akita AI is open-source software licensed under the Apache 2.0 License. Feel free to use, modify, and distribute it as per the license.
