"""
# Text Generation Web UI - File Consolidation Script

This script is designed to consolidate all text files in a given directory into a single text file and a consolidated subdirectory. It is primarily used by the Training module of the Text Generation Web UI.

## How to Use

To use this script, you need to pass the base path of the directory containing the text files as an argument to consolidate_files.py. For example:

python consolidate_files.py /content/text-generation-webui/training/datasets

### What It Does
Scans for text files in the base directory and all its subdirectories (recursively) and copies them to the consolidated directory.
Concatenates all the text files in the consolidated directory into a single text file, adding the name of each file as a header.
The resulting consolidated directory can be used by the Training module of the Text Generation Web UI, and the consolidated text file can be used by the Training Pro module of the Text Generation Web UI.
"""

import os
import shutil
import glob
import sys

def consolidate_files(base_path):
    # Define the paths
    consolidated_path = os.path.join(base_path, "consolidated")
    consolidated_file_path = os.path.join(base_path, "consolidated.txt")

    # Delete the consolidated directory if it exists
    if os.path.exists(consolidated_path):
        shutil.rmtree(consolidated_path)

    # Create the consolidated directory
    os.makedirs(consolidated_path)

    # Delete the consolidated file if it exists
    if os.path.exists(consolidated_file_path):
        os.remove(consolidated_file_path)

    # Scan for txt files and copy them to the consolidated directory
    for txt_file in glob.glob(base_path + '**/*.txt', recursive=True):
        if txt_file != consolidated_file_path:
            shutil.copy2(txt_file, consolidated_path)

    # Concatenate all text files in the consolidated directory into one file
    with open(consolidated_file_path, 'w') as outfile:
        for filename in sorted(glob.glob(os.path.join(consolidated_path, '*.txt'))):
            with open(filename, 'r') as readfile:
                outfile.write('\n' + os.path.basename(filename).upper() + '\n')
                shutil.copyfileobj(readfile, outfile)

if __name__ == "__main__":
    consolidate_files(sys.argv[1])
