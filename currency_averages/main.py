import logging
import web_extractor as we
import currencies as cur
import toolkit
import config

config = config.Config()
currencies = cur.Currencies()
currencies.detect_new_currencies(['USD', 'GBP', 'JPY'])

# web_extractor = we.WebExtractor()
# web_extractor.extract_historical_data("USD")
df_new_currency, new_currency = toolkit.load_historical_data(config.downloads_folder)
currencies.append_currency(df_new_currency, new_currency)
currencies.save_backup()

logging.info("program finished")