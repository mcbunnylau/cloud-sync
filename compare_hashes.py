import json
from pathlib import Path
import sys
import ntpath

folder_name = sys.argv[1]

file_hashes_list = []

global_hashes = {}

file_name_list = []

for path in Path(folder_name).rglob("*"):
    with open(path) as json_file:
        file_hashes = json.load(json_file)
        file_hashes_list.append(file_hashes)
        global_hashes = {**global_hashes, **file_hashes["files"]}
        file_name_list.append(ntpath.basename(path))

for i in range(len(file_hashes_list)):
    missing_hashes = {}
    hashes = global_hashes.keys()
    for hash in hashes:
        if hash not in file_hashes_list[i]["files"]:
            missing_hashes[hash] = global_hashes[hash]
            missing_hashes["length"] = len(missing_hashes) - 1
    print(missing_hashes)

    new_file_hashes = file_hashes_list[i]
    new_file_hashes["missing files"] = missing_hashes

    with open("hashes/" + file_name_list[i], "w") as outfile:
        json.dump(new_file_hashes, outfile, indent=2)

