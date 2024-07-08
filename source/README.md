Sync_Folders

There is a program that performs one way synchronization source ----> replica

-Synchronization is carried out periodically and changes(file update, copying, removal operations) are displayed in the console and written to a log file.

-Folder paths, synchronization interval and log file path should be provided using command line arguments.

Requirements
-Python 3.x
-Libraries: hashlib, os, time, shutil, argparse, logging 

Usage
python3 sync_folders.py -h

Notes
-The script uses the MD5 hash of files to compare and determine if a file needs to be updated in the replica folder.

-If the source folder does not exist, the script will raise an error.

-If the replica folder does not exist, the script will raise an info and will creates a replica folder.

-The script checks permissions for source folders and its subdirectories also replica folders.

-The script will continuously monitor the source folder and synchronize it with the replica folder based on the specified time interval.

-To stop the script manually, use the keyboard interrupt (CTRL+C).

