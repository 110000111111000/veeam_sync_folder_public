import os

directory1 = "/Users/baharspring/veeam/source"

def check_RWE_permission(directory):
    subdirectories = []
    files = []

    for root, dirs, files_list in os.walk(directory, topdown=True):
        # Check root permissions
        if not (os.access(root, os.R_OK) and os.access(root, os.W_OK) and os.access(root, os.X_OK)):
            return False, root

        for name in dirs:
            subdirectory = os.path.join(root, name)
            subdirectories.append(subdirectory)
            read_permission = os.access(subdirectory, os.R_OK)
            write_permission = os.access(subdirectory, os.W_OK)
            execute_permission = os.access(subdirectory, os.X_OK)
            print(f'Subdirectory: {subdirectory}, Readable: {read_permission}, Writable: {write_permission}, Executable: {execute_permission}')
            if not (read_permission and write_permission and execute_permission):
                return False, subdirectory

        for name in files_list:
            file_path = os.path.join(root, name)
            files.append(file_path)
            read_permission = os.access(file_path, os.R_OK)
            write_permission = os.access(file_path, os.W_OK)
            execute_permission = os.access(file_path, os.X_OK)
            print(f'File: {file_path}, Readable: {read_permission}, Writable: {write_permission}, Executable: {execute_permission}')
            if not (read_permission and write_permission and execute_permission):
                return False, file_path

    return True, (subdirectories, files)

# Calling the function and capturing the results
permission, details = check_RWE_permission(directory1)

# Printing the results
if permission:
    subdirs, files = details
    print("Subdirectories:", subdirs)
    print("Files:", files)
else:
    print(f"Permission denied at: {details}")
