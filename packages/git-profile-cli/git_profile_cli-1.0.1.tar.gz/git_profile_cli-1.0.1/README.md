# git-profile-cli

git-profile-cli is a command-line tool that simplifies the management of multiple Git profiles. It allows developers to effortlessly switch between different Git configurations, including user names, email addresses, and SSH keys. This tool is perfect for developers who work on various projects or contribute to multiple organizations.

## Features

- Manage multiple Git profiles with ease
- Switch between profiles quickly
- Automatically update Git global configuration
- Configure SSH keys for different profiles
- Interactive profile selection and management
- Extensible and modular codebase

## Installation

### From PyPI (Recommended)

```bash
pip install git-profile-cli
```

### From Source

1. Clone the repository:
   ```bash
   git clone https://github.com/tux86/git-profile-cli.git
   cd git-profile-cli
   ```

2. Install the package:
   ```bash
   pip install .
   ```

## Usage

After installation, you can use Git profile cli with the `git-profile` command:

### List all profiles

```bash
git-profile list
```

### Display the current profile

```bash
git-profile current
```

### Add a new profile

```bash
git-profile add
```

You'll be prompted to enter the profile details interactively.

### Modify an existing profile

```bash
git-profile modify <profile_name>
```

### Select a profile

```bash
git-profile [select] [profile_name]
```

You can use this command in several ways:
- `git-profile select work`: Directly selects the 'work' profile
- `git-profile select`: Prompts you to choose a profile interactively
- `git-profile`: Same as `git-profile select`, prompts you to choose a profile interactively

Examples:
```bash
git-profile select work  # Directly selects the 'work' profile
git-profile select  # Prompts you to choose a profile interactively
git-profile  # Also prompts you to choose a profile interactively
```

Note: Running `git-profile` without any command is equivalent to `git-profile select` and will prompt you to choose a profile interactively.

### Delete a profile

```bash
git-profile delete
```

You'll be prompted to select the profile to delete.

### Specify a custom configuration file

You can use a custom configuration file by using the `--config` or `-c` option:

```bash
git-profile -c /path/to/custom/config.yaml <command>
```

## Configuration

Git-Profile-Cli uses a YAML configuration file to store profile information. By default, it's located at `~/.git-profile/config.yaml`. Each profile in the configuration file has the following structure:

```yaml
profiles:
  - name: work
    user_name: John Doe
    user_email: john.doe@company.com
    ssh_key_path: ~/.ssh/id_rsa_work
  - name: personal
    user_name: John Doe
    user_email: john.doe@gmail.com
    ssh_key_path: ~/.ssh/id_rsa_personal
```

## Development

To set up the development environment:

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running Tests

To run tests, use:

```bash
python -m unittest discover tests
```

### Building the Package

To build the package, use:

```bash
python -m build
```

## Contributing

Contributions are welcome! Here are some ways you can contribute to this project:

1. Report bugs and suggest features by opening issues.
2. Submit pull requests with bug fixes or new features.
3. Improve documentation or add examples.
4. Share the project and help others.

## Authors

* **Walid Karray** - [tux86](https://github.com/tux86)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to all contributors who have helped to improve this project.
- Inspired by the need for easy management of multiple Git profiles.
- Hat tip to anyone whose code was used as inspiration.