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
def sync_folders(source_folder, replica_folder, log_file, sync_interval):
    retry_delay = 5  # Delay before retrying in case of an error (in seconds)
    while True:
        try:
            # Check permissions
            source_permission, source_path = check_read_permission(source_folder)
            if not source_permission:
                logging.error(f"Permission denied: Cannot read from source folder or its subdirectory '{source_path}'")
                return

            replica_permission, replica_path = check_all_permissions(replica_folder)
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
    parser.add_argument('source', type=str, help='Path to the source directory')
    parser.add_argument('replica', type=str, help='Path to the replica directory')
    parser.add_argument('interval', type=int, help='Synchronization interval in seconds')
    parser.add_argument('--log', type=str, default='sync_log.txt', help='Path to the log file (default: sync_log.txt)')
    
    args = parser.parse_args()

    try:
        sync_folders(args.source, args.replica, args.log, args.interval)
    except KeyboardInterrupt:
        logging.info("\nSynchronization interrupted by user.")
    except Exception as e:
        logging.error(f"Error occurred during synchronization: {e}")
