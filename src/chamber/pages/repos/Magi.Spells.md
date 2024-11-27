# Magi.Spells

Welcome to **Magi.Spells**, a collection of optional spells for the **Magi.CLI** tool. These spells enhance your magical command-line experience by providing additional functionalities. The spells are stored in the **Magi.Chamber** server and can be easily pulled into your local environment.

## Table of Contents

- [Magi.Spells](#magispells)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Installation](#installation)
  - [Spell Dependency Management](#spell-dependency-management)
    - [Handling Missing Dependencies](#handling-missing-dependencies)
    - [Lazy Loading of Spells](#lazy-loading-of-spells)
  - [Available Spells](#available-spells)
    - [aether\_inquiry (ai)](#aether_inquiry-ai)
    - [astral\_realm (ar)](#astral_realm-ar)
    - [runecraft (rc)](#runecraft-rc)
    - [pagecraft (pgc)](#pagecraft-pgc)
    - [scribe (scb)](#scribe-scb)
    - [warp (wp)](#warp-wp)
    - [spellcraft (sc)](#spellcraft-sc)
  - [Usage Examples](#usage-examples)
    - [Installing a Spell](#installing-a-spell)
    - [Using a Spell](#using-a-spell)
    - [Uninstalling a Spell](#uninstalling-a-spell)
  - [Contributing](#contributing)
    - [How to Contribute](#how-to-contribute)
    - [Contribution Guidelines](#contribution-guidelines)
    - [Reporting Issues](#reporting-issues)
  - [License](#license)

## Introduction

**Magi.Spells** is a repository that serves as the source for additional spells used by **Magi.CLI**, a command-line tool that brings a touch of magic to your terminal. The spells in this repository are designed to extend the capabilities of **Magi.CLI**, allowing you to perform complex tasks with simple commands.

Each spell declares its own dependencies, ensuring modularity and scalability. This per-spell dependency management allows you to install only the packages required for the spells you use, keeping your environment clean and efficient.

## Installation

To add spells from **Magi.Spells** to your **Magi.CLI** tool, use the `ponder` command, which handles the installation of spells and their dependencies.

Ensure you have **Magi.CLI** installed:

```bash
pip install magi_cli_pypi
```

Install spells using the `ponder` command:

```bash
cast ponder <spell_name>
```

Replace `<spell_name>` with the name of the spell you wish to install. For example:

```bash
cast ponder runecraft
```

The `ponder` command will fetch the spell from the **Magi.Chamber**, install any required dependencies, and make the spell available for use.

## Spell Dependency Management

Each spell specifies its external dependencies using a special `__requires__` variable within the spell script. This variable is a list of packages that are not part of Python's standard library but are required for the spell to function.

For example:

```python
__requires__ = ['click', 'requests', 'openai']
```

When you install a spell using the `ponder` command:

1. The `ponder` command extracts the `__requires__` variable from the spell.
2. It prompts you for consent before installing the dependencies.
3. It installs the necessary packages, ensuring the spell functions correctly.

### Handling Missing Dependencies

If you attempt to use a spell whose dependencies are not installed, **Magi.CLI** will:

- Gracefully handle the missing dependencies.
- Provide a clear error message indicating which dependencies are missing.
- Suggest running `cast ponder <spell_name>` to install the missing dependencies.

### Lazy Loading of Spells

To prevent issues with missing dependencies at startup, **Magi.CLI** employs lazy loading for spells:

- Spells are only loaded when invoked.
- This approach allows the CLI tool to function even if some spells have unmet dependencies.
- It improves startup performance and reduces unnecessary resource usage.

## Available Spells

Below is a list of available spells along with their descriptions and dependencies.

### aether_inquiry (ai)

- **Description**: Call upon the arcane intellect of an artificial intelligence to answer your questions and generate spells or Python scripts.
- **Dependencies**: `click`, `openai`

### astral_realm (ar)

- **Description**: Clone a remote repository, start a local server, and populate a webpage with the repository's files.
- **Dependencies**: `click`, `flask`, `gitpython`

### runecraft (rc)

- **Description**: Generate a GUI for a Bash script in the form of an enchanted rune.
- **Dependencies**: `click`, `requests`, `Pillow`, `openai`, `PyQt5`

### pagecraft (pgc)

- **Description**: Craft a Markdown page from a URL through the use of aether inquiry (AI).
- **Dependencies**: `click`, `beautifulsoup4`, `openai`, `requests`

### scribe (scb)

- **Description**: Transcribe the contents of a file or directory into markdown.
- **Dependencies**: `click`

### warp (wp)

- **Description**: Warp to remote SSH sessions with ease.
- **Dependencies**: `click`, `paramiko`, `cryptography`

### spellcraft (sc)

- **Description**: Create a macro spell and store it in `.tome`.
- **Dependencies**: `click`

## Usage Examples

### Installing a Spell

To install the `runecraft` spell:

```bash
cast ponder runecraft
```

You'll be prompted to install the spell and its dependencies.

### Using a Spell

After installing, you can use the spell by casting it with its alias:

```bash
cast rc path/to/your/script.sh
```

### Uninstalling a Spell

If you wish to uninstall a spell:

```bash
cast ponder runecraft
```

If the spell is already installed, the `ponder` command will offer to uninstall it.

## Contributing

We welcome contributions to **Magi.Spells**! If you have an idea for a new spell or improvements to existing ones, please follow the guidelines below.

### How to Contribute

1. **Fork the Repository**: Create your own fork of the **Magi.Spells** repository.

2. **Create a New Spell**:

   - Add your spell script to the `spells` directory.
   - Ensure your spell includes the following:
     - An `__requires__` variable listing any external dependencies.
     - An `alias` variable for the spell's command alias.
     - A `main` function that invokes your spell.
   - Follow the existing spell format for consistency.

3. **Test Your Spell**:

   - Use the `ponder` command to install your spell and verify that dependencies are correctly managed.
   - Ensure your spell functions as intended.

4. **Update Documentation**:

   - Add your spell to the **Available Spells** section in the `README.md`.
   - Include a description and list of dependencies.

5. **Submit a Pull Request**:

   - Once your spell is ready, submit a pull request to the main repository.
   - Provide a detailed description of your spell and any relevant information.

### Contribution Guidelines

- **Code Style**:
  - Follow Python best practices and PEP 8 guidelines.
  - Keep your code clean and well-documented.
- **Dependencies**:
  - Only include necessary external dependencies.
  - Use standard library modules whenever possible.
- **Error Handling**:
  - Ensure your spell handles errors gracefully.
  - Provide meaningful error messages to the user.
- **Testing**:
  - Thoroughly test your spell in various scenarios.
  - Verify that dependencies are properly declared and installed.
- **Licensing**:
  - By contributing, you agree that your contributions will be licensed under the same license as this repository (MIT License).

### Reporting Issues

If you encounter any issues or have suggestions for improvements, please open an issue on the GitHub repository. Provide as much detail as possible to help us address the problem.

## License

**Magi.Spells** is released under the MIT License. By contributing to this repository, you agree to have your contributions licensed under the MIT License.