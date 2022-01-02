# cloud-sync

# File hash

The "[name of folder]\_file_hashes.json", inside the "hashes" folder, contains a json object with a list of hashes (blocks).
Each block contains some information that represents that hashed file. Example of the "[name of folder]\_file_hashes.json":

```
{
    "length": "",
    "files": {
        "example_hash_of_file": {
            "file_hash": "",
            "local_file_path": "",
        }
    },
    "missing files": [],
    "duplicate files": {}
}
```

# Dummy folder and files

To create a dummy file for testing in powershell:

```
new-item -name "folder1" -itemtype "directory"
new-item -name "folder2" -itemtype "directory"
new-item -name "folder3" -itemtype "directory"
new-item -name "hashes" -itemtype "directory"

fsutil file createnew "folder1/wow1.mp4" 1
fsutil file createnew "folder1/wow12.mp4" 12
fsutil file createnew "folder1/wow123.mp4" 123

fsutil file createnew "folder2/lol9.mp4" 9
fsutil file createnew "folder2/lol98.mp4" 98
fsutil file createnew "folder2/lol987.mp4" 987
new-item "folder2" -name "folder2.1" -itemtype "directory"
fsutil file createnew "folder2/folder2.1/lol9876.mp4" 9876

fsutil file createnew "folder3/dup1.mp4" 100
fsutil file createnew "folder3/dup12.mp4" 100
fsutil file createnew "folder3/dup123.mp4" 100

```

# testing

In this example, we are using PowerShell.

There are 2 Python3 scripts "hasher.py" and "compare_hashes.py".
"hasher.py" will take the first argument as the number of storage folders to sync, followed by the folder names.

```
python3 hasher.py "3" "folder1" "folder2" "folder3"
```

This will hash all the files inside the folder and place them in the "hashes" folder in the root directory. It will also find duplicated files and list the location (file path) of it in the json file generated.

# Todo

- add a script to automatically copy/sync all the folders
- validating all the folders are in-sync
- automated folder generation when syncing new files
