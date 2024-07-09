**Sync_Folders**

This program performs one-way synchronization from source ----> replica.

- Synchronization is carried out periodically changes(creating, copying, removal operations) are displayed in the console and written to a log file.

- Folder paths, synchronization interval, and log file path should be provided using command line arguments.

**Requirements**

- Python 3.x
- Libraries: hashlib, os, time, shutil, argparse, logging 

**Usage**

#Display help message

python3 sync_folders.py -h

#Run synchronization

python3 syn_folders.py /path/to/source /path/to/replica 5 --log /path/to/logfile

**Notes**

- The script uses the MD5 hash of files to compare and determine if a file needs to be updated in the replica folder.

- If the source folder does not exist, the script will raise an error.

- If the replica folder does not exist, the script will raise an info message on the cosole and creates the replica folder.

- The script checks permissions for source folders and its subdirectories as well as replica folder and its subdirectories.

- The script will continuously monitor the source folder and synchronize it with the replica folder based on the specified time interval.

- To stop the script manually, use the keyboard interrupt (CTRL+C).

