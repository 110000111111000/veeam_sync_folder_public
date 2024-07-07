import os

# Define the parent directories and the common directory name
# Make sure these directories exist and are writable
parent_dir1 = "/Users/baharspring/veeam/parent1"
parent_dir2 = "/Users/baharspring/veeam/parent2"
directory_name = "common_directory_name"

# Full paths for the directories
dir1 = os.path.join(parent_dir1, directory_name)
dir2 = os.path.join(parent_dir2, directory_name)

# Create the directories
os.makedirs(dir1, exist_ok=True)
os.makedirs(dir2, exist_ok=True)

print(f"Directories {dir1} and {dir2} have been created.")
