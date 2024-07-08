import os
import math

source = '/Users/baharspring/veeam/source' 
def make_directory():
	working_directory = os.getcwd()
	if not os.path.exists(source):
		os.makedirs(source)
	if not os.path.exists('source/subdirectory11'):
		os.makedirs('source/subdirectory11')
	directory_path_text = '/Users/baharspring/veeam/source/subdirectory11'
	file_name = 'test11.txt'
	file_path = os.path.join(directory_path_text, file_name)
	# create the file
	for i in range (0,10):
		x = math.factorial(i)
		print('i',i, 'x', x)
		with open(file_path, 'a') as f:
			f.write(f'i:{i}, i!:{x}') 


	return(working_directory)
	

print('current working directory',make_directory())	
