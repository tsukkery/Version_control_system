import os
import sys
from datetime import datetime

def read_version():
    if os.path.exists("version"):
        with open("version", "r") as f:
            return f.read().strip()
    else:
        return None

def write_version(version):
    with open("version", "w") as f:
        f.write(version)

def write_log(old_version, new_version, update_type):
    with open("version_log", "a") as log_file:
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S.%f")[:-3]  # Получаем временную метку
        log_message = f"[{new_version}] <- [{old_version}][{timestamp}] {update_type} update\n"
        log_file.write(log_message)

def increment_version(version, update_type):
    major, minor, patch = map(int, version.split('.'))

    if update_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif update_type == "minor":
        minor += 1
        patch = 0
    elif update_type == "patch":
        patch += 1

    return f"{major}.{minor}.{patch}"

def main():
    if not os.path.exists("version"):
        print("File version not found, creating new one with version 1.0.0.")
        write_version("1.0.0")
    
    current_version = read_version()
    if current_version is None:
        print("Error: couldn't read last version.")
        return
    
    version_parts = current_version.split(".")
    if len(version_parts) != 3 or not all(part.isdigit() for part in version_parts):
        print("Wrong version format in file version. Required format 0.0.0")
        return
    
    if len(sys.argv) != 2 or sys.argv[1] not in ["major", "minor", "patch"]:
        print("Error: incorrect parameter (major, minor or patch).")
        return
    
    update_type = sys.argv[1]
    
    new_version = increment_version(current_version, update_type)
    
    write_version(new_version)
    
    write_log(current_version, new_version, update_type)
    
    print(f"Version updated from {current_version} to {new_version}.")

if __name__ == "__main__":
    main()
