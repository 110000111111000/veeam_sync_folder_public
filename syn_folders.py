import os
import shutil
import hashlib
import time
import argparse
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to calculate MD5 checksum
def calculate_md5(file_path):
    """Calculate the MD5 checksum of a file."""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

# Function to check (read, write, execute) permissions for a directory and its subdirectories
def check_permission(directory):
    """Check  RWX (read, write, execute) permissions for a directory and its subdirectories."""
    subdirectories = []
    files = []

    for root, dirs, files_list in os.walk(directory):
        # Check root permissions
        if not (os.access(root, os.R_OK) and os.access(root, os.W_OK) and os.access(root, os.X_OK)):
            return False, root

        for name in dirs:
            subdirectory = os.path.join(root, name)
            subdirectories.append(subdirectory)
            read_permission = os.access(subdirectory, os.R_OK)
            write_permission = os.access(subdirectory, os.W_OK)
            execute_permission = os.access(subdirectory, os.X_OK)
            #print(f'Subdirectory: {subdirectory}, Readable: {read_permission}, Writable: {write_permission}, Executable: {execute_permission}')
            if not (os.access(subdirectory, os.R_OK) and os.access(subdirectory, os.W_OK) and os.access(subdirectory, os.X_OK)):
                return False, subdirectory

        for name in files_list:
            file_path = os.path.join(root, name)
            files.append(file_path)
            read_permission = os.access(file_path, os.R_OK)
            write_permission = os.access(file_path, os.W_OK)
            execute_permission = os.access(file_path, os.X_OK)
            #print(f'File: {file_path}, Readable: {read_permission}, Writable: {write_permission}, Executable: {execute_permission}')
            if not (os.access(file_path, os.R_OK) and os.access(file_path, os.W_OK) and os.access(file_path, os.X_OK)):
                return False, file_path
               
    return True, (subdirectories, files)

# Function to synchronize directories
def sync_folders(source_folder, replica_folder, log_file, sync_interval):
    # Check if source folder exists
    if not os.path.exists(source_folder):
        logging.error(f"Source folder '{source_folder}' does not exist.")
        return
    # Check if replica folder exists
    if not os.path.exists(replica_folder):
        logging.info(f"Replica folder '{replica_folder}' does not exist. Creating replica ...")
        os.makedirs(replica_folder)
        logging.info(f"Replica folder '{replica_folder}' created.")
   
    retry_delay = 5  # Delay before retrying in case of an error (in seconds)
    while True:
        try:
            # Check permissions
            source_permission, source_path = check_permission(source_folder)
            if not source_permission:
                logging.error(f"Permission denied: Cannot read from source folder or its subdirectory '{source_path}'")
                return

            replica_permission, replica_path = check_permission(replica_folder)
            if not replica_permission:
                logging.error(f"Permission denied: Insufficient permissions for replica folder or its subdirectory '{replica_path}'")
                return

            # Perform synchronization
            with open(log_file, 'a') as log:
                # Sync from source to replica
                for root, dirs, files in os.walk(source_folder):
                    rel_path = os.path.relpath(root, source_folder)
                    dest_path = os.path.join(replica_folder, rel_path)
                    if not os.path.exists(dest_path):
                        os.makedirs(dest_path)
                        log.write(f'{time.ctime()} - Created directory: {dest_path}\n')
                        logging.info(f'Created directory: {dest_path}')
                    for file in files:
                        source_file = os.path.join(root, file)
                        replica_file = os.path.join(dest_path, file)
                        if not os.path.exists(replica_file) or calculate_md5(source_file) != calculate_md5(replica_file):
                            shutil.copy2(source_file, replica_file)
                            log.write(f'{time.ctime()} - Copied file: {source_file} to {replica_file}\n')
                            logging.info(f'Copied file: {source_file} to {replica_file}')
                # Remove files and directories in replica that are not in source
                for root, dirs, files in os.walk(replica_folder):
                    rel_path = os.path.relpath(root, replica_folder)
                    source_path = os.path.join(source_folder, rel_path)
                    if not os.path.exists(source_path):
                        shutil.rmtree(root)
                        log.write(f'{time.ctime()} - Removed directory: {root}\n')
                        logging.info(f'Removed directory: {root}')
                        continue
                    for file in files:
                        replica_file = os.path.join(root, file)
                        source_file = os.path.join(source_path, file)
                        if not os.path.exists(source_file):
                            os.remove(replica_file)
                            log.write(f'{time.ctime()} - Removed file: {replica_file}\n')
                            logging.info(f'Removed file: {replica_file}')
            
            logging.info("Synchronization complete. Waiting for the next interval...")
            time.sleep(sync_interval)  # Sleep for the specified synchronization interval
        
        except OSError as e:
            logging.error(f"OSError occurred: {e}. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        except Exception as e:
            logging.error(f"Exception occurred: {e}")
            return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Synchronize directories and log synchronization details.')
    parser.add_argument('source', type=str, help='Path to the source directory exp:(/Users/baharspring/veeam/source)')
    parser.add_argument('replica', type=str, help='Path to the replica directory exp:(/Users/baharspring/veeam/replica)')
    parser.add_argument('interval', type=int, help='Synchronization interval in seconds')
    parser.add_argument('--log', type=str, default='sync_log.txt', help='Path to the log file (default: sync_log.txt),EXP how to execute the [sync_folders.py] =  python3 sync_folders.py /Users/baharspring/veeam/source /Users/baharspring/veeam/replica 20 --log /Users/baharspring/veeam/logfile')
    
    args = parser.parse_args()

    try:
        sync_folders(args.source, args.replica, args.log, args.interval)
    except KeyboardInterrupt:
        logging.info("\nSynchronization interrupted by user.")
    except Exception as e:
        logging.error(f"Error occurred during synchronization: {e}")
