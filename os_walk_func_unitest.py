import os

directory1 = "/Users/baharspring/veeam/source"

def check_RWE_permission(directory, indent=0):
    subdirectories = []
    files = []

    for root, dirs, files_list in os.walk(directory, topdown=True):
        for name in dirs:
            subdirectory = os.path.join(root, name)
            subdirectories.append(subdirectory)
            read_permission = os.access(subdirectory, os.R_OK)
            write_permission = os.access(subdirectory, os.W_OK)
            execute_permission = os.access(subdirectory, os.X_OK)
            print(f'Subdirectory: {subdirectory}, Readable: {read_permission}, Writable: {write_permission}, Executable: {execute_permission}')  

        for name in files_list:
            file_path = os.path.join(root, name)
            files.append(file_path)
            read_permission = os.access(file_path, os.R_OK)
            write_permission = os.access(file_path, os.W_OK)
            execute_permission = os.access(file_path, os.X_OK)
            print(f'File: {file_path}, Readable: {read_permission}, Writable: {write_permission}, Executable: {execute_permission}')
            


    return subdirectories, files

# Calling the function and capturing the results
subdirs, files = check_RWE_permission(directory1)

# Printing the results
print("Subdirectories:", subdirs)
print("Files:", files)

