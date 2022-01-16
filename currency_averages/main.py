import logging
import web_extractor as we
import currencies as cur
import toolkit
import config

# setup currencies, load backup and detect new ones
config = config.Config()
currencies = cur.Currencies()
currencies.detect_new_currencies(['USD', 'GBP'])

# extract historical data of new currencies
web_extractor = we.WebExtractor(config.downloads_folder)

for currency in currencies.new_currencies:
    web_extractor.extract_historical_data(currency)
    df_new_currency, new_currency = toolkit.load_historical_data(config.downloads_folder)
    currencies.append_currency(df_new_currency, new_currency)
    

currencies.save_backup()

logging.info("program finished")