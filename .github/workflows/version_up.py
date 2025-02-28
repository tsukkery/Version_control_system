import os
import sys
from datetime import datetime

VERSION_FILE = 'version'
LOG_FILE = 'version_log'

def get_current_timestamp():
    now = datetime.now()
    return now.strftime('%d.%m.%Y %H:%M:%S.') + f'{now.microsecond // 1000:03d}'

def read_version():
    if not os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, 'w') as f:
            f.write('1.0.0\n')
    with open(VERSION_FILE, 'r') as f:
        return f.read().strip()

def write_version(version):
    with open(VERSION_FILE, 'w') as f:
        f.write(version)

def print_version():
    print(read_current_version())

def log_version_change(old_version, new_version, update_type):
    timestamp = datetime.now().strftime('%d.%m.%Y %H:%M:%S.%f')[:-3]
    log_entry = f"[{new_version}] <- [{old_version}] [{timestamp}] {update_type} update\n"
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(log_entry)

def increment_version(version, update_type):
    major, minor, patch = map(int, version.split('.'))

    if update_type == 'major':
        major += 1
        minor = 0
        patch = 0
    elif update_type == 'minor':
        minor += 1
        patch = 0
    elif update_type == 'patch':
        patch += 1

    new_version = f'{major}.{minor}.{patch}'
    write_version(new_version)
    timestamp = get_current_timestamp()
    log_entry = f'[{new_version}] <- [{current}] [{timestamp}] {update_type} update'
    prepend_to_file(VERSION_LOG_FILE, log_entry)
    print(f"Версия обновлена до {new_version}")

    return f"{major}.{minor}.{patch}"

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <update_type>")
        print("update_type should be one of: major, minor, patch")
        sys.exit(1)

    update_type = sys.argv[1]

    current_version = read_version()
    new_version = increment_version(current_version, update_type)

    write_version(new_version)
    log_version_change(current_version, new_version, update_type)

    print(f"Version updated from {current_version} to {new_version}")

if __name__ == "__main__":
    main()
