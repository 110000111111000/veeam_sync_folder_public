import os
import stat

def get_stat_folders(directory):
    """
    Recursively retrieve and print permissions of all directories, subdirectories, and files
    under the specified directory.

    Args:
    - directory (str): Path to the directory.

    Returns:
    - None: Prints the permissions of each directory, subdirectory, and file.
    """
    try:
        # Walk through the directory and its subdirectories
        for dirpath, dirnames, filenames in os.walk(directory):
            # Get stat information for the current directory
            st = os.stat(dirpath)
            
            # Extract permissions
            permissions = stat.filemode(st.st_mode)
            
            # Print permissions for the current directory
            print(f"Directory path: {dirpath}")
            print(f"SubDirectory path: {dirnames}")
            print(f"SubDirectory_files path: {filenames}")

            print(f"Permissions: {permissions}")
            print(f"Information related to the directory: {st}")
            print("-" * 50)
            
            # Print permissions for subdirectories
            for dirname in dirnames:
                print(dirname)
                subdir_path = os.path.join(dirpath, dirname)
                #print(subdir_path)
                
                st_subdir = os.stat(subdir_path)
                permissions_subdir = stat.filemode(st_subdir.st_mode)
                
                print(f"Subdirectory: {subdir_path}")
                print(f"Permissions: {permissions_subdir}")
                print(f"Information related to the subdirectory: {st_subdir}")
                print("-" * 50)
                
            
            # Print permissions for files inside the current directory
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                
                st_file = os.stat(file_path)
                permissions_file = stat.filemode(st_file.st_mode)
                    
                print(f"File: {file_path}")
                print(f"Permissions: {permissions_file}")
                print(f"Information related to the file: {st_file}")
                print("-" * 50) 
               
    except OSError as e:
        print(f"Error occurred while fetching permissions: {e}")

# Example usage:
directory_path = "/Users/baharspring/veeam/source"
get_stat_folders(directory_path)
