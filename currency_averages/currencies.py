import pandas as pd
import os
import logging

class Currencies:
    def __init__(self, backup):
            self.currencies = backup
            self.new_currencies = {}

    def append_currency(self, df_new_currency, new_currency):
        if new_currency is not None:
            self.currencies = pd.concat([self.currencies, df_new_currency],
                                        axis=1)

            logging.info("{0} dataframe included".format(new_currency))
        else:
            logging.warning("No new currencies added")
        

        
    def detect_new_currencies(self, db_currencies):
        current_currencies = self.currencies.columns.values
        new_currencies = set(db_currencies) - set(current_currencies)
        
        logging.info("new currencies detected: {0}".format(new_currencies))
        
        self.new_currencies = new_currencies