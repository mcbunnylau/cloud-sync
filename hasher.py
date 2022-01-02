import sys
import hashlib
import time
from pathlib import Path
import json
import os

def hashing(file_path):
    assert os.path.isfile(file_path)
    start_time = time.time()
    # BUF_SIZE is totally arbitrary, change for your app!
    BUF_SIZE = 60 * 1024 # lets read stuff in 1Kb chunks!

    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()

    with open(file_path, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            # md5.update(data)
            # sha1.update(data)
            sha256.update(data)

    # print("MD5: {0}".format(md5.hexdigest()))
    # print("SHA1: {0}".format(sha1.hexdigest()))
    print("SHA256: {0}".format(sha256.hexdigest()))

    print("--- SHA256 hashed in: %s seconds ---" % (time.time() - start_time))
    return sha256.hexdigest()

def createFileBlock(file_hash, local_file_path):
    block = {
        "file_hash": file_hash,
        "local_file_path": local_file_path,
    }
    return block

def generateFileHashes(file_hashes, folder_name):
    file_hashes["length"] = len(file_hashes["files"])
    with open('hashes/' + folder_name + '_file_hashes.json', 'w') as outfile:
        json.dump(file_hashes, outfile, indent=2)
    return file_hashes

def fetchFolder(args):
    folders = args[1] # number of folders

    folder_list = []
    for i in range(int(folders)):
        # _folders = [x[0] for x in os.walk(args[i+2])] # sys.argv[] starts from 1 not 0, ignoring first arg
        # for folder in _folders:
        temp = []
        temp.append(Path(args[i+2]).rglob("*"))
        temp.append(str(args[i+2])) # name of folder
        folder_list.append(temp)
    
    return folder_list

def generateFolderHashes(folder_list):
    json_file_hashes_list = []
    for folder in folder_list:
        file_hashes = {"files": {}, "duplicate files": {"length": 0}}
        _folder = folder[0]
        folder_name = folder[1]

        for file_path in _folder:
            try:
                print(folder_name + ": " + str(file_path)) # print file_path and folder_name
                hash = hashing(file_path)

                # check to see if duplicate files
                if hash in file_hashes["files"]:
                    try:
                        file_hashes["duplicate files"][hash].append(str(file_path))
                    except:
                        duplicate_file_path_list = [file_hashes["files"][hash]["local_file_path"], str(file_path)]
                        file_hashes["duplicate files"][hash] = duplicate_file_path_list
                    file_hashes["duplicate files"]["length"] = len(file_hashes["duplicate files"]) - 1
                else:
                    file_hashes["files"][hash] = createFileBlock(hash, str(file_path))
            except:
                pass

        json_file_hashes = generateFileHashes(file_hashes, folder_name)
        json_file_hashes_list.append(json_file_hashes)
    return json_file_hashes_list

def main():
    folder_list = fetchFolder(sys.argv)
    print(folder_list)
    json_file_hashes_list = generateFolderHashes(folder_list)
    # print(json_file_hashes_list)
        
main()