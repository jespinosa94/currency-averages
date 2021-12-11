import yaml
import os
import re
import pandas as pd


class Config:
    def __init__(self):
        config = read_config("config/config.yaml")
        self.downloads_folder = config['downloads_folder']

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
        
def load_historical_data(folder):
    """Loads all files from downloads folder into a pandas dataframe
    1. get all files from downloads folder
    2. iterate over each file
        load it into a df
        merge to main df
        
    practice loading a file into a df
    """
    print(folder)
    # test = pd.read_csv()
    