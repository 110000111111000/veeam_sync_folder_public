import os
import shutil
import hashlib
#import logging
#import argparse
#import time

# Initialize logging
#logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
source = "/Users/baharspring/veeam/source"
replica = "/Users/baharspring/veeam/replica"

def get_stat_folders(directory):
    stat_folder = os.stat(directory)
    """
    Retrieve stat information (metadata) of a directory.

    Args:
    - directory (str): Path to the directory.

    Returns:
    - stat_folder (os.stat_result object): Object containing metadata of the directory.
    """
    return stat_folder
print(get_stat_folders(source))


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
        logging.error(f"OS error occurred during directory structure comparison: {e}")

        return None

    return sub_dirs





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
            replica_size = None
            shutil.copytree(source, replica)
            print(f"Directory '{source}' has been successfully copied to '{replica}'.")
            #os.makedirs(replica)
        else:	
            replica_status = f'The replica folder "{replica}" exists.'
            replica_size = get_directory_size(replica)
            replica_structure = get_structure_folder(replica)
            if replica_size == source_size:
                print("replica size is the same as source_size ")
                if replica_structure == source_structure:
                    print("source and replica has the same structure")
            else:
                print("replica size is not the same as source_size")    

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

#def main():
#    # Parse command-line arguments
#    parser = argparse.ArgumentParser(description='Synchronize directories and log synchronization details.')
#    parser.add_argument('source', type=str, help='Path to the source directory(Exp: /Users/baharspring/veeam/source)')
#    parser.add_argument('replica', type=str, help='Path to the replica directory')
#    parser.add_argument('--interval', type=int, default=3600, help='Synchronization interval in seconds (default: 3600)')
 #   parser.add_argument('--log', type=str, default='sync_log.txt', help='Path to the log file (default: sync_log.txt)')
    
#    args = parser.parse_args()

    # Configure logging to write to a file
#    logging.basicConfig(filename=args.log, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Perform initial synchronization
#    synchronize_directories(args.source, args.replica)

    # Run synchronization periodically based on interval
#    while True:
#        time.sleep(args.interval)
#        synchronize_directories(args.source, args.replica)

#if __name__ == "__main__":
#    main()	


