import os
import shutil
#import logging

source = "/Users/baharspring/veeam/source"
replica = "/Users/baharspring/veeam/replica"

## Function to estimate the size of folders
def get_directory_size(directory):
	"""
    Calculate the total size of all files in a directory (including subdirectories).

    Args:
    - directory: The path to the directory whose size needs to be calculated.

    Returns:
    - int: Total size of all files in bytes.None if there's an error.
    """
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

import os

source = "/Users/baharspring/veeam/source"


def get_structure_folder(directory):
    """
    Collect the structure of a directory, including all its subdirectories.

    Args:
    - directory (str): Path to the directory whose structure needs to be collected.

    Returns:
    - list of str: A list of relative paths of all subdirectories.
    """

    try:
        sub_dirs = []

        # steps through the directory   
        for dirpath, dirnames, filenames in os.walk(directory):
            relpath = os.path.relpath(dirpath, directory)
            sub_dirs.append(relpath)

        # Check if the directory is empty
        if not sub_dirs:
            print(f'The directory "{directory}"" is empty.')
        else:
            print(f'Collected structure for directory "{directory}"')   
            print(sub_dirs)

    except OSError as e:
        print(f"OS error occurred during directory structure comparison: {e}")

        return None

    return sub_dirs

#get_structure_folder()



def compare_directory_structure(source, replica):
    """
    Compare the directory structure (including subdirectory names) of two folders.

    Args:
    - source (str): Path to the source directory.
    - replica (str): Path to the replica directory.

    Returns:
    - bool: True if directory structures match, False otherwise.
    """
    try:
        # Get lists of subdirectories in source and replica
        source_dirs = []
        replica_dirs = []

        for dirpath, dirnames, filenames in os.walk(source):
            relpath = os.path.relpath(dirpath, source)
            source_dirs.append(relpath)

        for dirpath, dirnames, filenames in os.walk(replica):
            relpath = os.path.relpath(dirpath, replica)
            replica_dirs.append(relpath)

        # Sort the lists of directories
        source_dirs.sort()
        replica_dirs.sort()

        # Compare the lists
        if source_dirs == replica_dirs:
            print("Directory structures match.")
            return True
        else:
            print("Directory structures do not match.")
            return False

    except OSError as e:
        print(f"OS error occurred during directory structure comparison: {e}")
        return False
    except Exception as e:
        print(f"Error occurred during directory structure comparison: {e}")
        return False

# Example usage:
if __name__ == "__main__":
    source = "/Users/baharspring/veeam/source"
    replica = "/Users/baharspring/veeam/replica"

    structure_match = compare_directory_structure(source, replica)
    if structure_match:
        print("Directory structures are the same.")
    else:
        print("Directory structures are different.")    



def compare_directories(source, replica):
    try:

        # Calculate sizes of source and replica directories
        source_size = get_directory_size(source)
        replica_size = get_directory_size(replica)
        # Check if overall directory sizes match
        if source_size != replica_size:
            print("Source and replica directories have different sizes.")
            return False

		# Walk through the source directory
        for dirpath, dirnames, _ in os.walk(source):
            relpath = os.path.relpath(dirpath, source)
            replica_dir = os.path.join(replica, relpath)

		# Check if replica subdirectory exists
        if not os.path.exists(replica_dir):
            return False

		# Compare sizes of current subdirectories
        for dirname in dirnames:
            source_subdir = os.path.join(dirpath, dirname)
            replica_subdir = os.path.join(replica_dir, dirname)

			# Check if replica subdirectory exists
            if not os.path.exists(replica_subdir):
                return False

            # Compare sizes of subdirectories
            source_subdir_size = get_directory_size(source_subdir)
            replica_subdir_size = get_directory_size(replica_subdir)

            if source_subdir_size != replica_subdir_size:
                return False
            return True    

    except Exception as e:
        print(f"Error occurred during directory comparison: {e}")
        return False

def synchronize_directories(source, replica):
    try:
        working_directory = os.getcwd()
        working_directory_status = f'You are Here: "{working_directory}"'

		# check if the source folder exists
        if os.path.exists(source):
            source_status = f'The source folder "{source}" exists.'
            source_size = get_directory_size(source)
            source_structure = get_structure_folder(source)
        else:
            source_status = f'The source folder "{source}" does not exist. Provide the correct source folder path!'
            source_size = None
            source_structure = None

		# Check if the replica folder exists and create it if it doesn't	
        if not os.path.exists(replica):
            replica_status = f'The replica folder "{replica}" does not exist, so it has been created.'
            shutil.copytree(source, replica)
            print(f"Directory '{source}' has been successfully copied to '{replica}'.")
            #os.makedirs(replica)
        else:	
            replica_status = f'The replica folder "{replica}" exists.'
            replica_size = get_directory_size(replica)
            replica_structure = get_structure_folder(replica)

		# Print the status messages
        print(working_directory_status)
        print(source_status)
        print(replica_status)
        print(f"Source folder size: {source_size} bytes" if source_size is not None else "Source folder does not exist.")		 
        print(f"Replica folder size: {replica_size} bytes" if replica_size is not None else "Replica folder does not exist.")

        return working_directory_status, source_status, replica_status, source_size, replica_size
    except Exception as e:
        print(f"Error occurred: {e}")
        return None



synchronize_directories(source, replica)	 
