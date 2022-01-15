import pandas as pd
from datetime import datetime
import os
import logging

class Currencies:
    def __init__(self):
            self.backup_dir = "bck/"
            self.currencies = self.load_backup()
            
    def load_backup(self):
        try:
            file_list = os.listdir(self.backup_dir)
            file_list.sort(reverse=True)
            last_file = file_list[0]
            backup = pd.read_csv(os.path.join(self.backup_dir, last_file),
                                 sep=";",
                                 index_col=0)
            
            logging.info("{0} backup restored".format(last_file))
            return backup
        except:
            logging.warning("No backup file found, creating empty Dataframe")
            return pd.DataFrame()
        
        
    def append_currency(self, df_new_currency):
        self.currencies = pd.concat([self.currencies, df_new_currency],
                                    axis=1)
        print("Merged dataframes")
        
    def save_backup(self):
        date_formatted = datetime.now().strftime("%Y%m%d_%H%M")
        self.currencies.to_csv(self.backup_dir+"currencies"+date_formatted+".csv",
                               sep=";")
        print("Backup created")