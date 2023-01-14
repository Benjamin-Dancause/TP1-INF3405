import os

path = 'root/'

# Get the list of all files and folders in the directory
files_and_folders = os.listdir(path)

for name in files_and_folders:
    print(name)
