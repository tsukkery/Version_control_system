import argparse
import os
import sys
from datetime import datetime

VERSION_FILE = "version"
VERSION_LOG_FILE = "version_log"
DEFAULT_VERSION = "0.0.0"

def read_version(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            line = f.readline().strip()
            if not line:
                print("No existing version found. Using default.")
                write_version(DEFAULT_VERSION)
                return DEFAULT_VERSION
            return line
    except FileNotFoundError:
        print(f"Version file '{filename}' not found. Creating it with default version.")
        write_version(DEFAULT_VERSION)
        return DEFAULT_VERSION

def print_version_log(line_count):
    try:
        with open(VERSION_LOG_FILE, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines()]
            if not lines:
                print("Version log file is empty.")
                return
            if line_count is not None:
                lines = lines[:line_count]
            for line in lines:
                print(line)
    except FileNotFoundError:
        raise FileNotFoundError(f"Version log file '{VERSION_LOG_FILE}' not found.")


def create_path(path):
    os.makedirs(path, exist_ok=True)
    global VERSION_FILE
    global VERSION_LOG_FILE
    VERSION_FILE = os.path.join(path, VERSION_FILE)
    VERSION_LOG_FILE = os.path.join(path, VERSION_LOG_FILE)


def write_version(version):
    try:
        with open(VERSION_FILE, "w", encoding="utf-8") as f:
            f.write(version)
    except Exception as e:
        raise Exception(f"Error writing to '{VERSION_FILE}': {e}")


def write_version_log(old_version, new_version, message):
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S.%f")
    entry = f"[{new_version}] <- [{old_version}] [{timestamp}] {message}\n"
    try:
        if not os.path.isfile(VERSION_LOG_FILE):
            print(f"Version log file '{VERSION_LOG_FILE}' not found. Creating it.")
            open(VERSION_LOG_FILE, "w", encoding="utf-8").close()
        with open(VERSION_LOG_FILE, "r", encoding="utf-8") as f:
            existing = f.read()
        with open(VERSION_LOG_FILE, "w", encoding="utf-8") as f:
            f.write(entry + existing)
    except Exception as e:
        raise Exception(f"Error writing to '{VERSION_LOG_FILE}': {e}")


def update_version(version_type, message):
    version = get_version(VERSION_FILE)
    try:
        major, minor, patch = map(int, version.split("."))
    except ValueError:
        raise ValueError(f"Invalid version format: '{version}'. Must be 'X.Y.Z'.")
    if version_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif version_type == "minor":
        minor += 1
        patch = 0
    elif version_type == "patch":
        patch += 1
    else:
        raise ValueError(f"Invalid version type: '{version_type}'. Must be 'major', 'minor' or 'patch'.")
    new_version = f"{major}.{minor}.{patch}"
    write_version(new_version)
    write_version_log(version, new_version, message)
    print(f"Done! Updated from '{version}' to '{new_version}'.")


def reset_file(filename, confirm_arg):
    if confirm_arg:
        response = "y"
    else:
        response = input(f"Are you sure you want to RESET '{filename}'?\n"
                         f"Answer (y/n): ")
    if response.lower() == "y":
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("")
            print(f"Done! File '{filename}' resetted.")
        except EOFError:
            print("Reset cancelled.")
        except FileNotFoundError:
            print(f"Nothing to reset!")
        except Exception as e:
            raise Exception(f"Error resetting file '{filename}': {e}")
    else:
        print("Reset cancelled.")


def undo():
    try:
        with open(VERSION_LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
            if not lines:
                print(f"Can't undo! '{VERSION_LOG_FILE}' is empty.")
                return
    except Exception as e:
        raise Exception(f"Error reading '{VERSION_LOG_FILE}': {e}")
    last_entry = lines[0].strip()
    match = re.match(r"\[(.*?)] <- \[(.*?)] \[(.*?)] (.*)", last_entry)
    if not match:
        raise ValueError(f"Couldn't parse last log entry: '{last_entry}'."
                         f"Fix it manually.")
    new_version, old_version, timestamp, message = match.groups()
    write_version(old_version)
    print(f"Done! Version restored to: {old_version}")
    try:
        with open(VERSION_LOG_FILE, "w", encoding="utf-8") as f:
            f.writelines(lines[1:])
    except Exception as e:
        raise Exception(f"Error writing to version log file: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Project versioning script")
    group = parser.add_mutually_exclusive_group()
    parser.add_argument("workdir_path", nargs="?", const=".", default=".", help="Path to working directory")
    group.add_argument("version_type", nargs="?", choices=["major", "minor", "patch"],
                       help="increment version type (major, minor, patch)")
    parser.add_argument("-m", "--message", nargs="?", default="", const="", help="commit message for version change")
    parser.add_argument("-y", "--yes", action="store_true", help="suppress confirmation")
    parser.add_argument("-v", "--version", action="store_true", help="print current version")
    parser.add_argument("--version_log", nargs="?", type=int, const=1,
                        help="print specified count of log lines (default - 1)")
    group.add_argument("--reset_version", action="store_true", help="reset version file")
    group.add_argument("--reset_version_log", action="store_true", help="reset version log file")
    group.add_argument("--undo", action="store_true", help="back to previous version")

    args = parser.parse_args()

    create_path(args.workdir_path)

    if args.message and any([args.reset_version, args.reset_version_log, args.undo]):
        parser.error("'--message' can only be specified with 'version_type'!")
    if not args.version_type and args.message:
        parser.error("'--message' can only be specified with 'version_type'!")
    if not args.yes and args.reset_version or not args.yes and args.reset_version_log:
        parser.error("'-y' can only be specified with 'reset_version' or 'reset_version_log'!")

    if args.version_type:
        update_version(args.version_type, args.message)
    elif args.version:
        print(read_version(VERSION_FILE))
    elif args.version_log:
        print_version_log(args.version_log)
    elif args.reset_version:
        reset_file(VERSION_FILE, args.yes)
    elif args.reset_version_log:
        reset_file(VERSION_LOG_FILE, args.yes)
    elif args.undo:
        undo()
    else:
        parser.print_help()
