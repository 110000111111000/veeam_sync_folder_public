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

get_structure_folder(source)
