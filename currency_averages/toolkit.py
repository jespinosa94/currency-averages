import yaml
import os
import re
import pprint

def read_config(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def get_fxtop_files(downloads_path):
    file_pattern = re.compile("^FXTOP.*")
    file_list = os.listdir(downloads_path)
    file_list_filtered = list(filter(file_pattern.match, file_list))
    return file_list_filtered
    
    
def remove_files_from(path):
    """Delete all files in list
    """
    file_list = get_fxtop_files(path)
    for file in file_list:
        f = os.path.join(path, file)
        os.remove(f)