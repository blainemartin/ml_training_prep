import os
import shutil
import glob

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

# Call the function with your base path
consolidate_files("/content/text-generation-webui/training/datasets/")
