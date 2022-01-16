import pandas as pd
from datetime import datetime
import os
import logging
import toolkit

class Currencies:
    def __init__(self):
            self.backup_dir = "bck/"
            self.currencies = self.load_backup()
            self.new_currencies = {}
            
    def load_backup(self):
        try:
            file_list = os.listdir(self.backup_dir)
            file_list.sort(reverse=True)
            last_file = file_list[0]
            backup = pd.read_csv(os.path.join(self.backup_dir, last_file),
                                 sep=";",
                                 parse_dates=True,
                                 index_col=0)
            
            logging.info("{0} backup restored".format(last_file))
            return backup
        except:
            logging.warning("No backup file found, creating empty Dataframe")
            return pd.DataFrame()
        
        
    def append_currency(self, df_new_currency, new_currency):
        self.currencies = pd.concat([self.currencies, df_new_currency],
                                    axis=1)
        
        logging.info("{0} dataframe included".format(new_currency))
        
    def save_backup(self):
        toolkit.check_folder_exists(self.backup_dir)
        date_formatted = datetime.now().strftime("%Y%m%d_%H%M")
        self.currencies.to_csv(self.backup_dir+"currencies"+date_formatted+".csv",
                               sep=";")
        logging.info("backup file created")
        
    def detect_new_currencies(self, db_currencies):
        current_currencies = self.currencies.columns.values
        new_currencies = set(db_currencies) - set(current_currencies)
        
        logging.info("new currencies detected: {0}".format(new_currencies))
        
        self.new_currencies = new_currencies