import os
import shutil
import hashlib
import stat

def compute_file_hash(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def print_permissions(filepath):
    st = os.stat(filepath)
    print(f"Permissions of {filepath}: {stat.filemode(st.st_mode)}")
    print(f"Owner UID: {st.st_uid}, GID: {st.st_gid}")

def adjust_permissions(path):
    try:
        os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # Give read/write/execute to owner, group, others
    except Exception as e:
        print(f"Failed to adjust permissions for {path}: {e}")

def sync_directories(source, replica):
    # Step 1: Initialize
    if not os.path.exists(source):
        raise ValueError("Source directory does not exist.")
    if not os.path.exists(replica):
        os.makedirs(replica)

    # Step 2 and 3: Compare Structures and Files
    for dirpath, dirnames, filenames in os.walk(source):
        relpath = os.path.relpath(dirpath, source)
        replica_dir = os.path.join(replica, relpath)

        if not os.path.exists(replica_dir):
            os.makedirs(replica_dir)

        source_files = set(filenames)
        replica_files = set(os.listdir(replica_dir))

        # Compare files
        for filename in source_files:
            source_file = os.path.join(dirpath, filename)
            replica_file = os.path.join(replica_dir, filename)

            if not os.path.exists(replica_file) or os.path.getsize(source_file) != os.path.getsize(replica_file):
                shutil.copy2(source_file, replica_file)
            else:
                if compute_file_hash(source_file) != compute_file_hash(replica_file):
                    shutil.copy2(source_file, replica_file)

        # Remove extra files from replica
        for filename in replica_files - source_files:
            replica_filepath = os.path.join(replica_dir, filename)
            try:
                print_permissions(replica_filepath)
                os.remove(replica_filepath)
            except PermissionError as e:
                print(f"PermissionError: {e} - Could not remove file {replica_filepath}")
                # Attempt to adjust permissions and retry
                try:
                    adjust_permissions(replica_filepath)
                    os.remove(replica_filepath)
                except Exception as e:
                    print(f"Failed to remove file with adjusted permissions: {e}")

    # Remove extra directories from replica
    for dirpath, dirnames, filenames in os.walk(replica, topdown=False):
        relpath = os.path.relpath(dirpath, replica)
        source_dir = os.path.join(source, relpath)

        for dirname in dirnames:
            replica_subdir = os.path.join(dirpath, dirname)
            if not os.path.exists(os.path.join(source_dir, dirname)):
                try:
                    print_permissions(replica_subdir)
                    shutil.rmtree(replica_subdir)
                except PermissionError as e:
                    print(f"PermissionError: {e} - Could not remove directory {replica_subdir}")
                    # Attempt to adjust permissions and retry
                    try:
                        adjust_permissions(replica_subdir)
                        shutil.rmtree(replica_subdir)
                    except Exception as e:
                        print(f"Failed to remove directory with adjusted permissions: {e}")

    # Step 5: Handle Metadata (Optional, if needed)
    # Set the metadata of files and directories in the replica to match the source
    for dirpath, dirnames, filenames in os.walk(source):
        relpath = os.path.relpath(dirpath, source)
        replica_dir = os.path.join(replica, relpath)

        for filename in filenames:
            source_file = os.path.join(dirpath, filename)
            replica_file = os.path.join(replica_dir, filename)
            shutil.copystat(source_file, replica_file)

        shutil.copystat(dirpath, replica_dir)

# Example usage:
source_dir = "/Users/baharspring/veeam/source"
replica_dir = "/Users/baharspring/veeam/replica"
sync_directories(source_dir, replica_dir)
