import os
import shutil
import hashlib
import time
import argparse

# Function to calculate MD5 checksum
def calculate_md5(file_path):
    """Calculate the MD5 checksum of a file."""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

# Function to check read permissions for a directory and its subdirectories
def check_read_permission(directory):
    """Check read permission for a directory and its subdirectories."""
    for root, _, _ in os.walk(directory):
        if not os.access(root, os.R_OK):
            return False, root
    return True, None

# Function to check all permissions (read, write, execute) for a directory and its subdirectories
def check_all_permissions(directory):
    """Check read, write, and execute permissions for a directory and its subdirectories."""
    for root, _, _ in os.walk(directory):
        if not (os.access(root, os.R_OK) and os.access(root, os.W_OK) and os.access(root, os.X_OK)):
            return False, root
    return True, None

# Function to synchronize directories
def sync_folders(source_folder, replica_folder, log_file):
    retry_delay = 5  # Delay before retrying in case of an error (in seconds)
    while True:
        try:
            source_permission, source_path = check_read_permission(source_folder)
            if not source_permission:
                print(f"Permission denied: Cannot read from source folder or its subdirectory '{source_path}'")
                return

            replica_permission, replica_path = check_all_permissions(replica_folder)
            if not replica_permission:
                print(f"Permission denied: Insufficient permissions for replica folder or its subdirectory '{replica_path}'")
                return
            
            with open(log_file, 'a') as log:
                # Sync from source to replica
                for root, dirs, files in os.walk(source_folder):
                    rel_path = os.path.relpath(root, source_folder)
                    dest_path = os.path.join(replica_folder, rel_path)
                    if not os.path.exists(dest_path):
                        os.makedirs(dest_path)
                        log.write(f'{time.ctime()} - Created directory: {dest_path}\n')
                        print(f'Created directory: {dest_path}')
                    for file in files:
                        source_file = os.path.join(root, file)
                        replica_file = os.path.join(dest_path, file)
                        if not os.path.exists(replica_file) or calculate_md5(source_file) != calculate_md5(replica_file):
                            shutil.copy2(source_file, replica_file)
                            log.write(f'{time.ctime()} - Copied file: {source_file} to {replica_file}\n')
                            print(f'Copied file: {source_file} to {replica_file}')
                # Remove files and directories in replica that are not in source
                for root, dirs, files in os.walk(replica_folder):
                    rel_path = os.path.relpath(root, replica_folder)
                    source_path = os.path.join(source_folder, rel_path)
                    if not os.path.exists(source_path):
                        shutil.rmtree(root)
                        log.write(f'{time.ctime()} - Removed directory: {root}\n')
                        print(f'Removed directory: {root}')
                        continue
                    for file in files:
                        replica_file = os.path.join(root, file)
                        source_file = os.path.join(source_path, file)
                        if not os.path.exists(source_file):
                            os.remove(replica_file)
                            log.write(f'{time.ctime()} - Removed file: {replica_file}\n')
                            print(f'Removed file: {replica_file}')
            break  # Exit the loop if everything went well
        except OSError as e:
            print(f"OSError occurred: {e}. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)

def synchronize_directories(source, replica, log_file):
    try:
        working_directory = os.getcwd()
        print(f'You are Here: "{working_directory}"')

        if os.path.exists(source):
            print(f'The source folder "{source}" exists.')
            source_size = get_directory_size(source)
            source_structure = get_structure_folder(source)
        else:
            print(f'The source folder "{source}" does not exist. Provide the correct source folder path!')
            return

        if not os.path.exists(replica):
            print(f'The replica folder "{replica}" does not exist, so it has been created.')
            shutil.copytree(source, replica)
            print(f"Directory '{source}' has been successfully copied to '{replica}'.")
        else:
            print(f'The replica folder "{replica}" exists.')
            replica_size = get_directory_size(replica)
            replica_structure = get_structure_folder(replica)
            if replica_size == source_size and replica_structure == source_structure:
                print("Replica size and structure match source.")
            else:
                print("Replica size or structure do not match source.")
                sync_folders(source, replica, log_file)
    except Exception as e:
        print(f"Error occurred: {e}")

def get_directory_size(directory):
    try:
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                total_size += os.path.getsize(filepath)
    except OSError as e:
        print(f"Error occurred while calculating directory size for {directory}: {e}")
        return None
    return total_size

def get_structure_folder(directory):
    try:
        sub_dirs = []
        for dirpath, dirnames, filenames in os.walk(directory):
            relpath = os.path.relpath(dirpath, directory)
            sub_dirs.append(relpath)
        if not sub_dirs:
            print(f'The directory "{directory}" is empty.')
        else:
            print(f'Collected structure for directory "{directory}"')
            print(sub_dirs)
    except OSError as e:
        print(f"OS error occurred during directory structure comparison: {e}")
        return None
    return sub_dirs

def main():
    parser = argparse.ArgumentParser(description='One-way folder synchronization.')
    parser.add_argument('source', type=str, help='Path to the source folder')
    parser.add_argument('replica', type=str, help='Path to the replica folder')
    parser.add_argument('interval', type=int, help='Synchronization interval in seconds')
    parser.add_argument('log_file', type=str, help='Path to the log file')
    args = parser.parse_args()

    while True:
        synchronize_directories(args.source, args.replica, args.log_file)
        time.sleep(args.interval)

if __name__ == '__main__':
    main()
