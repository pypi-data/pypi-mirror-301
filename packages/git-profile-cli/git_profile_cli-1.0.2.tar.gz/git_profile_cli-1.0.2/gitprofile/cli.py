#!/usr/bin/env python3

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

import inquirer
import yaml

DEFAULT_CONFIG_DIR = Path.home() / ".git-profile"
DEFAULT_CONFIG_FILE = DEFAULT_CONFIG_DIR / "config.yaml"
SSH_CONFIG_FILE = Path.home() / ".ssh" / "config"


def load_config(config_path):
    if not config_path.exists():
        print(f"⚠️ Configuration not found at {config_path}.")
        config = {'profiles': []}
        print("🛠️ Initializing a new configuration file with no profiles.")
        save_config(config, config_path)
        return config

    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f) or {}
        if 'profiles' not in config or not isinstance(config['profiles'], list):
            config['profiles'] = []
    except yaml.YAMLError as e:
        print(f"❌ Error parsing YAML configuration: {e}")
        sys.exit(1)
    return config


def save_config(config, config_path):
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False)
    print(f"💾 Configuration saved to {config_path}")


def backup_ssh_config():
    if SSH_CONFIG_FILE.exists():
        backup_path = SSH_CONFIG_FILE.with_suffix('.backup')
        try:
            shutil.copyfile(SSH_CONFIG_FILE, backup_path)
            print(f"📦 Backup of existing SSH config created at {backup_path}")
        except IOError as e:
            print(f"❌ Failed to create a backup of the existing SSH config: {e}")
            sys.exit(1)


def save_ssh_config(content):
    backup_ssh_config()
    with open(SSH_CONFIG_FILE, "w") as f:
        f.write(content)
    print(f"🔐 SSH config updated at {SSH_CONFIG_FILE}")


def list_profiles(config):
    profiles = config.get("profiles", [])
    if not profiles:
        print("🚫 No profiles configured.")
        return
    print("👥 Available Git Profiles:")
    for prof in profiles:
        print(f" - {prof['name']}")


def current_profile(config):
    try:
        current_name = subprocess.check_output(
            ["git", "config", "--global", "user.name"], text=True).strip()
        current_email = subprocess.check_output(
            ["git", "config", "--global", "user.email"], text=True).strip()
    except subprocess.CalledProcessError:
        print("❌ Error: No Git global user configuration found.")
        sys.exit(1)

    for profile in config.get("profiles", []):
        if profile["user_name"] == current_name and profile["user_email"] == current_email:
            print("👤 Current Git Profile:")
            print(f" - Name: {profile['name']}")
            print(f" - user.name: {current_name}")
            print(f" - user.email: {current_email}")
            return

    print("🚫 No matching profile found in configuration for the current Git settings:")
    print(f" - user.name: {current_name}")
    print(f" - user.email: {current_email}")


def add_profile_interactive():
    print("✍️ Please enter the details for the new Git profile:")
    name = input_non_empty("Unique profile name: ")
    user_name = input_non_empty("Git user.name: ")
    user_email = input_non_empty("Git user.email: ")
    ssh_key_path = input_valid_ssh_key("Path to SSH key (e.g., ~/.ssh/id_rsa_personal): ")

    return {
        "name": name,
        "user_name": user_name,
        "user_email": user_email,
        "ssh_key_path": ssh_key_path
    }


def input_non_empty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("🚫 Input cannot be empty. Please try again.")


def input_valid_ssh_key(prompt):
    while True:
        ssh_key_path = input(prompt).strip()
        expanded_ssh_key_path = os.path.expanduser(ssh_key_path)
        if os.path.exists(expanded_ssh_key_path):
            return ssh_key_path
        print(f"❌ SSH key not found at {expanded_ssh_key_path}. Please enter a valid path.")


def add_profile(config, config_path, args):
    if all([args.name, args.user_name, args.user_email, args.ssh_key_path]):
        new_profile = {
            "name": args.name,
            "user_name": args.user_name,
            "user_email": args.user_email,
            "ssh_key_path": args.ssh_key_path
        }
    else:
        new_profile = add_profile_interactive()

    profiles = config.get("profiles", [])
    if any(prof['name'] == new_profile['name'] for prof in profiles):
        print(f"🚫 Profile with name '{new_profile['name']}' already exists.")
        sys.exit(1)

    expanded_ssh_key_path = os.path.expanduser(new_profile["ssh_key_path"])
    if not os.path.exists(expanded_ssh_key_path):
        print(f"❌ SSH key not found at {expanded_ssh_key_path}. Please ensure the SSH key exists.")
        sys.exit(1)

    profiles.append(new_profile)
    config["profiles"] = profiles
    save_config(config, config_path)
    print(f"✅ Added new profile '{new_profile['name']}' to configuration.")


def modify_profile(config, config_path, args):
    profiles = config.get("profiles", [])
    profile = next((prof for prof in profiles if prof['name'] == args.profile), None)
    if not profile:
        print(f"🚫 Profile '{args.profile}' not found in configuration.")
        sys.exit(1)

    new_user_name = args.user_name or input(f"Enter new user.name (current: {profile['user_name']}): ").strip() or \
                    profile['user_name']
    new_user_email = args.user_email or input(f"Enter new user.email (current: {profile['user_email']}): ").strip() or \
                     profile['user_email']
    new_ssh_key_path = args.ssh_key_path or input(
        f"Enter new SSH key path (current: {profile['ssh_key_path']}): ").strip() or profile['ssh_key_path']

    if not os.path.exists(os.path.expanduser(new_ssh_key_path)):
        print(f"❌ SSH key not found at {new_ssh_key_path}. Please ensure the SSH key exists.")
        sys.exit(1)

    profile.update({
        "user_name": new_user_name,
        "user_email": new_user_email,
        "ssh_key_path": new_ssh_key_path
    })

    save_config(config, config_path)
    print(f"✅ Modified profile '{args.profile}'.")


def select_profile(config, profile_name=None):
    profiles = config.get("profiles", [])
    if not profiles:
        print("🚫 No profiles configured.")
        sys.exit(1)

    if not profile_name:
        choices = [prof['name'] for prof in profiles]
        profile_name = prompt_choice("Select a Git profile", choices)

    profile = next((prof for prof in profiles if prof['name'] == profile_name), None)
    if not profile:
        print(f"🚫 Profile '{profile_name}' not found in configuration.")
        sys.exit(1)

    set_git_config(profile)
    set_ssh_config(profile)
    print("✅ Profile selection complete.")


def prompt_choice(message, choices):
    questions = [
        inquirer.List('choice',
                      message=message,
                      choices=choices,
                      carousel=True)
    ]
    answers = inquirer.prompt(questions)
    if answers:
        return answers['choice']
    else:
        sys.exit("🚫 No selection made.")


def set_git_config(profile):
    print(f"👤 Selecting profile: {profile['name']}")
    try:
        subprocess.run(["git", "config", "--global", "user.name", profile["user_name"]], check=True)
        subprocess.run(["git", "config", "--global", "user.email", profile["user_email"]], check=True)
        print(
            f"✅ Updated Git global config with user.name='{profile['user_name']}' and user.email='{profile['user_email']}'")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to update Git configuration: {e}")
        sys.exit(1)


def set_ssh_config(profile):
    ssh_key_path = os.path.expanduser(profile["ssh_key_path"])
    if not os.path.exists(ssh_key_path):
        print(f"❌ SSH key not found at {ssh_key_path}. Please ensure the SSH key exists.")
        sys.exit(1)

    os.chmod(ssh_key_path, 0o600)

    ssh_config_content = f"""# Managed by git-profile-cli
Host github.com
    HostName github.com
    User git
    IdentityFile {ssh_key_path}
    IdentitiesOnly yes
"""
    save_ssh_config(ssh_config_content)


def delete_profile(config, config_path, profile_name=None):
    profiles = config.get("profiles", [])
    if not profiles:
        print("🚫 No profiles configured.")
        return

    if not profile_name:
        choices = [prof['name'] for prof in profiles]
        profile_name = prompt_choice("Select a Git profile to delete", choices)

    profile = next((prof for prof in profiles if prof['name'] == profile_name), None)
    if not profile:
        print(f"🚫 Profile '{profile_name}' not found.")
        sys.exit(1)

    profiles.remove(profile)
    config["profiles"] = profiles
    save_config(config, config_path)
    print(f"🗑️ Deleted profile '{profile_name}' from configuration.")


def get_version():
    try:
        from ._version import version
        return version
    except ImportError:
        return "unknown"


def parse_args():
    parser = argparse.ArgumentParser(description="git-profile - Manage multiple Git profiles easily.")
    parser.add_argument(
        "--config",
        "-c",
        type=str,
        default=str(DEFAULT_CONFIG_FILE),
        help=f"Path to the YAML configuration file (default: {DEFAULT_CONFIG_FILE})"
    )
    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version=f"%(prog)s {get_version()}",
        help="Show the version number and exit"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    subparsers.add_parser("list", aliases=["l"], help="List all configured Git profiles")
    subparsers.add_parser("current", aliases=["c"], help="Display the current Git profile")

    add_parser = subparsers.add_parser("add", aliases=["a"], help="Add a new Git profile to the configuration")
    add_parser.add_argument("name", nargs='?', help="Unique name for the profile")
    add_parser.add_argument("user_name", nargs='?', help="Git user.name for the profile")
    add_parser.add_argument("user_email", nargs='?', help="Git user.email for the profile")
    add_parser.add_argument("ssh_key_path", nargs='?', help="Path to the SSH key for the profile")

    modify_parser = subparsers.add_parser("modify", aliases=["m"], help="Modify an existing Git profile")
    modify_parser.add_argument("profile", help="Name of the profile to modify")
    modify_parser.add_argument("--user_name", help="New user.name for the profile")
    modify_parser.add_argument("--user_email", help="New user.email for the profile")
    modify_parser.add_argument("--ssh_key_path", help="New SSH key path for the profile")

    select_parser = subparsers.add_parser("select", aliases=["s"], help="Select a specified Git profile")
    select_parser.add_argument("profile", nargs="?", help="Name of the profile to select")

    delete_parser = subparsers.add_parser("delete", aliases=["d"], help="Delete a specified Git profile")
    delete_parser.add_argument("profile", nargs="?", help="Name of the profile to delete")

    return parser.parse_args()


def main():
    args = parse_args()
    config_path = Path(args.config)

    if config_path.suffix not in [".yaml", ".yml"]:
        print("⚠️ Configuration file must have a .yaml or .yml extension.")
        sys.exit(1)

    config = load_config(config_path)

    if args.command in ["list", "l"]:
        list_profiles(config)
    elif args.command in ["current", "c"]:
        current_profile(config)
    elif args.command in ["add", "a"]:
        add_profile(config, config_path, args)
    elif args.command in ["modify", "m"]:
        modify_profile(config, config_path, args)
    elif args.command in ["select", "s"]:
        select_profile(config, args.profile)
    elif args.command in ["delete", "d"]:
        delete_profile(config, config_path, args.profile)
    else:
        select_profile(config)


if __name__ == "__main__":
    main()
