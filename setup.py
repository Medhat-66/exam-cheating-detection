import os

base_dir = os.path.dirname(os.path.abspath(__file__))

folders = [
    "assets/icons",
    "assets/logo",
    "assets/models",
    "data/database",
    "data/screenshots",
    "data/videos",
    "data/logs",
    "src/config",
    "src/core",
    "src/behavior",
    "src/database_manager",
    "src/notification",
    "src/ui",
    "src/utils"
]

files = [
    "main.py",
    "requirements.txt",
    "src/config/settings.py",
    "src/utils/logger.py",
    "src/database_manager/db_manager.py",
    "src/notification/notifier.py",
    "src/utils/screenshot.py"
]

for folder in folders:
    os.makedirs(os.path.join(base_dir, folder), exist_ok=True)

for file in files:
    filepath = os.path.join(base_dir, file)
    with open(filepath, 'w') as f:
        pass

print("DONE!")