import os
import datetime
import sys

if not os.path.exists('version'):
    with open('version', 'w') as f:
        f.write('1.0.0')

with open('version', 'r') as f:
    version = f.read().strip()

if not all(i.isdigit() for i in version.split('.')):
    print("Некорректный формат версии")
    exit()

if len(sys.argv) < 2:
    print("Не указан параметр обновления (major, minor, patch)!")
    exit()

update_type = sys.argv[1]

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
else:
    print("Некорректный параметр обновления!")
    exit()

new_version = f"{major}.{minor}.{patch}"

with open('version', 'w') as f:
    f.write(new_version)

current_time = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S.%f")[:-3]
with open('version_log', 'a') as f:
    f.write(f"[{new_version}] <- [{version}] [{current_time}] {update_type} update\n")

print(f"Версия обновлена на {new_version}")
