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

def load_file(path):
    """Loads a single file from the specified path and returns a df
    """
    df = pd.read_excel(path,
                       header=None,
                       skiprows=2,
                       index_col=0,
                       usecols=[0, 1],
                       names=["YearMonth", "Average"],
                       parse_dates=True)
    return df
    

def load_historical_data(folder):
    """Loads all files from downloads folder into a pandas dataframe
    """
    file_list = get_fxtop_files(folder)
    currency_dfs = []
    currency_header = file_list[1].split("_")[3][:3]
    
    for file in file_list:
        currency_dfs.append(load_file(
            os.path.join(folder, file)
        ))
    
    merged_df = pd.concat(currency_dfs)
    merged_df.rename({"Average": currency_header}, inplace=True, axis="columns")
    merged_df.sort_index(inplace=True)
    
    remove_files_from(folder)    
    return merged_df