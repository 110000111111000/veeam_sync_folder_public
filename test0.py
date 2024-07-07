import os
import time
import hashlib
import shutil
import sys
import argparse
from datetime import datetime

def calculate_md5(file_path):
    """Calculate the MD5 checksum of a file."""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def sync_folders(source_folder, replica_folder, log_file):
    """Synchronize the replica folder to match the source folder."""
    with open(log_file, 'a') as log:
        # Sync from source to replica
        for root, dirs, files in os.walk(source_folder):
            rel_path = os.path.relpath(root, source_folder)
            dest_path = os.path.join(replica_folder, rel_path)
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)
                log.write(f'{datetime.now()} - Created directory: {dest_path}\n')
                print(f'Created directory: {dest_path}')
            
            for file in files:
                source_file = os.path.join(root, file)
                replica_file = os.path.join(dest_path, file)
                if not os.path.exists(replica_file) or calculate_md5(source_file) != calculate_md5(replica_file):
                    shutil.copy2(source_file, replica_file)
                    log.write(f'{datetime.now()} - Copied file: {source_file} to {replica_file}\n')
                    print(f'Copied file: {source_file} to {replica_file}')
        
        # Remove files and directories in replica that are not in source
        for root, dirs, files in os.walk(replica_folder):
            rel_path = os.path.relpath(root, replica_folder)
            source_path = os.path.join(source_folder, rel_path)
            if not os.path.exists(source_path):
                shutil.rmtree(root)
                log.write(f'{datetime.now()} - Removed directory: {root}\n')
                print(f'Removed directory: {root}')
                continue
            
            for file in files:
                replica_file = os.path.join(root, file)
                source_file = os.path.join(source_path, file)
                if not os.path.exists(source_file):
                    os.remove(replica_file)
                    log.write(f'{datetime.now()} - Removed file: {replica_file}\n')
                    print(f'Removed file: {replica_file}')

def main():
    parser = argparse.ArgumentParser(description='One-way folder synchronization.')
    parser.add_argument('source_folder', type=str, help='Path to the source folder')
    parser.add_argument('replica_folder', type=str, help='Path to the replica folder')
    parser.add_argument('interval', type=int, help='Synchronization interval in seconds')
    parser.add_argument('log_file', type=str, help='Path to the log file')

    args = parser.parse_args()

    while True:
        sync_folders(args.source_folder, args.replica_folder, args.log_file)
        time.sleep(args.interval)

if __name__ == '__main__':
    main()
