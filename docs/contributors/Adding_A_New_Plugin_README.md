# Adding a New Plugin to Akita

Welcome to Akita, an AI-enhanced development tool designed to streamline the software development process. This guide will walk you through the process of adding a new plugin to Akita.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Creating Your Plugin](#creating-your-plugin)
- [Full Example Plugin](#full-example-plugin)
- [Testing Your Plugin](#testing-your-plugin)
- [Submitting Your Plugin](#submitting-your-plugin)
- [Community and Contributions](#community-and-contributions)
- [License](#license)

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.9 or later
- Poetry

## Setup Instructions

Please see our [Contributors Guide](README.md) for setup instructions.

## Creating Your Plugin

1. **Plugin Structure:**
   - Navigate to the `akita/plugins` directory.
   - Create a new directory for your plugin, e.g., `my_plugin`.
   - Inside your plugin directory, create two files: `my_plugin_plugin.py` and `__init__.py`.

2. **Implementing the Plugin:**
   - Open `my_plugin_plugin.py` and import the necessary modules:
     ```python
     from akita.plugins.base_plugin import BasePlugin
     ```
   - Define your plugin class that inherits from `BasePlugin` and implement the required methods. Refer to the [Example Plugin](#example-plugin-helloakita) section below.

3. **Registering the Plugin:**
   - Ensure your plugin is discoverable by adding it to the `__init__.py` file in your plugin directory. The PluginManager automatically looks for plugins within the plugins directory and attempts to load each one by following a naming convention.

Note that you can find a template for your plugin at akita/plugins/template.

## Full Example Plugin:

Below is a simple example of a plugin that adds a "custom" command to Akita:

To add custom commands to your plugin for the Akita project, you should follow a structured approach that involves creating command classes and registering them with the command factory. Here's a step-by-step guide on how to do it, along with recommendations for where these commands should be located within your plugin's directory structure:

1. **Create Command Classes:**
   - Each command should be encapsulated in its own class, inheriting from `BaseCommand`.
   - Implement the `execute` method where you define the behavior of your command.

2. **Directory Structure:**
   - Your plugin should reside within the `plugins` directory of the Akita project.
   - Within your plugin's directory, it's a good practice to organize your commands in a subdirectory, for example, `commands`.
   - This results in a structure like: `akita/plugins/<your_plugin_name>/commands/`.

3. **Example Command Class:**
   ```python
   # akita/plugins/<your_plugin_name>/commands/custom_command.py

   from akita.cli.commands.base_command import BaseCommand

   class CustomCommand(BaseCommand):
       def execute(self, args):
           # Implementation of your command's functionality
           print("Executing custom command with args:", args)
   ```

4. **Registering Commands in Your Plugin:**
   - Your plugin class should inherit from `BasePlugin`.
   - Override the `load_subparsers` method to add your command's parser and subparsers.

5. **Example Plugin Class:**
   ```python
   # akita/plugins/<your_plugin_name>/<your_plugin_name>_plugin.py

   from akita.plugins.base_plugin import BasePlugin
   from .commands.custom_command import CustomCommand

   class YourPluginNamePlugin(BasePlugin):
       def __init__(self, command_factory):
           super().__init__(command_factory)
       
       def load_subparsers(self, subparsers):
           # Define subparsers for your command here
           custom_command_parser = subparsers.add_parser("custom", help="Custom command help")
           custom_command_parser.set_defaults(
               func=lambda args: self.command_factory.get_command("custom_command")().execute(args)
           )
   ```

6. **Loading Your Plugin:**
   - Make sure your plugin is correctly discovered and loaded by the `PluginManager`. The provided code automatically looks for plugins within the `plugins` directory and attempts to load each one by following a naming convention.

Following these steps, you can add custom commands to your plugin, and they will be integrated into the Akita project's command-line interface. Ensure that your plugin and commands are named and structured in a way that makes them easily identifiable and maintainable.

## Testing Your Plugin

After developing your plugin for Akita AI, follow these steps to test its functionality within your development environment:

1. **Activate Your Virtual Environment:**

   If you're using Poetry, activate the virtual environment created for Akita AI with:
   ```bash
   poetry shell
   ```

   This ensures that you are using the correct Python and dependencies specific to Akita AI.

2. **Run Akita Using Poetry:**

   With Poetry, you can directly run Akita commands without needing to invoke the Python module. To start, simply use:
   ```bash
   poetry run akita
   ```
   Now, test your new plugin command:
   ```bash
   poetry run akita your-plugin-name your-new-command
   ```

   Replace `your-new-command` with the actual command name you've added. For example, if you've created a plugin that is invoked with `your-plugin command1`, you would use:
   ```bash
   poetry run akita your-plugin command1
   ```

This method ensures that you're running Akita AI within the context of your virtual environment, using the dependencies and Python version specified by Poetry, providing a consistent development and testing experience.

## Submitting Your Plugin

Once you're satisfied with your plugin, submit it to the Akita project by creating a pull request from your forked repository. Please include a detailed description of your plugin's functionality and any setup instructions if necessary.

## Community and Contributions

We welcome contributions from the community! Whether it's adding new features, fixing bugs, or improving documentation, your contributions are valuable to us. Please read our [CONTRIBUTING](CONTRIBUTING.md) guide for more information on how to get involved.

## License

Ensure your plugin adheres to the project's [LICENSE](LICENSE).