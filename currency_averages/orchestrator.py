import logging
import os
import re
import pandas as pd
from datetime import datetime
import currencies as cur
import web_extractor as we


class Orchestrator:
    """Orchestrates all actions between the currencies, the web extractor
    and the files in the system."""
    def __init__(self, config):
        self.config = config
        self.currencies = cur.Currencies(self.load_backup())
        self.__remove_files_from(config.downloads_folder)

    @staticmethod
    def check_folder_exists(folder_route):
        """Check if directory exists, if not, create it"""

        if not os.path.isdir(folder_route):
            os.makedirs(folder_route)

    @staticmethod
    def get_fxtop_files(downloads_path):
        file_pattern = re.compile("^FXTOP.*")
        file_list = os.listdir(downloads_path)
        file_list_filtered = list(filter(file_pattern.match, file_list))
        return file_list_filtered

    @staticmethod
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

    def __remove_files_from(self, path):
        """Delete all files in list
        """
        if not self.config.enable_remove_files:
            return

        file_list = Orchestrator.get_fxtop_files(path)
        for file in file_list:
            f = os.path.join(path, file)
            os.remove(f)

    def __load_historical_data(self):
        """Loads all files from downloads folder into a pandas dataframe
        """
        try:
            file_list = self.get_fxtop_files(self.config.downloads_folder)
            currency_dfs = []
            currency_header = file_list[1].split("_")[3][:3]

            for file in file_list:
                currency_dfs.append(self.load_file(
                    os.path.join(self.config.downloads_folder, file)
                ))

            merged_df = pd.concat(currency_dfs)
            merged_df.rename({"Average": currency_header},
                             inplace=True,
                             axis="columns")
            merged_df.sort_index(inplace=True)

            currency = merged_df.columns.values[0]

            logging.info("{0} historical data retrieved".format(currency))

            self.__remove_files_from(self.config.downloads_folder)

            return merged_df, currency
        except:
            logging.warning("No historical files found in directory")
            return pd.DataFrame(), None

    def __load_last_months(self, folder):
        """Loads each file corresponding to a currency and updates the final
        currency values.
        """
        file_list = self.get_fxtop_files(folder)
        result = self.currencies.currencies

        for file in file_list:
            # 'FXTOP_PRICES_EUR_GBP.xlsx' --> GBP.xlsx --> GBP
            currency_header = file.split('_')[3].split('.')[0]
            df_new = self.load_file(os.path.join(folder, file))
            df_new.rename({"Average": currency_header}, inplace=True, axis="columns")
            result = pd.concat([result, df_new])

            # Adds only new months to the dataframe
            result = result[~result.index.duplicated(keep='first')]

            # Override past months
            result.update(df_new)

        self.currencies.currencies = result
        logging.info("{0} currencies updated".format(len(file_list)))

    def load_backup(self):
        try:
            file_list = os.listdir(self.config.backup_folder)
            file_list.sort(reverse=True)
            last_file = file_list[0]
            backup = pd.read_csv(os.path.join(self.config.backup_folder,
                                              last_file),
                                 sep=";",
                                 parse_dates=True,
                                 index_col=0)

            logging.info("{0} backup restored".format(last_file))
            return backup
        except:
            logging.warning("No backup file found, creating empty Dataframe")
            return pd.DataFrame()

    def detect_new_currencies(self, new_currencies):
        self.currencies.detect_new_currencies(new_currencies)

    def extract_historical_from_new_currencies(self):
        historical_we = we.WebExtractor(self.config)
        for currency in self.currencies.new_currencies:
            historical_we.extract_currency(currency)
            df_new_currency, new_currency = self.__load_historical_data()
            self.currencies.append_currency(df_new_currency, new_currency)

    def update_currencies(self):
        update_we = we.WebExtractor(self.config)
        update_we.extract_last_months(self.currencies.currencies.columns.values)
        self.__load_last_months(self.config.downloads_folder)

    def save_backup(self):
        self.check_folder_exists(self.config.backup_folder)
        date_formatted = datetime.now().strftime("%Y%m%d_%H%M")
        self.currencies.currencies.to_csv(self.config.backup_folder
                                          + "currencies"
                                          + date_formatted+".csv",
                                          sep=";")
        logging.info("backup file created")

    def close_program(self):
        logging.info("program finished")
