import yaml
import os
import re
import pprint

def read_config(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)
    
def clear_downloads_path(path):
    """Delete all FXTOP files
    """
    file_pattern = re.compile("^FXTOP.*")
    file_list = os.listdir(path)
    file_list_filtered = list(filter(file_pattern.match, file_list))
    for file in file_list_filtered:
        f = os.path.join(path, file)
        os.remove(f)