# PyDepDetective

[![PyPI version](https://badge.fury.io/py/pydepdetective.svg)](https://badge.fury.io/py/pydepdetective)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Ever hated starting a new python project (or an existing one) and having to install dependencies one by one?

PyDepDetective is a Python tool that automatically detects and installs dependencies for a given Python file. It simplifies the process of setting up project dependencies by analyzing import statements, comments, and even references to `requirements.txt` files.

## Features

- Analyzes Python files to detect import statements
- Identifies third-party imports by filtering out standard library modules
- Detects `pip install` comments in the code
- Recognizes references to `requirements.txt` files
- Checks for already installed packages to avoid unnecessary reinstallation
- Handles common package name mismatches (e.g., `PIL` for `pillow`)
- Provides an interactive prompt to confirm installations
- Supports installation from `requirements.txt` files

## Installation

You can install PyDepDetective using pip:

```
pip install pydepdetective
```

## Usage

After installation, you can run PyDepDetective from the command line:

```
pydepdetective path/to/your/file.py
```

The tool will analyze the file and prompt you to install any detected dependencies.

## How It Works

1. PyDepDetective parses the given Python file and extracts all import statements.
2. It filters out standard library imports to identify third-party packages.
3. The file content is also analyzed for `# pip install` comments and references to `requirements.txt`.
4. The tool checks which packages are already installed in your environment.
5. You are prompted to confirm the installation of detected dependencies.
6. If confirmed, PyDepDetective uses pip to install the required packages.

## Limitations (for now)

- May not detect very complex dynamic imports or imports within deeply nested code.
- The package name mapping is limited to common cases and may need expansion for less common packages.
- Does not handle version specifications (e.g., `package>=1.0.0`).

## Contributing

Contributions to improve PyDepDetective are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Contact

If you have any questions or feedback, please open an issue on the GitHub repository.

Happy coding!