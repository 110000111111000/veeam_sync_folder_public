import os
import shutil
import time
import hashlib
import logging
import argparse

def setup_logging(log_file):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ])

def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def sync_folders(source, replica):
    # Ensure the replica folder exists
    if not os.path.exists(replica):
        os.makedirs(replica)
        logging.info(f"Created directory: {replica}")

    # Copy files and directories from source to replica
    for item in os.listdir(source):
        source_item = os.path.join(source, item)
        replica_item = os.path.join(replica, item)

        if os.path.isdir(source_item):
            # If it's a directory, recursively sync
            sync_folders(source_item, replica_item)
        else:
            # If it's a file, copy it to the replica if it doesn't exist or is different
            if not os.path.exists(replica_item) or calculate_md5(source_item) != calculate_md5(replica_item):
                shutil.copy2(source_item, replica_item)
                logging.info(f"Copied: {source_item} to {replica_item}")

    # Delete files and directories from replica that are not in source
    for item in os.listdir(replica):
        source_item = os.path.join(source, item)
        replica_item = os.path.join(replica, item)

        if not os.path.exists(source_item):
            if os.path.isdir(replica_item):
                shutil.rmtree(replica_item)
                logging.info(f"Deleted directory: {replica_item}")
            else:
                os.remove(replica_item)
                logging.info(f"Deleted file: {replica_item}")

def main():
    parser = argparse.ArgumentParser(description="Synchronize two folders.")
    parser.add_argument('source', type=str, help='Path to the source folder: Exp: "/Users/baharspring/veeam"')
    parser.add_argument('replica', type=str, help='Path to the replica folder, Exp: "/Users/baharspring/veeam"')
    parser.add_argument('interval', type=int, help='Synchronization interval in seconds')
    parser.add_argument('log_file', type=str, help='Path to the log file')

    args = parser.parse_args()

    setup_logging(args.log_file)

    logging.info(f"Starting synchronization: source={args.source}, replica={args.replica}, interval={args.interval}s")

    while True:
        sync_folders(args.source, args.replica)
        time.sleep(args.interval)

if __name__ == "__main__":
    main()
